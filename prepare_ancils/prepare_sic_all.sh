#!/bin/bash
for f in sic/sic*
do
echo ${f}

mkdir tmpsic

#Use ncl's poisson_grid_fill to fill in the sea ice before regridding
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

 fin=addfile ("${f}" , "r")
 sic = fin->sea_ice_area_fraction

;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
; interpolation
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 guess     = 1                ; use zonal means
 is_cyclic = True             ; cyclic [global]
 nscan     = 2000             ; usually much less than this
 eps       = 1.e-2            ; variable dependent
 relc      = 0.6              ; relaxation coefficient
 opt       = 0                ; not used

 poisson_grid_fill( sic, is_cyclic, guess, nscan, eps, relc, opt)

;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
; output
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 fout  = addfile ("tmpsic/filled.nc", "c") 
 copy_VarAtts(fin,fout)

 fout->sea_ice_area_fraction=sic

 end
 
EOF

cp tmpsic/filled.nc ${f%.nc}_filled.nc

# Remap to the HadAM4 model grid
cdo -remapbil,hadam4_grid.txt tmpsic/filled.nc tmpsic/remapped.nc
# Mask to retain only sea values
cdo -add tmpsic/remapped.nc n216_add_mask.nc tmpsic/masked.nc
# Set the missing value
cdo -setmissval,2e20 tmpsic/masked.nc tmpsic/masked2.nc
# Set high values to the missing value
cdo -setrtomiss,999,2000 tmpsic/masked2.nc ${f%.nc}_AM4.nc

rm -fr tmpsic
done
