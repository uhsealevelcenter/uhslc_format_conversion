# ---------------------------------------------------------------------------

import os
import gc
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
# RESEARCH QUALITY
# ---------------------------------------------------------------------------

# names of basin divisions in the RQ data set
basins = ['atlantic', 'pacific', 'indian']
#basins = ['pacific']

# ---------------------------------------------------------------------------

for b in basins:

    # -----------------------------------------------------------------------
    # DAILY

    # target directories for basin daily files
    nc_dir_bd = init['nc_dir'] + 'rqds/' + b + '/daily/'
    csv_dir_bd = init['csv_dir'] + 'rqds/' + b + '/daily/'
    
    # create target directories if necessary
    if not os.path.exists(nc_dir_bd):
        os.makedirs(nc_dir_bd)
    if not os.path.exists(csv_dir_bd):
        os.makedirs(csv_dir_bd)
    
    # get names of .dat files
    sta_files = glob(init['dat_dir'] + 'rqds/' + b + '/daily/*.dat')
    
    # loop over daily .dat files
    pb = rw.ProgressBar(len(sta_files), '\nConverting daily RQ ' + b + ' ...')
    for idx, f in enumerate(sta_files):
    
        sta = rw.StationDailyRQ(b)
    
        try:
            sta.dat_read(f, meta)
            if sta.uhslc_id.data: # protection if .dat file is empty
                sta.trim()
                meta.update(sta)
                sta.write_netcdf(nc_dir_bd, init['t_ref_str'])
                sta.write_csv(csv_dir_bd)
        except Exception as e:
            msg = 'While processing ' + str(f) + ':\n' + str(e)
            print(msg)
            
        gc.collect() # force garbage collection
        
        meta.write_json()
        pb.update()
        
    # -----------------------------------------------------------------------
    # HOURLY
    
    # target directories for basin hourly files
    nc_dir_bh = init['nc_dir'] + 'rqds/' + b + '/hourly/'
    csv_dir_bh = init['csv_dir'] + 'rqds/' + b + '/hourly/'
    
    # create target directories if necessary
    if not os.path.exists(nc_dir_bh):
        os.makedirs(nc_dir_bh)
    if not os.path.exists(csv_dir_bh):
        os.makedirs(csv_dir_bh)
    
    # get directories with .dat files for each station
    sta_dir = glob(init['dat_dir'] + 'rqds/' + b + '/hourly/*/')
    
    # read the station .dat files and write new formats
    pb = rw.ProgressBar(len(sta_dir), '\nConverting hourly RQ ' + b + ' ...')
    for idx, d in enumerate(sta_dir):
    
        # aggregate data from .dat files for this station
        sta_files = glob(d + '*.dat')
        sta = rw.StationHourlyRQ(b)
    
        try:
            for f in sta_files:
                sta.dat_read_append(f, meta)
            if sta.uhslc_id.data: # protection if .dat file is empty
                sta.trim()
                meta.update(sta)
                sta.write_netcdf(nc_dir_bh, init['t_ref_str'])
                # sta.write_csv(csv_dir_bh)
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
      






