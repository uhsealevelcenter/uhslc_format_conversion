import os
from glob import glob

import readwrite

# ---------------------------------------------------------------------------

# directory containing the rqds and fast directories of .dat files
dat_dir = '../data/dat/'

# target directories for netcdf and csv station files
nc_dir = '../data/netcdf/'
csv_dir = '../data/csv/'

# target directories for bulk files; create if necessary
bulk_dir = nc_dir + 'bulk/'
if not os.path.exists(bulk_dir):
    os.makedirs(bulk_dir)

# reference time for netcdf
t_ref_str = '1800-01-01 00:00:00'

# create metdata container
meta = readwrite.Metadata()

# ---------------------------------------------------------------------------
# RESEARCH QUALITY
# ---------------------------------------------------------------------------

# names of basin divisions in the RQ data set
basins = ['atlantic', 'pacific', 'indian']

# ---------------------------------------------------------------------------

for b in basins:

    # -----------------------------------------------------------------------
    # DAILY

    # target directories for basin hourly files
    nc_dir_bd = nc_dir + 'rqds/' + b + '/daily/'
    csv_dir_bd = csv_dir + 'rqds/' + b + '/daily/'

    # create target directories if necessary
    if not os.path.exists(nc_dir_bd):
        os.makedirs(nc_dir_bd)
    if not os.path.exists(csv_dir_bd):
        os.makedirs(csv_dir_bd)

    # get names of .dat files
    sta_files = glob(dat_dir + 'rqds/' + b + '/daily/*.dat')

    # initialize bulk file
    blk = readwrite.BulkDailyRQ(bulk_dir, b, t_ref_str)
    blk.init_netcdf(len(sta_files))

    # loop over daily .dat files
    for idx, f in enumerate(sta_files):

        sta = readwrite.StationDailyRQ()

        try:
            sta.dat_read(f, meta)
            if sta.uhslc_id.data: # protection if .dat file is empty
                sta.trim()
                meta.update(sta)
                sta.write_netcdf(nc_dir_bd, t_ref_str)
                sta.write_csv(csv_dir_bd)
                blk.write_sta(sta, idx)
        except Exception as e:
            msg = 'While processing ' + str(f) + ':\n' + str(e)
            print(msg)

    print('rqds:' + b + ':daily complete')

    # -----------------------------------------------------------------------
    # HOURLY

    # target directories for basin hourly files
    nc_dir_bh = nc_dir + 'rqds/' + b + '/hourly/'
    csv_dir_bh = csv_dir + 'rqds/' + b + '/hourly/'

    # create target directories if necessary
    if not os.path.exists(nc_dir_bh):
        os.makedirs(nc_dir_bh)
    if not os.path.exists(csv_dir_bh):
        os.makedirs(csv_dir_bh)

    # get directories with .dat files for each station
    sta_dir = glob(dat_dir + 'rqds/' + b + '/hourly/*/')

    # initialize bulk file
    blk = readwrite.BulkHourlyRQ(bulk_dir, b, t_ref_str)
    blk.init_netcdf(len(sta_dir))

    # read and the station .dat files and write new formats
    for idx, d in enumerate(sta_dir):

        # aggregate data from .dat files for this station
        sta_files = glob(d + '*.dat')
        sta = readwrite.StationHourlyRQ()

        try:
            for f in sta_files:
                sta.dat_read_append(f, meta)
            if sta.uhslc_id.data: # protection if .dat file is empty
                sta.trim()
                meta.update(sta)
                sta.write_netcdf(nc_dir_bh, t_ref_str)
                sta.write_csv(csv_dir_bh)
                blk.write_sta(sta, idx)
        except Exception as e:
            msg = 'While processing ' + str(f) + ':\n' + str(e)
            print(msg)

    print('rqds:' + b + ':hourly complete')
    
# ---------------------------------------------------------------------------
# FAST DELIVERY
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# DAILY 

# target directories for daily FD files
nc_dir_fdd = nc_dir + 'fast/daily/'
csv_dir_fdd = csv_dir + 'fast/daily/'

# create target directories if necessary
if not os.path.exists(nc_dir_fdd):
    os.makedirs(nc_dir_fdd)
if not os.path.exists(csv_dir_fdd):
    os.makedirs(csv_dir_fdd)

# get names of .dat files
sta_files = glob(dat_dir + 'fast/d*.dat')
    
# initialize bulk file
blk = readwrite.BulkDailyFD(bulk_dir, t_ref_str)
blk.init_netcdf(len(sta_files))

# loop over daily .dat files
for idx, f in enumerate(sta_files):

    sta = readwrite.StationDailyFD()

    try:
        sta.dat_read(f, meta)
        if sta.uhslc_id.data: # protection if .dat file is empty
            sta.trim()
            meta.update(sta)
            sta.write_netcdf(nc_dir_fdd, t_ref_str)
            sta.write_csv(csv_dir_fdd)
            blk.write_sta(sta, idx)
    except Exception as e:
        msg = 'While processing ' + str(f) + ':\n' + str(e)
        print(msg)

print('fast:daily complete')

# ---------------------------------------------------------------------------
# HOURLY

# target directories for hourly FD files
nc_dir_fdh = nc_dir + 'fast/hourly/'
csv_dir_fdh = csv_dir + 'fast/hourly/'

# create target directories if necessary
if not os.path.exists(nc_dir_fdh):
    os.makedirs(nc_dir_fdh)
if not os.path.exists(csv_dir_fdh):
    os.makedirs(csv_dir_fdh)

# get names of .dat files
sta_files = glob(dat_dir + 'fast/h*.dat')

# initialize bulk file
blk = readwrite.BulkHourlyFD(bulk_dir, t_ref_str)
blk.init_netcdf(len(sta_files))

# loop over hourly .dat files
for idx, f in enumerate(sta_files):

    sta = readwrite.StationHourlyFD()

    try:
        sta.dat_read(f, meta)
        if sta.uhslc_id.data: # protection if .dat file is empty
            sta.trim()
            meta.update(sta)
            sta.write_netcdf(nc_dir_fdh, t_ref_str)
            sta.write_csv(csv_dir_fdh)
            blk.write_sta(sta, idx)
    except Exception as e:
        msg = 'While processing ' + str(f) + ':\n' + str(e)
        print(msg)

print('fast:hourly complete')

# ---------------------------------------------------------------------------  
    
    
    
    
    
    
    
    

