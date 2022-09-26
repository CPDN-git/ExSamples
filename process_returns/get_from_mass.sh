#!/bin/bash -l

#batch_ids="batch_882 batch_883 batch_886 batch_887 batch_877 batch_878 batch_879"
#batch_ids="batch_882 batch_883 batch_886 batch_887 batch_896 batch_897 batch_898 batch_877 batch_878 batch_879"
#batch_ids="batch_886"
if test $# -lt 1
then
  echo Usage e.g. $0 batch_882 [batch...]
  exit 1
fi

batch_ids=$@

# climateprediction.net worskpace. 
#set up $cpdn_workspace

# MOOSE project directory
# set up $moosedir

outdir=/ExSamples/archive

# 1. get all the tar files
# 2. loop through tar files and untar mimicking cpdn structure .../batch_882/successful/hadam4h_b0e9_200911_5_882_012035521_1

for b in $batch_ids
do
  outdir2=${outdir}/$b
  if test ! -d $outdir2
  then
    mkdir -p $outdir2
  fi
  moo get -i -v $moosedir/$b/ $outdir2
done

for b in $batch_ids
do
  outdir2=${outdir}/$b
  tar_files=$(ls $outdir2/*.tar)
#  echo $tar_files

  for tf in $tar_files
  do
    expt=$(basename $tf .tar)
    outdir3=${outdir}/$b/successful/$expt
    if test ! -d $outdir3
    then
      mkdir -p $outdir3
    fi
    tar -xv -C $outdir3 --strip-components=4 -f $tf > /dev/null 2>&1
    if test $? -ne 0
    then
      echo Problem with $tf. Removing the zip files
      rm -R ${outdir3} $tf
    fi

  done

done

exit


