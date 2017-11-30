# ---------------------------------------------------------------------------

import os
import numpy as np
import datetime as dt
import netCDF4, urllib, xmltodict, json, time
from collections import OrderedDict
from unidecode import unidecode

# ---------------------------------------------------------------------------

def conversion_setup():
    
    init = {
    
        # directory containing the rqds and fast directories of .dat files
        'dat_dir' : 'data/dat/',
        
        # target directories for netcdf and csv station files
        'nc_dir' : 'data/netcdf/',
        'csv_dir' : 'data/csv/',
        
        # reference time for netcdf
        't_ref_str' : '1800-01-01 00:00:00'
    
    }
    
    return init

# ---------------------------------------------------------------------------

class StationVariable(object):

    def __init__(self):
        self.data = []
        self.dimensions = ()
        self.nc_format = ''
        self.fill_value = None
        self.attributes = OrderedDict()

# ---------------------------------------------------------------------------

class ReadWriteObj(object):

    def __init__(self):

        self.attributes = OrderedDict()
        self.attributes['ncei_template_version'] = \
            'NCEI_NetCDF_TimeSeries_Orthogonal_Template_v2.0'
        self.attributes['featureType'] = 'timeSeries'
        self.attributes['Conventions'] = 'CF-1.6, ACDD-1.3'
        self.attributes['date_created'] = \
            time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        self.attributes['publisher_name'] = \
            'University of Hawaii Sea Level Center (UHSLC)'
        self.attributes['publisher_email'] = \
            'philiprt@hawaii.edu, markm@soest.hawaii.edu'
        self.attributes['publisher_url'] = 'http://uhslc.soest.hawaii.edu'

        self.sea_level = StationVariable()
        self.sea_level.dimensions = ('record_id', 'time')
        self.sea_level.nc_format = 'i2'
        self.sea_level.fill_value = -32767
        self.sea_level.attributes['long_name'] = 'relative sea level'
        self.sea_level.attributes['units'] = 'millimeters'
        self.sea_level.attributes['source'] = 'in situ tide gauge water ' \
            + 'level observations'
        self.sea_level.attributes['platform'] = 'station_name, ' \
            + 'station_country, station_country_code, uhslc_id, gloss_id, ' \
            + 'ssc_id'

        self.time = StationVariable()
        self.time.dimensions = ('time',)
        self.time.nc_format = 'f8'
        self.time.attributes['long_name'] = 'time'
        self.time.attributes['axis'] = 'T'
        self.time.pytime = []

        self.lat = StationVariable()
        self.lat.dimensions = ('record_id',)
        self.lat.nc_format = 'f4'
        self.lat.attributes['standard_name'] = 'latitude'
        self.lat.attributes['units'] = 'degrees_north'
        self.lat.attributes['axis'] = 'Y'
        self.lat.attributes['valid_min'] = -90
        self.lat.attributes['valid_max'] = 90

        self.lon = StationVariable()
        self.lon.dimensions = ('record_id',)
        self.lon.nc_format = 'f4'
        self.lon.attributes['standard_name'] = 'longitude'
        self.lon.attributes['units'] = 'degrees_east'
        self.lon.attributes['axis'] = 'X'
        self.lon.attributes['valid_min'] = 0
        self.lon.attributes['valid_max'] = 360

        self.station_name = StationVariable()
        self.station_name.dimensions = ('record_id', 'nameMaxLength')
        self.station_name.nc_format = 'S1'
        self.station_name.attributes['long_name'] = 'station name'

        self.station_country = StationVariable()
        self.station_country.dimensions = ('record_id', 'countryMaxLength')
        self.station_country.nc_format = 'S1'
        self.station_country.attributes['long_name'] = 'station country ' \
            + '(ISO 3166-1)'

        self.station_country_code = StationVariable()
        self.station_country_code.dimensions = ('record_id',)
        self.station_country_code.nc_format = 'i2'
        self.station_country_code.fill_value = 0
        self.station_country_code.attributes['long_name'] = 'station ' \
            + 'country code (ISO 3166-1 numeric)'
        self.station_country_code.attributes['comment'] = 'These are ' \
            + '3-digit country codes (e.g., 003) stored as integers.'
        
        self.record_id = StationVariable()
        self.record_id.dimensions = ('record_id',)
        self.record_id.nc_format = 'i2'
        self.record_id.attributes['long_name'] = 'unique identifier ' \
            + 'for each record (i.e., station and version) in the database'
        
        self.uhslc_id = StationVariable()
        self.uhslc_id.dimensions = ('record_id',)
        self.uhslc_id.nc_format = 'i2'
        self.uhslc_id.attributes['long_name'] = 'unique station ID number ' \
            + 'used by the University of Hawaii Sea Level Center (UHSLC)'

        self.gloss_id = StationVariable()
        self.gloss_id.dimensions = ('record_id',)
        self.gloss_id.nc_format = 'i2'
        self.gloss_id.fill_value = 0
        self.gloss_id.attributes['long_name'] = 'unique station ID number ' \
            + 'used by the WMO/IOC Global Sea Level Observing System (GLOSS)'

        self.ssc_id = StationVariable()
        self.ssc_id.dimensions = ('record_id', 'sscMaxLength')
        self.ssc_id.nc_format = 'S1'
        self.ssc_id.attributes['long_name'] = 'unique station ID code in ' \
            + 'the Sealevel Station Catalog (SSC) produced by the WMO/IOC ' \
            + 'Sea Level Monitoring Facility (VLIZ)'
        self.ssc_id.attributes['comment'] = 'Note that SSC IDs vary in ' \
            + 'length. The IDs are padded with space characters to ' \
            + 'produce the retangular character matrix provided here.'

    def init_as_RQ(self, res):

        self.attributes['summary'] = 'The Joint Archive for Sea Level (JASL) Research Quality Data Set (RQDS) is a collaboration between the University of Hawaii Sea Level Center (UHSLC) and the World Data Center for Oceanography of the National Centers for Environmental Information (NCEI), National Oceanic and Atmospheric Administration (NOAA). The objective of the JASL RQDS is to assemble a well-documented, quality-controlled archive of hourly and daily sea level values that is appropriate for scientific research applications. The JASL RQDS is the largest global collection of quality-controlled hourly sea level data, and ongoing efforts seek to acquire new sites and uncover historic records as available.'
        self.attributes['processing_level'] = 'The JASL receives hourly data from regional and national sea level networks operating world-wide. JASL RQDS data undergo a level 1 quality assessment focused on variability (e.g., unit and timing evaluation, outlier detection, combination of multiple channels into a primary channel, etc.) followed by a level 2 quality assessment focused on datum stability (e.g., tide gauge datum evaluation, assessment of level ties to tide gauge benchmarks, comparison with nearby stations, etc.).'
        self.attributes['acknowledgment'] = 'The JASL/UHSLC Research Quality Data Set is supported by the National Oceanic and Atmospheric Administration (NOAA) via the National Centers for Environmental Information (NCEI) and the Office of Climate Observations (OCO).'

        self.version = StationVariable()
        self.version.dimensions = ('record_id',)
        self.version.nc_format = 'S1'
        self.version.attributes['long_name'] = 'station version'
        self.version.attributes['comment'] = 'The station version is a '\
            + 'letter from A to Z differentiating segments of a station ' \
            + 'record that cannot be linked to a common benchmark.'

        self.decimation_method = StationVariable()
        self.decimation_method.dimensions = ('record_id',)
        self.decimation_method.nc_format = 'i2'
        self.decimation_method.attributes['long_name'] = 'decimation method'
        self.decimation_method.attributes['flag_values'] = '1, 2, 3, 4'
        self.decimation_method.attributes['flag_meanings'] = 'filtered, ' \
            + 'average, spot readings, other'

        self.reference_offset = StationVariable()
        self.reference_offset.dimensions = ('record_id',)
        self.reference_offset.nc_format = 'i2'
        self.reference_offset.attributes['units'] = 'millimeters'
        self.reference_offset.attributes['long_name'] = 'reference offset'
        self.reference_offset.attributes['comment'] = 'This is a constant ' \
            + 'offset to be added to each data value to make the data ' \
            + 'relative to the tide staff zero or primary datum.'

        self.reference_code = StationVariable()
        self.reference_code.dimensions = ('record_id',)
        self.reference_code.nc_format = 'S1'
        self.reference_code.attributes['long_name'] = 'reference code'
        self.reference_code.attributes['flag_values'] = 'R, X'
        self.reference_code.attributes['flag_meanings'] = 'data referenced ' \
            + 'to datum, data not referenced to datum'

        self.attributes['title'] = \
            'JASL/UHSLC Research Quality Tide Gauge Data (' + res + ')'
        self.attributes.move_to_end('title', last=False)
        self.res_flag = res[0]

    def init_as_FD(self, res):

        self.attributes['summary'] = 'The UHSLC assembles and distributes the Fast Delivery (FD) dataset of hourly- and daily-averaged tide gauge water-level observations. Tide gauge operators, or data creators, provide FD data to UHSLC after a level 1 quality assessment (see processing_level attribute). The UHSLC provides an independent quality assessment of the time series and makes FD data available within 4-6 weeks of collection. This is a "fast" turnaround time compared to Research Quality (RQ) data, which are available on an annual cycle after a level 2 quality assessment. RQ data replace FD data in the data stream as the former becomes available. This file contains hybrid time series composed of RQ data when available with FD data appended to the end of each RQ series.'
        self.attributes['processing_level'] = 'Fast Delivery (FD) data undergo a level 1 quality assessment (e.g., unit and timing evaluation, outlier detection, combination of multiple channels into a primary channel, etc.). In this file, FD data are appended to Research Quality (RQ) data that have received a level 2 quality assessment (e.g., tide gauge datum evaluation, assessment of level ties to tide gauge benchmarks, comparison with nearby stations, etc.).'
        self.attributes['acknowledgment'] = 'The UHSLC Fast Delivery database is supported by the National Oceanic and Atmospheric Administration (NOAA) Office of Climate Observations (OCO).'

        self.last_rq_date = StationVariable()
        self.last_rq_date.dimensions = ('record_id',)
        self.last_rq_date.nc_format = 'f8'
        self.last_rq_date.fill_value = 0
        self.last_rq_date.attributes['long_name'] = 'date of last ' \
            + 'Research Quality sea level value'
        self.last_rq_date.attributes['comment'] = 'Values in last_rq_date correspond to an identical value in the time vector. Dates less than or equal to last_rq_date for a given station correspond to Research Quality (RQ) data. Dates after last_rq_date correspond to Fast Delivery (FD) data. Missing values indicate no RQ data for a station.'
        self.last_rq_date.pytime = []

        self.attributes['title'] = \
            'UHSLC Fast Delivery Tide Gauge Data (' + res + ')'
        self.attributes.move_to_end('title', last=False)
        self.res_flag = res[0]

# ---------------------------------------------------------------------------

class Station(ReadWriteObj):

    def __init__(self):
        ReadWriteObj.__init__(self)

    def trim(self):

        # first sea level data value
        idx1 = None
        for k, val in enumerate(self.sea_level.data):
            if val != self.sea_level.fill_value:
                idx1 = k
                break

        # last sea level data value
        idx2 = None
        for k, val in enumerate(self.sea_level.data[::-1]):
            if val != self.sea_level.fill_value:
                idx2 = len(self.sea_level.data) - k - 1
                break

        # trim all variables with time dimension to data span
        nc_vars = vars(self)
        for v in list(nc_vars):
            if isinstance(nc_vars[v], StationVariable) and \
                'time' in nc_vars[v].dimensions and v != 'time':
                    if idx1 is not None:
                        nc_vars[v].data = nc_vars[v].data[idx1:idx2+1]
                    else:
                        nc_vars[v].data = []

        # trim python datenumbers
        if idx1 is not None:
            self.time.pytime = self.time.pytime[idx1:idx2+1]  
        else:          
            self.time.pytime = []

    def write_netcdf(self, nc_dir, t_ref_str):

        # get list of variables to be written to netcdf
        nc_vars = vars(self)
        v_all = [v for v in list(nc_vars)
            if isinstance(nc_vars[v], StationVariable)]

        # influence the order of variables written to the netcdf file
        v_core = ['sea_level', 'time', 'lat', 'lon', 'station_name',
            'station_country', 'station_country_code', 'record_id', 'uhslc_id',
            'version', 'gloss_id', 'ssc_id']
        v_list = [v_all.pop(v_all.index(v)) for v in v_core if v in v_all]
        v_list.extend(sorted(v_all))

        # netcdf filename
        if 'version' in v_list:
            vrsn = self.version.data.lower()
        else:
            vrsn = ''
        fname = nc_dir + self.res_flag \
            + str(self.uhslc_id.data).zfill(3) + vrsn + '.nc'
        if os.path.exists(fname):
            os.remove(fname)

        # create time vector relative to reference time
        self.time.t_ref = dt.datetime.strptime(t_ref_str,
            '%Y-%m-%d %H:%M:%S')
        self.time.data.extend(
            [round((t - self.time.t_ref).total_seconds()/(60*60*24)
                - self.time.gmt_offset, 6) for t in self.time.pytime])
        self.time.attributes['units'] = 'days since ' + t_ref_str

        if 'last_rq_date' in v_list:
            if self.last_rq_date.pytime == dt.datetime(1,1,1,0,0,0):
                self.last_rq_date.data = 0
            else:
                self.last_rq_date.data = round((self.last_rq_date.pytime
                    - self.time.t_ref).total_seconds()/(60*60*24) \
                    - self.time.gmt_offset, 6)
                self.last_rq_date.attributes['units'] = \
                    'days since ' + t_ref_str

        # open netcdf file
        rootgrp = netCDF4.Dataset(fname, mode='w', clobber=True,
            format='NETCDF4_CLASSIC')

        # set global attributes
        rootgrp.setncatts(self.attributes)

        # create dimensions
        time = rootgrp.createDimension('time', None)
        record_id = rootgrp.createDimension('record_id', 1)
        nameMaxLength = rootgrp.createDimension('nameMaxLength',
            len(self.station_name.data))
        countryMaxLength = rootgrp.createDimension('countryMaxLength',
            len(self.station_country.data))
        sscMaxLength = rootgrp.createDimension('sscMaxLength',
            len(self.ssc_id.data))

        # write variables
        for v in v_list:

            if nc_vars[v].fill_value is not None:
                ncv = rootgrp.createVariable(v, nc_vars[v].nc_format,
                    nc_vars[v].dimensions,
                    fill_value=nc_vars[v].fill_value)
            else:
                ncv = rootgrp.createVariable(v, nc_vars[v].nc_format,
                    nc_vars[v].dimensions)

            ncv.setncatts(nc_vars[v].attributes)

            # need 2D arrays for insertion into two dimensions
            if len(nc_vars[v].dimensions) == 2:
                # strings
                if nc_vars[v].nc_format == 'S1':
                    fs = 'S' + str(rootgrp.dimensions[
                        nc_vars[v].dimensions[1]].size)
                    ncv[:,:] = netCDF4.stringtochar(
                        np.array(unidecode(nc_vars[v].data),fs))
                # numeric
                else:
                    ncv[:,:] = [nc_vars[v].data]
            # 1D
            else:
                ncv[:] = nc_vars[v].data

        rootgrp.close()


    def write_csv(self, csv_dir):

        if self.res_flag == 'h':
            fstr = '%Y,%-m,%-d,%-H,'
        elif self.res_flag == 'd':
            fstr = '%Y,%-m,%-d,'

        if 'version' in list(vars(self)):
            vrsn = self.version.data.lower()
        else:
            vrsn = ''

        fname = csv_dir + self.res_flag + str(self.uhslc_id.data).zfill(3) \
            + vrsn + '.csv'
        if os.path.exists(fname):
            os.remove(fname)

        with open(fname, 'w') as f:
            for t, h in zip(self.time.pytime, self.sea_level.data):
                line = t.strftime(fstr) + str(h) + '\n'
                f.write(line)

# ---------------------------------------------------------------------------

class StationHourlyRQ(Station):

    def __init__(self):
        Station.__init__(self)
        self.init_as_RQ('hourly')

    def dat_read_append(self, fname, meta):

        with open(fname, 'r') as f:

            hdr = f.readline() # read first line

            if not hdr or hdr == '\n': # file empty
                print('!!File ' + fname + ' is empty!!')
                return

            uid = int(hdr[0:3])
            self.uhslc_id.data = uid
            self.version.data = hdr[3]
            
            self.record_id.data = int(str(self.uhslc_id.data) + \
                str(ord(self.version.data)-64))

            self.station_name.data = reformat_name_str(hdr[5:24])
            self.station_name.data = self.station_name.data.strip()

            self.station_country.data = hdr[24:44]
            self.station_country.data = self.station_country.data.strip()

            self.lat.data = int(hdr[49:51]) \
                + round(int(hdr[51:54])/600, 3)
            if hdr[54] == 'S':
                self.lat.data = -self.lat.data
            self.lon.data = int(hdr[56:59]) \
                + round(int(hdr[59:62])/600, 3)
            if hdr[62] == 'W':
                self.lon.data = 360 - self.lon.data
            if hdr[69] == '\\':
                self.decimation_method.data = None
            else:
                self.decimation_method.data = int(hdr[69])
            self.reference_offset.data = int(hdr[71:76])
            self.reference_code.data = hdr[76]
            self.time.gmt_offset = int(hdr[64:68])/240 # in days

            uidx = None
            for k, st in enumerate(meta.data['features']): 
                if st['properties']['uhslc_id'] == uid:
                    uidx = k
                    this_sta = meta.data['features'][uidx]
            
            if uidx is not None:
                self.station_country.data = this_sta['properties']['country']
                self.station_country_code.data \
                    = this_sta['properties']['country_code']
                self.gloss_id.data = this_sta['properties']['gloss_id']
                self.ssc_id.data = this_sta['properties']['ssc_id']
            else:              
                self.station_country_code.data = 0
                self.gloss_id.data = 0
                self.ssc_id.data = 'none'

            # loop over each line of data
            for line in f:

                if line[15] == ' ': line = line[:15] + '0' + line[16:]
                if line[17] == ' ': line = line[:17] + '0' + line[18:]

                lnt = line[11:20]
                t0 = dt.datetime.strptime(lnt[0:-1], '%Y%m%d') \
                    + (int(lnt[-1]) - 1)*dt.timedelta(hours=12) \
                    + dt.timedelta(minutes=30)
                self.time.pytime.extend(
                    [t0 + h*dt.timedelta(hours=1) for h in np.arange(12)])

                lndat = line[20:]
                spl = [lndat[d:d+5] for d in np.arange(0, 56, 5)]
                fv = self.sea_level.fill_value
                self.sea_level.data.extend(
                    [int(d) if int(d) != 9999 else fv for d in spl])

# ---------------------------------------------------------------------------

class StationDailyRQ(Station):

    def __init__(self):
        Station.__init__(self)
        self.init_as_RQ('daily')

    def dat_read(self, fname, meta):

        with open(fname, 'r') as f:

            # get meta data in header
            hdr = f.readline() # read first line

            if not hdr or hdr == '\n': # file empty
                print('!!File ' + fname + ' is empty!!' + ' '*50)
                return

            uid = int(hdr[0:3])
            self.uhslc_id.data = uid
            self.version.data = hdr[3]
            
            self.record_id.data = int(str(self.uhslc_id.data) + \
                str(ord(self.version.data)-64))

            self.station_name.data = reformat_name_str(hdr[5:24])
            self.station_name.data = self.station_name.data.strip()

            self.station_country.data = hdr[24:44]
            self.station_country.data = self.station_country.data.strip()

            self.lat.data = int(hdr[54:56]) \
                + round(int(hdr[56:59])/600, 3)
            if hdr[59] == 'S':
                self.lat.data = -self.lat.data
            self.lon.data = int(hdr[61:64]) \
                + round(int(hdr[64:67])/600, 3)
            if hdr[67] == 'W':
                self.lon.data = 360 - self.lon.data
            self.decimation_method.data = int(hdr[69])
            self.reference_offset.data = int(hdr[71:76])
            self.reference_code.data = hdr[76]
            self.time.gmt_offset = 0 # in days
            
            uidx = None
            for k, st in enumerate(meta.data['features']): 
                if st['properties']['uhslc_id'] == uid:
                    uidx = k
                    this_sta = meta.data['features'][uidx]
            
            if uidx is not None:
                self.station_country.data = this_sta['properties']['country']
                self.station_country_code.data \
                    = this_sta['properties']['country_code']
                self.gloss_id.data = this_sta['properties']['gloss_id']
                self.ssc_id.data = this_sta['properties']['ssc_id']
            else:
                self.station_country_code.data = 0
                self.gloss_id.data = 0
                self.ssc_id.data = 'none'
            
            # loop over each line of data
            for line in f:

                t0 = dt.datetime(int(line[10:14]),1,1,12,0) \
                    + (int(line[15:18]) - 1)*dt.timedelta(days=1)
                tline = [t0 + h*dt.timedelta(days=1) for h in np.arange(12)]
                hline = [int(line[k:k+5]) for k in 20+5*np.arange(12)]

                for t, d in zip(tline, hline):
                    if d != -9999:
                        self.time.pytime.extend([t])
                        if d == 9999:
                            self.sea_level.data.extend(
                                [self.sea_level.fill_value])
                        else:
                            self.sea_level.data.extend([d])

# ---------------------------------------------------------------------------

class StationHourlyFD(Station):

    def __init__(self):
        Station.__init__(self)
        self.init_as_FD('hourly')

    def dat_read(self, fname, meta):

        with open(fname, 'r') as f:

            # get id from header and link to other meta
            hdr = f.readline() # read first line

            if not hdr or hdr == '\n': # file empty
                print('!!File ' + fname + ' is empty!!')
                return

            uid = int(hdr[0:3])
            self.uhslc_id.data = uid
            
            self.record_id.data = int(str(self.uhslc_id.data) + '0')

            self.station_name.data = hdr[3:11]
            self.station_name.data = self.station_name.data.strip()

            self.lat.data = int(hdr[21:23]) \
                + round(float(hdr[24:28].strip())/600, 3)
            if hdr[28] == 'S':
                self.lat.data = -self.lat.data
            self.lon.data = int(hdr[36:39]) \
                + round(float(hdr[40:44].strip())/600, 3)
            if hdr[44] == 'W':
                self.lon.data = 360 - self.lon.data
            self.time.gmt_offset = 0

            uidx = None
            for k, st in enumerate(meta.data['features']): 
                if st['properties']['uhslc_id'] == uid:
                    uidx = k
                    this_sta = meta.data['features'][uidx]
            
            if uidx is not None:
                self.station_name.data = this_sta['properties']['name']
                self.station_country.data = this_sta['properties']['country']
                self.station_country_code.data \
                    = this_sta['properties']['country_code']
                self.gloss_id.data = this_sta['properties']['gloss_id']
                self.ssc_id.data = this_sta['properties']['ssc_id']
            else:
                self.station_country.data = 'Unknown'
                self.station_country_code.data = 0
                self.ssc_id.data = 'none'
                self.gloss_id.data = 0

            # loop over each line and read data
            for line in f:

                if line[17:20] == 'LAT': continue

                if line[15] == ' ': line = line[:15] + '0' + line[16:]
                if line[17] == ' ': line = line[:17] + '0' + line[18:]

                t0 = dt.datetime.strptime(line[11:19], '%Y%m%d') \
                    + (int(line[19]) - 1)*dt.timedelta(hours=12) \
                    + dt.timedelta(minutes=30)
                self.time.pytime.extend(
                    [t0 + h*dt.timedelta(hours=1) for h in np.arange(12)])

                self.sea_level.data.extend([int(line[k:k+5]) \
                    if int(line[k:k+5]) != 9999 else self.sea_level.fill_value
                    for k in 20+5*np.arange(12)])
            
            # get last time in the data that is RQ
            self.last_rq_date.pytime = dt.datetime(1,1,1,0,0,0)
            if uidx is not None:
                if this_sta['properties']['rq_span']['latest'] is not None:
                    lrq = dt.datetime.strptime(
                        this_sta['properties']['rq_span']['latest'],
                            '%Y-%m-%d')
                    for k, t in enumerate(self.time.pytime):
                        if t >= lrq + dt.timedelta(days=1):
                            self.last_rq_date.pytime = self.time.pytime[k-1]
                            break

# ---------------------------------------------------------------------------

class StationDailyFD(Station):

    def __init__(self):
        Station.__init__(self)
        self.init_as_FD('daily')

    def dat_read(self, fname, meta):

        with open(fname, 'r') as f:

            # get id from header and link to other meta
            hdr = f.readline() # read first line

            if not hdr or hdr == '\n': # file empty
                print('!!File ' + fname + ' is empty!!')
                return

            uid = int(hdr[0:3])
            self.uhslc_id.data = uid

            self.record_id.data = int(str(self.uhslc_id.data) + '0')

            self.station_name.data = hdr[3:11]
            self.station_name.data = self.station_name.data.strip()

            self.lat.data = int(hdr[21:23]) \
                + round(float(hdr[24:28].strip())/600, 3)
            if hdr[28] == 'S':
                self.lat.data = -self.lat.data
            self.lon.data = int(hdr[36:39]) \
                + round(float(hdr[40:44].strip())/600, 3)
            if hdr[44] == 'W':
                self.lon.data = 360 - self.lon.data
            self.time.gmt_offset = 0

            uidx = None
            for k, st in enumerate(meta.data['features']): 
                if st['properties']['uhslc_id'] == uid:
                    uidx = k
                    this_sta = meta.data['features'][uidx]
            
            if uidx is not None:
                self.station_name.data = this_sta['properties']['name']
                self.station_country.data = this_sta['properties']['country']
                self.station_country_code.data \
                    = this_sta['properties']['country_code']
                self.gloss_id.data = this_sta['properties']['gloss_id']
                self.ssc_id.data = this_sta['properties']['ssc_id']
            else:
                self.station_country.data = 'Unknown'
                self.station_country_code.data = 0
                self.ssc_id.data = 'none'
                self.gloss_id.data = 0

            # loop over each line and read data
            for line in f:

                data = line[19:-1]
                for k, c in enumerate(data[::-1]):
                    if c != ' ':
                        idx = len(data) - k
                        break

                data = data[0:idx]
                n_days = int(len(data)/5)

                t0 = dt.datetime(int(line[11:15]),int(line[15:17]),1,12,0)

                self.time.pytime.extend([t0 + ((int(line[17])-1)*11 + d)\
                    *dt.timedelta(days=1) for d in np.arange(n_days)])

                self.sea_level.data.extend([int(data[k:k+5]) \
                    if int(data[k:k+5]) != 9999 else self.sea_level.fill_value
                    for k in 5*np.arange(n_days)])
            
            # get last time in the data that is RQ
            self.last_rq_date.pytime = dt.datetime(1,1,1,0,0,0)
            if uidx is not None:
                if this_sta['properties']['rq_span']['latest'] is not None:
                    lrq = dt.datetime.strptime(
                        this_sta['properties']['rq_span']['latest'],
                            '%Y-%m-%d')
                    for k, t in enumerate(self.time.pytime):
                        if t >= lrq + dt.timedelta(days=1):
                            self.last_rq_date.pytime = self.time.pytime[k-1]
                            break

# ---------------------------------------------------------------------------

class Metadata(object):

    def __init__(self):

        # get available meta data from IOC site
        req = urllib.request.urlopen(
            'http://www.ioc-sealevelmonitoring.org/ssc/service.php?format=json')
        ioc_meta = json.loads(req.read().decode(
            req.info().get_param('charset') or 'utf-8'))

        # load dictionary of ISO country codes
        with open('./ISO_3166_codes/iso_3116.json', 'r') as f:
            self.iso_a2_lookup = json.load(f)

        # load existing meta data if possible; otherwise initialize
        if os.path.exists('./meta.geojson'):
            with open('./meta.geojson') as f:
                self.data = json.load(f, object_pairs_hook=OrderedDict)
        else:
            self.data = OrderedDict({
                'type': 'FeatureCollection',
                'features': []
            })

        # use ioc meta data to update or initialize stations in list
        for sta in ioc_meta:

            if 'uhslc' in sta:

                if isinstance(sta['uhslc'], str):
                    uhslc_id = [int(sta['uhslc'])]
                else:
                    uhslc_id = [int(u) for u in sta['uhslc']]

                if not isinstance(sta['name'], str):
                    sta['name'] = sta['name'][0]

                if 'gloss' in sta:
                    gid = int(sta['gloss'])
                else: gid = 0

                iso_a2 = sta['country']
                cnm = self.iso_a2_lookup[iso_a2]['name']
                ccd = self.iso_a2_lookup[iso_a2]['numeric']

                for uid in uhslc_id:
                    
                    uidx = None
                    
                    # update some fields if already in meta list
                    for k, st in enumerate(self.data['features']): 
                        if st['properties']['uhslc_id'] == uid:
                            uidx = k                            
                            self.data['features'][uidx]['properties']\
                                ['ssc_id'] = sta['ssc_id'][4:]
                            self.data['features'][uidx]['properties']\
                                ['gloss_id'] = gid
                            self.data['features'][uidx]['properties']\
                                ['country'] = cnm
                            self.data['features'][uidx]['properties']\
                                ['country_code'] = ccd
                    
                    # create new station in list if not present        
                    if uidx is None:
                        self.data['features'].append(
                            {
                                'type': 'Feature',
                                'geometry': {
                                    'type': 'Point',
                                    'coordinates': [None, None]
                                },
                                'properties': {
                                    'name': sta['name'],
                                    'uhslc_id': uid,
                                    'ssc_id': sta['ssc_id'][4:],
                                    'gloss_id': gid,
                                    'country': cnm,
                                    'country_code': ccd,
                                    'fd_span': {
                                        'oldest': None,
                                        'latest': None
                                    },
                                    'rq_span': {
                                        'oldest': None,
                                        'latest': None
                                    }
                                }
                            }
                        )
                        
    # ----------------------------------------------------------------------

    def update(self, sta):
        
        uidx = None
        for k, st in enumerate(self.data['features']): 
            if st['properties']['uhslc_id'] == sta.uhslc_id.data:
                uidx = k
        
        if uidx is None:
            self.data['features'].append(
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [sta.lon.data, sta.lat.data]
                    },
                    'properties': {
                        'name': sta.station_name.data,
                        'uhslc_id': sta.uhslc_id.data,
                        'ssc_id': sta.ssc_id.data,
                        'gloss_id': sta.gloss_id.data,
                        'country': sta.station_country.data,
                        'country_code': sta.station_country_code.data,
                        'fd_span': {
                            'oldest': None,
                            'latest': None
                        },
                        'rq_span': {
                            'oldest': None,
                            'latest': None
                        }
                    }
                }
            )
            uidx = len(self.data['features']) - 1
        
        # if daily RQ, update with dates of oldest/latest RQ data
        if isinstance(sta, StationDailyRQ):
            
            # prefer Pat's station name/lat/lon
            self.data['features'][uidx]\
                ['properties']['name'] = sta.station_name.data
            self.data['features'][uidx]\
                ['geometry']['coordinates'] = [sta.lon.data, sta.lat.data]
            
            oldest = \
                self.data['features'][uidx]['properties']['rq_span']['oldest']
            if (oldest is None or
                sta.time.pytime[0] < dt.datetime.strptime(oldest, '%Y-%m-%d')):
                self.data['features'][uidx]['properties']['rq_span']\
                    ['oldest'] = sta.time.pytime[0].strftime('%Y-%m-%d')

            latest = \
                self.data['features'][uidx]['properties']['rq_span']['latest']
            if (latest is None or
                sta.time.pytime[-1] > dt.datetime.strptime(latest, '%Y-%m-%d')):
                self.data['features'][uidx]['properties']['rq_span']\
                    ['latest'] = sta.time.pytime[-1].strftime('%Y-%m-%d')
            
        # if daily FD, update with dates of oldest/latest FD data
        if isinstance(sta, StationDailyFD):
            
            if self.data['features'][uidx]['geometry']['coordinates'] is None:
                self.data['features'][uidx]\
                    ['geometry']['coordinates'] = [sta.lon.data, sta.lat.data]
            
            oldest = \
                self.data['features'][uidx]['properties']['fd_span']['oldest']
            if (oldest is None or
                sta.time.pytime[0] < dt.datetime.strptime(oldest, '%Y-%m-%d')):
                self.data['features'][uidx]['properties']['fd_span']\
                    ['oldest'] = sta.time.pytime[0].strftime('%Y-%m-%d')

            latest = \
                self.data['features'][uidx]['properties']['fd_span']['latest']
            if (latest is None or
                sta.time.pytime[-1] > dt.datetime.strptime(latest, '%Y-%m-%d')):
                self.data['features'][uidx]['properties']['fd_span']\
                    ['latest'] = sta.time.pytime[-1].strftime('%Y-%m-%d')
                    
    # -----------------------------------------------------------------------
    
    def not_in_SSC(self):
        
        not_in = ''
        
        for sta in self.data['features']:
            if sta['properties']['ssc_id'] == 'none':
                not_in += str(sta['properties']['uhslc_id']) + ', '
        
        if not_in:
            print('\n**The following UHSLC IDs are not in the IOC SSC**')
            print(not_in[0:-2] + '\n')
    
    # -----------------------------------------------------------------------
                    
    def write_json(self):
                
        # sort stations in list by increasing uhslc id
        self.data['features'] = sorted(self.data['features'],
            key=lambda k: k['properties']['uhslc_id'])
        
        with open('./meta.geojson', 'w') as f:
            json.dump(self.data, f)

# ---------------------------------------------------------------------------

def reformat_name_str(name):

    if '-' in name:
        z = name.index('-')
        name = name[0:z] + name[z+2:]
    if ',' in name:
        z = name.index(',')
        if name[z+1] != ' ':
            name = name[0:z+1] + ' ' + name[z+1:]

    return name

# ---------------------------------------------------------------------------

# Make a progress bar for the loops
class ProgressBar:
    
    def __init__(self, total, description=None):
        
        self.total = total
        self.decimals = 1
        self.length = 50
        self.fill = '█'
        self.iteration = 0
        self.intervals = np.ceil(np.linspace(1, self.total, self.length))
        self.percent = np.linspace(0, 100, self.length+1)[1:].astype(int)
        
        unq, cnt = np.unique(self.intervals, return_counts=True)
        idx = np.array([np.where(self.intervals == u)[0][-1] for u in unq])
        self.intervals = self.intervals[idx]
        self.percent = self.percent[idx]
        self.cumcnt = np.cumsum(cnt)                
                
        if description: 
            print(description)
        print('\r|%s| 0%% complete' % (' '*self.length), end = '\r')
        
    def update(self):
        
        self.iteration += 1
        
        if self.iteration in self.intervals:
            prog = np.where(self.intervals == self.iteration)[0][-1]
            pctstr = str(self.percent[prog]) + '%'            
            bar = (self.fill * self.cumcnt[prog]
                + ' ' * (self.length - self.cumcnt[prog]))
            print('\r|%s| %s complete' % (bar, pctstr), end = '\r')
            if self.iteration == self.total:                 
                print() # blank line on completion
                
                
