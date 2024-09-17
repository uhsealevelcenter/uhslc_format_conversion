#!/bin/bash

export PATH=/home/uhslc/anaconda3/bin:$PATH

cd ~/uhslc_format_conversion

date
time python3 convert_fd.py

tar czf netcdf.tgz -C data netcdf
rsync -au data/csv data/netcdf meta.geojson netcdf.tgz /srv/htdocs/uhslc.soest.hawaii.edu/data

#time python3 meta2fdhtml.py  > /srv/htdocs/uhslc.soest.hawaii.edu/data/fd.html
## time python3 meta2xml.py  > /srv/htdocs/uhslc.soest.hawaii.edu/icontent/StationMap/js/stations.xml
#time python3 meta2allxml.py > /srv/htdocs/uhslc.soest.hawaii.edu/station/list/all.xml

python3 meta2fdhtml.py  > /srv/htdocs/uhslc.soest.hawaii.edu/data/fd.html
python3 meta2allxml.py > /srv/htdocs/uhslc.soest.hawaii.edu/station/list/all.xml

# Generate fd metadata csv for routine insert to database.
#python3 /home/samw/metadata/fd_metadata_2_csv.py

date

