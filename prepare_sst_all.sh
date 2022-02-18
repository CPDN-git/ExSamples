#!/bin/bash

for f in sst/sst*
do
    echo ${f}
    mkdir tmp
    # Select the surface temperature data fromo the HadGEM UKCP file
    cdo -selvar,surface_temperature ${f} tmp/st.nc
    # Multiply by the land-sea mask from the model to retain only sea points
    cdo -mul tmp/st.nc -seltimestep,1 sic_mask4.nc tmp/tmp1.nc
    # Set the missing value
    cdo -setmissval,2e20 tmp/tmp1.nc tmp/tmp2.nc
    # Set data points with a value of 0 to missing
    cdo -setctomiss,0 tmp/tmp2.nc ${f%.nc}_masked.nc
    rm -fr tmp
done

for f in sst/sst*masked.nc
do

echo ${f}
mkdir tmpsst

#Use ncl's poisson_grid_fill to fill in the SST data before regridding
#NCARG_ROOT="/usr"

ncl <<EOF
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"  
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"  
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl" 

begin

setfileoption("nc","Format","NetCDF4")

;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
; read infile
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 fin=addfile ("${f}.nc" , "r")
 sst = fin->surface_temperature

;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
; interpolation
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 guess     = 1                ; use zonal means
 is_cyclic = True             ; cyclic [global]
 nscan     = 2000             ; usually much less than this
 eps       = 1.e-2            ; variable dependent
 relc      = 0.6              ; relaxation coefficient
 opt       = 0                ; not used

 poisson_grid_fill( sst, is_cyclic, guess, nscan, eps, relc, opt)

;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
; output
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 fout  = addfile ("tmpsst/filled.nc", "c") 
 copy_VarAtts(fin,fout)

 fout->surface_temperature=sst

 end
 
EOF

cp tmpsst/filled.nc ${f%.nc}_filled.nc

# Remap the filled data to the HadAM4 grid
cdo -remapbil,hadam4_grid.txt tmpsst/filled.nc tmpsst/remapped.nc
# Apply the HadAM4 land sea mask to the data
cdo -add tmpsst/remapped.nc n216_add_mask.nc tmpsst/masked.nc
# Set the missing data value
cdo -setmissval,2e20 tmpsst/masked.nc tmpsst/masked2.nc
# Set very high values to missing
cdo -setrtomiss,999,2000 tmpsst/masked2.nc tmpsst/masked3.nc
# Set values with temperature less than -1.8C to -1.8C this is for sst under ice which  the model requires to be this value to prevent ice melt.
cdo -setrtoc,0,271.34,271.34  tmpsst/masked3.nc ${f%.nc}_AM4.nc

rm -fr tmpsst

done
