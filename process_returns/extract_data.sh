#!/bin/bash -l

if test $# -ne 1
then
  echo Usage: $0 batch_id
  exit 1
fi

# Script to extract data from BATCH to a directory on the server where the data is stored
# Example paths are given for the GPFS filesystem on cpdn-ppc01 (data for upload2 in Oxford)
# Author: Sihan Li
# Modified: 08/09/2017
#

#Batch 882 Baseline
#Batches 883 and 896 Future 2066
#Batches 886 and 897 Future 2068
#Batches 887 and 898 Future 2072 
# - Batch 877 -> Baseline          : potentially more corruption
# - Batch 878 -> Future 2066 (hot) : potentially more corruption
# - Batch 879 -> Future 2068 (wet) : potentially more corruption



# Set up paths
EXTRACT_SCRIPTS_DIR=cpdn_extract_scripts

# Current URL for uploads includes project and batch number
BATCH=$1
# Specify a certain year to extract, if extract all years, set to 0
YEAR=0


# Start and end zip to extract data from:
START_ZIP=2
END_ZIP=5

# Extract data from the batch directory ['ga.pd',5216,[],'all',-0.0001,1,24,'mean','z0'],\
python $EXTRACT_SCRIPTS_DIR/wah_extract_local_hadam4.py -i $BATCH_DATA_DIR \
-f "\
['ga.pe',5216,[],'all',-0.0001,1,720,'mean',''],\
['ga.pb',5216,[],'all',-0.0001,1,6,'mean',''],\
['ga.pc',5216,[],'all',-0.0001,1,24,'maximum',''],\
['ga.pc',3236,[],'all',150,400,24,'maximum',''],\
['ga.pd',3236,[],'all',150,400,24,'minimum',''],\
['ga.pa',3236,[],'all',150,400,24,'mean',''],\
['ga.pa',3245,[],'all',-30,200,24,'mean',''],\
['ga.pa',3249,[],'all',0,200,24,'mean',''],\
['ga.pb',3249,[],'all',0,200,6,'maximum',''],\
['ga.pa',8234,[],'all',0,200,24,'mean',''],\
['ga.pa',8235,[],'all',0,200,24,'mean',''],\
['ga.pc',16222,[],'all',50000,200000,24,'mean',''],\
['ga.pa',15201,[],'all',-200,200,24,'mean','any'],\
['ga.pa',15202,[],'all',-200,200,24,'mean','any'],\
['ga.pa',16202,[],'all',1000,10000,24,'mean','any'],\
['ga.pd',15202,[],'all',-200,200,24,'mean','any'],\
['ga.pb',1,[],'all',50000,200000,0,'mean',''],\
['ga.pc',15201,[],'all',-200,200,0,'mean','any'],\
['ga.pc',15226,[],'all',0,1,0,'mean','any'],\
['ga.pc',16203,[],'all',150,400,0,'mean','any'],\
['ga.pa',4203,[],'all',-0.0001,1,24,'mean',''],\
['ga.pa',2207,[],'all',0,1000,24,'mean',''],\
['ga.pa',1235,[],'all',0,1000,24,'mean',''],\
"  -o $EXTRACT_DATA_DIR/${BATCH} -y $YEAR -s $START_ZIP -e $END_ZIP

#['ga.pf',16202,[],'all',10000,100000,24,'mean','z7'],\
#['ga.pf',15201,[],'all',0,200,24,'mean','z4'],\
#['ga.pf',15201,[],'all',0,200,24,'mean','z4'],\


#['ga.pe',5216,[],'all',-0.0001,1,720,'mean',''],\                   # monthly mean precip
#['ga.pb',5216,[],'all',-0.0001,1,6,'mean',''],\                   # 6hrly mean precip
#['ga.pc',5216,[],'all',-0.0001,1,24,'maximum',''],\                   # daily max precip
#['ga.pc',3236,[],'all',150,400,24,'maximum',''],\                  # daily max temp
#['ga.pd',3236,[],'all',150,400,24,'minimum',''],\                  # daily min temp
#['ga.pa',3236,[],'all',150,400,24,'mean',''],\                     # daily mean temp
#['ga.pa',3245,[],'all',0,200,24,'mean',''],\                     # daily rel hum at surface
#['ga.pa',3249,[],'all',0,200,24,'mean',''],\                     # daily 10m wind speed
#['ga.pb',3249,[],'all',0,200,6,'maximum',''],\                     # 6hrly maximum 10m wind speed
#['ga.pa',8234,[],'all',0,200,24,'mean',''],\                     # daily surface runoff
#['ga.pa',8235,[],'all',0,200,24,'mean',''],\                     # daily subsurface runoff
#['ga.pc',16222,[],'all',50000,200000,24,'mean',''],\                     # daily mslp
#['ga.pf',16202,[],'all',10000,100000,24,'mean','z7']             # daily 500 gph
#['ga.pf',15201,[],'all',0,200,24,'mean','z4']             # daily 850 westerly wind speed
#['ga.pf',15201,[],'all',0,200,24,'mean','z4']             # daily 850 westerly wind speed


#Examples
#['ga.pe',5216,[],'all',-0.0001,1,720,'mean',''],\
#['ga.pc',15201,[],'all',-200,200,6,'mean','pressure_0'],\
#['ga.pd',5216,[],'all',-0.0001,1,24,'mean','z0'],\
#['ma.pc',3236,[],'all',150,400,720,'maximum',''],\
#['ma.pc',3236,[],'min',150,400,720,'minimum',''],\
#['ma.pc',3236,[],'all',150,400,720,'mean',''],\
#['ga.pe',5216,[],'all',-0.0001,1,720,'mean',''],\
#['ga.pe',15201,[],'all',-100,100,720,'mean','z7'],\
#['ga.pe',15202,[],'all',-100,100,720,'mean','z7'],\
#['ga.pe',16203,[],'all',150,400,720,'mean','z7'],\
#['ga.pe',16202,[],'all',1000,15000,720,'mean','z7'],\




