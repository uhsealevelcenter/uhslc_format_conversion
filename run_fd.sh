#!/bin/bash

export PATH=/home/uhslc/anaconda3/bin:$PATH

cd /home/uhslc/uhslc_format_conversion

SRV_HOME="/srv/htdocs/uhslc.soest.hawaii.edu"

date

### UPDATE FAST DELIVERY DATA FROM THE SOURCE AND THE META GEOJSON FILE. ###
time /home/uhslc/anaconda3/bin/python3 convert_fd.py

### SYNC UPDATED DATA TO THE WEB. ###
tar czf netcdf.tgz -C data netcdf
rsync -au data/csv data/netcdf meta.geojson netcdf.tgz ${SRV_HOME}/data

### UPDATE THE FAST DELIVERY WEB HTML AND XML. ###
/home/uhslc/anaconda3/bin/python3 meta2fdhtml.py > ${SRV_HOME}/data/fd.html
/home/uhslc/anaconda3/bin/python3 meta2allxml.py > ${SRV_HOME}/station/list/all.xml

### CLEAN UP LOGS OLDER THAN 30 DAYS. ###
find /tmp/ -type f -name "makefd_*.log" -mtime +30 2>/dev/null | xargs -i rm {}

date
