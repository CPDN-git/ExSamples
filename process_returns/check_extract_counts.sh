cd $EXTRACT_DIR

batches="batch_882 batch_883 batch_886 batch_887 batch_896 batch_897 batch_898 batch_877 batch_878 batch_879"

for b in $batches
do
  vars=`ls -d /ExSamples/netcdf/$b/region/*`
#  echo $vars
  echo $b `ls -lrt /ExSamples/archive/$b/ | wc -l` 
  for v in $vars; do echo $v `ls $v | wc -l`; done
  echo
done


exit
