# ---------------------------------------------------------------------------

import os
import gc
from glob import glob
import numpy as np
import shutil
import sys
import urllib.request
import time
import zipfile

import readwrite as rw

if len(sys.argv) == 2:
    stnid = str(sys.argv[1])
else:
    stnid = '*'

# ---------------------------------------------------------------------------
# setup source dirs
os.makedirs('fast', exist_ok=True)
os.makedirs('global', exist_ok=True)

# setup output dirs
os.makedirs('data/dat/rqds', exist_ok=True)
os.makedirs('data/dat/fast', exist_ok=True)
os.makedirs('data/csv', exist_ok=True)
os.makedirs('data/netcdf', exist_ok=True)

# Collect source data, probably move this to class
fdfile = 'all_fast.zip'

if not os.path.isfile(fdfile) or (time.time() - os.path.getmtime(fdfile) > 86400):

    print ('Download FD\n')
    url = 'https://uhslc.soest.hawaii.edu/woce/all_fast.zip'
    zfn =  os.path.basename(url)
    with urllib.request.urlopen(url) as response, open(zfn, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    with zipfile.ZipFile(zfn,"r") as zip_ref:
        zip_ref.extractall('data/dat')

# initialize source and target directories, etc.
# see first function definition in readwrite.py
init = rw.conversion_setup()

# load/create metdata container
meta = rw.Metadata()

# ---------------------------------------------------------------------------
# FAST DELIVERY
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# DAILY

# target directories for daily FD files
nc_dir_fdd = init['nc_dir'] + 'fast/daily/'
csv_dir_fdd = init['csv_dir'] + 'fast/daily/'

# create target directories if necessary
if not os.path.exists(nc_dir_fdd):
    os.makedirs(nc_dir_fdd)
if not os.path.exists(csv_dir_fdd):
    os.makedirs(csv_dir_fdd)

# get names of .dat files
sta_files = glob(init['dat_dir'] + 'fast/d' + stnid + '.dat')

# loop over daily .dat files
pb = rw.ProgressBar(len(sta_files), '\nConverting daily FD ...')
for idx, f in enumerate(sta_files):

    sta = rw.StationDailyFD()

    try:
        sta.dat_read(f, meta)
        if sta.uhslc_id.data: # protection if .dat file is empty
            sta.trim()
            meta.update(sta)
            sta.write_netcdf(nc_dir_fdd, init['t_ref_str'])
            sta.write_csv(csv_dir_fdd)
    except Exception as e:
        msg = 'While processing ' + str(f) + ':\n' + str(e)
        print(msg)
    
    gc.collect() # force garbage collection
   
    meta.write_json() 
    pb.update()

# ---------------------------------------------------------------------------
# HOURLY

# target directories for hourly FD files
nc_dir_fdh = init['nc_dir'] + 'fast/hourly/'
csv_dir_fdh = init['csv_dir'] + 'fast/hourly/'

# create target directories if necessary
if not os.path.exists(nc_dir_fdh):
    os.makedirs(nc_dir_fdh)
if not os.path.exists(csv_dir_fdh):
    os.makedirs(csv_dir_fdh)

# get names of .dat files
sta_files = glob(init['dat_dir'] + 'fast/h' + stnid + '.dat')

# loop over hourly .dat files
pb = rw.ProgressBar(len(sta_files), '\nConverting hourly FD ...')
for idx, f in enumerate(sta_files):

    sta = rw.StationHourlyFD()

    try:
        sta.dat_read(f, meta)
        if sta.uhslc_id.data: # protection if .dat file is empty
            sta.trim()
            meta.update(sta)
            sta.write_netcdf(nc_dir_fdh, init['t_ref_str'])
            sta.write_csv(csv_dir_fdh)
    except Exception as e:
        msg = 'While processing ' + str(f) + ':\n' + str(e)
        print(msg)
        
    gc.collect() # force garbage collection
   
    meta.write_json() 
    pb.update()
    
# ---------------------------------------------------------------------------

# list stations not in the IOC SSC
meta.not_in_SSC()

# write meta data to json file
meta.write_json()

# ---------------------------------------------------------------------------

# copy to web services     
# os.system("tar czf netcdf.tgz -C data netcdf")
# os.system("rsync -avu data/csv data/netcdf meta.geojson netcdf.tgz wyrtki:/srv/htdocs/uhslc.soest.hawaii.edu/data")




