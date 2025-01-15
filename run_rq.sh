#!/bin/bash

export PATH=/home/uhslc/anaconda3/bin:$PATH

FORCE_RUN=$1

cd ~/uhslc_format_conversion

SRC_HOME="/home/kaimoku/data/rqds"
SRV_HOME="/srv/htdocs/uhslc.soest.hawaii.edu"

### CHECK FOR NEW METADATA AND NEW DATA FILES TO DETERMINE WHETHER TO PROCEED. ###
NEW_METADATA_CHECK=`find ${SRC_HOME}/metadata_yaml/ -type f -name "*yaml" -mtime -1`
NEW_DATA_CHECK=`find ${SRC_HOME}/ -type f \( -name "*.zip" -o -name "*.dat" \) -mtime -1`
if [ ! -z "${NEW_METADATA_CHECK}" ] || [ ! -z "${NEW_DATA_CHECK}" ] || [ "${FORCE_RUN}" = "force" ]; then

  date

  ### UPDATE RESEARCH QUALITY DATA FROM THE SOURCE AND THE META GEOJSON FILE. ###
  time python3 convert_rq.py

  ### SYNC UPDATED DATA TO THE WEB. ###
  tar czf netcdf.tgz -C data netcdf
  rsync -au data/csv data/netcdf meta.geojson netcdf.tgz ${SRV_HOME}/data
  rsync -auv ${SRV_HOME}/data/netcdf/rqds/{pacific,atlantic,indian}/hourly/h* ${SRV_HOME}/data/netcdf/rqds/global/hourly
  rsync -auv ${SRV_HOME}/data/netcdf/rqds/{pacific,atlantic,indian}/daily/d* ${SRV_HOME}/data/netcdf/rqds/global/daily

  ### UPDATE THE RESEARCH QUALITY WEB HTML. ###
  python3 meta2rqhtml.py  > ${SRV_HOME}/data/rq.html

  ### CLEAN UP LOGS OLDER THAN 30 DAYS. ###
  find /tmp/ -type f -name "makerq_*.log" -mtime +30 2>/dev/null | xargs -i rm {}

  date

fi
