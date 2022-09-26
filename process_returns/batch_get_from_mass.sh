cd $EXTRACT_DIR
batches="batch_882 batch_883 batch_886 batch_887 batch_896 batch_897 batch_898 batch_877 batch_878 batch_879"

for b in $batches
do
  sbatch --time=359 --output=get_from_mass_$b.log ./get_from_mass.sh $b
done

exit

