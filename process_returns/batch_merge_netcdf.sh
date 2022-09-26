cd $EXTRACT_DIR

batches="batch_882 batch_883 batch_886 batch_887 batch_897 batch_898 batch_877 batch_878 batch_879 batch_896"
#batches="batch_883 batch_886 batch_887 batch_897 batch_898 batch_878 batch_879 batch_896"



vars="item1235_daily_mean item16202_daily_mean item3236_daily_maximum item3249_daily_mean  item8234_daily_mean item15201_0hrly_mean item16203_0hrly_mean item3236_daily_mean item4203_daily_mean   item8235_daily_mean item15201_daily_mean item16222_daily_mean item3236_daily_minimum item5216_6hrly_mean    item15202_daily_mean item1_0hrly_mean   item3245_daily_mean   item5216_daily_maximum
item15226_0hrly_mean item2207_daily_mean  item3249_6hrly_maximum"

#vars="item5216_monthly_mean"



for b in $batches
do
 for v in $vars
 do
  case $v in
  *6hrly*) sbatch --mem=120000 --time=120 --output=merge_netcdf_${b}_$v.log python merge_netcdf.py $b $v;;
  *daily*) sbatch --mem=120000 --time=120 --output=merge_netcdf_${b}_$v.log python merge_netcdf.py $b $v;;
  *) sbatch --mem=50000 --time=120 --output=merge_netcdf_${b}_$v.log python merge_netcdf.py $b $v;;
  esac
 done
done

exit

