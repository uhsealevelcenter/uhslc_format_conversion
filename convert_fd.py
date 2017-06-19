# ---------------------------------------------------------------------------

import os
from glob import glob
import numpy as np

import readwrite as rw

# ---------------------------------------------------------------------------

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
sta_files = glob(init['dat_dir'] + 'fast/d*.dat')

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
            # sta.write_csv(csv_dir_fdd)
    except Exception as e:
        msg = 'While processing ' + str(f) + ':\n' + str(e)
        print(msg)
    
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
sta_files = glob(init['dat_dir'] + 'fast/h*.dat')

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
            # sta.write_csv(csv_dir_fdh)
    except Exception as e:
        msg = 'While processing ' + str(f) + ':\n' + str(e)
        print(msg)
        
    pb.update()
    
# ---------------------------------------------------------------------------

# list stations not in the IOC SSC
meta.not_in_SSC()

# write meta data to json file
meta.write_json()

# ---------------------------------------------------------------------------
      






