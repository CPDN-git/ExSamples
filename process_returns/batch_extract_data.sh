cd $EXTRACT_DIR
# may have to load conda environment

batches="batch_882 batch_883 batch_886 batch_887 batch_896 batch_897 batch_898 batch_877 batch_878 batch_879"
#batches="batch_882 batch_883 batch_886 batch_887 batch_897 batch_898 batch_877 batch_878 batch_879"
#batches="batch_877 batch_883"

for b in $batches
do
  sbatch --time=359 --output=extract_data_$b.log ./extract_data.sh $b
#  sbatch --time=359 --output=extract_data_extra_$b.log ./extract_data_extra.sh $b
done

exit

