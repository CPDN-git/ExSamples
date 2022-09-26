#!/bin/bash
#
#2868 anth_so2_scaling= 0.869377575     biomass scaling= 3.271871983     DMS_scaling= 1.554533208     sea salt emissions= 1.584505068
# 
#1554 anth_so2_scaling= 0.799006918     biomass scaling= 0.725782224     DMS_scaling= 0.686635027     sea salt emissions= 0.737035216
# 
#2242 anth_so2_scaling= 0.717568767     biomass scaling= 2.298518765     DMS_scaling= 1.694482566     sea salt emissions= 0.611892792

ens=(2868 1554 2242)
so2_scales=(0.869377575 0.799006918 0.717568767)
dms_scales=(1.554533208 0.686635027 1.694482566)

for i in ${!ens[@]}; do
    echo r001i1p0${ens[${i}]}
    mkdir so2dms/tmp

    for l in low high; do
        echo ${l}
        echo so2_scale ${so2_scales[${i}]} 
        cdo mulc,${so2_scales[${i}]} so2dms/ukca_emiss_SO2_${l}_2005-2016.nc so2dms/tmp/SO2_${l}.nc
    done

    echo dms_scale ${dms_scales[${i}]}
    cdo mulc,${dms_scales[${i}]} so2dms/dms_rcp45_N216_2005_2016.nc so2dms/tmp/dms.nc

    cdo merge so2dms/tmp/dms.nc so2dms/tmp/SO2_low.nc so2dms/tmp/SO2_high.nc so2dms/so2dms_r001i1p0${ens[${i}]}_2005-2016.nc

    rm -fr so2dms/tmp
done
