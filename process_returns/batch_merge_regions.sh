cd $EXTRACT_DIR

# dropped item15202_daily_mean as it was only stored for tropics

batches="2066 2068 2072 base"
#batches="base"
#batches="2066 2068 2072"
#vars="item5216_6hrly_mean item3245_daily_mean item3236_daily_maximum item3249_daily_mean item5216_monthly_mean"
#vars="item5216_6hrly_mean item5216_daily_mean"
#vars="item16222_daily_mean item3236_daily_minimum item8234_daily_mean item3236_daily_mean item3249_6hrly_maximum item5216_daily_maximum item8235_daily_mean item5216_6hrly_mean item5216_daily_mean"
#vars="item5216_daily_mean"

#vars="item3245_daily_mean"

vars="item1235_daily_mean item16202_daily_mean item3236_daily_maximum item3249_daily_mean  item8234_daily_mean item15201_0hrly_mean item16203_0hrly_mean item3236_daily_mean item4203_daily_mean   item8235_daily_mean item15201_daily_mean item16222_daily_mean item3236_daily_minimum item5216_6hrly_mean     item1_0hrly_mean   item3245_daily_mean   item5216_daily_maximum
item15226_0hrly_mean item2207_daily_mean  item3249_6hrly_maximum"

#vars="item5216_monthly_mean"
#vars="item5216_daily_mean"
#vars="item5216_6hrly_mean"
vars="item15202_daily_mean"

regions="UK NAtlanticEurope"

#batches="2066"
#vars="item5216_daily_mean"
#regions="NAtlanticEurope"

for b in $batches
do
for r in $regions
do
  for v in $vars
  do
    case $v in
    *0hrly*) sbatch --mem=20000 --time=120 --output=merge_region_${b}_${r}_$v.log python merge_region.py $b $r $v;;
    *6hrly*) sbatch --mem=20000 --time=180 --output=merge_region_${b}_${r}_$v.log python merge_region.py $b $r $v;;
    *daily*) sbatch --mem=20000 --time=30 --output=merge_region_${b}_${r}_$v.log python merge_region.py $b $r $v;;
    *) sbatch --mem=20000 --time=30 --output=merge_region_${b}_${r}_$v.log python merge_region.py $b $r $v;;
    esac
  done
done
done

exit

