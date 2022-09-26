#!/bin/bash
for f in vegfrac/*
do
echo ${f}

mkdir tmpveg

#Use ncl's poisson_grid_fill to fill in the sea ice before regridding
NCARG_ROOT="/usr"

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
 veg = fin->vegfrac

;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
; interpolation
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 guess     = 1                ; use zonal means
 is_cyclic = True             ; cyclic [global]
 nscan     = 2000             ; usually much less than this
 eps       = 1.e-2            ; variable dependent
 relc      = 0.6              ; relaxation coefficient
 opt       = 0                ; not used

 poisson_grid_fill( veg, is_cyclic, guess, nscan, eps, relc, opt)

;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
; output
;~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 fout  = addfile ("tmpveg/filled.nc", "c") 
 copy_VarAtts(fin,fout)

 fout->vegfrac=veg

 end
 
EOF

cp tmpveg/filled.nc ${f%.nc}_filled.nc

#cdo -remapcon,hadam4_grid.txt tmpveg/filled.nc tmpveg/remapped.nc
cdo -remapnn,hadam4_grid.txt tmpveg/filled.nc tmpveg/remapped.nc
cdo -add tmpveg/remapped.nc n216_add_mask_land.nc tmpveg/masked.nc
cdo -setmissval,2e20 tmpveg/masked.nc tmpveg/masked2.nc
cdo -setrtomiss,999,2000 tmpveg/masked2.nc ${f%.nc}_AM4.nc

#rm -fr tmpveg
done
