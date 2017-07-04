#!/usr/bin/env python3

# ---------------------------------------------------------------------------
# FAST DELIVERY
# ---------------------------------------------------------------------------

import gc
import os,sys
from glob import glob
from multiprocessing import Pool 

import readwrite as rw

# ---------------------------------------------------------------------------

def worker_daily(f):
    # DAILY
    print('processing d:', f)
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

def worker_hourly(f):
    # HOURLY
    print('processing h:', f)
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

# ---------------------------------------------------------------------------
if __name__ == '__main__':

    # initialize source and target directories, etc.
    # see first function definition in readwrite.py
    init = rw.conversion_setup()

    # load/create metdata container
    meta = rw.Metadata()

    # target directories for daily FD files
    nc_dir_fdd = init['nc_dir'] + 'fast/daily/'
    csv_dir_fdd = init['csv_dir'] + 'fast/daily/'
    nc_dir_fdh = init['nc_dir'] + 'fast/hourly/'
    csv_dir_fdh = init['csv_dir'] + 'fast/hourly/'

    # create target directories if necessary
    if not os.path.exists(nc_dir_fdd):
        os.makedirs(nc_dir_fdd)
    if not os.path.exists(csv_dir_fdd):
        os.makedirs(csv_dir_fdd)
    if not os.path.exists(nc_dir_fdh):
        os.makedirs(nc_dir_fdh)
    if not os.path.exists(csv_dir_fdh):
        os.makedirs(csv_dir_fdh)


    # ---------------------------------------------------------------------------
    # Loop daily
    # ---------------------------------------------------------------------------
    # get names of .dat files
    sta_files = glob(init['dat_dir'] + 'fast/d*.dat')
    pool = Pool(4)
    pool.map(worker_daily, sta_files)
    pool.close() 
    pool.join()

    # ---------------------------------------------------------------------------
    # Loop hourly
    # ---------------------------------------------------------------------------
    # get names of .dat files
    sta_files = glob(init['dat_dir'] + 'fast/h*.dat')
    pool = Pool(4)
    pool.map(worker_hourly, sta_files)
    pool.close()
    pool.join()

    # list stations not in the IOC SSC
    meta.not_in_SSC()

    # write meta data to json file
    meta.write_json()

# ---------------------------------------------------------------------------



