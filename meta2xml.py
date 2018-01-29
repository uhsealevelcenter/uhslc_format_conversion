# --------------------------------------------------------------------------- 
import dicttoxml


import os
import numpy as np
import datetime as dt
import netCDF4, urllib, xmltodict, json, time
from collections import OrderedDict
from unidecode import unidecode
from pprint import pprint

if os.path.exists('./meta.geojson'):
    with open('./meta.geojson') as f:
        # meta = json.load(f, object_pairs_hook=OrderedDict)
        meta = json.load(f)

s = meta['features']
length = len(s)
#print(length)

print('<?xml version="1.0" encoding="UTF-8"?>')
print('<stations>')

for stn in range(length):

    if s[stn]['properties']['uhslc_id'] == 0:
        uhslc_id = ''
    else:
        uhslc_id = s[stn]['properties']['uhslc_id']

    if s[stn]['properties']['gloss_id'] == 0:
        gloss_id = ''
    else:
        gloss_id = s[stn]['properties']['gloss_id']

    lat = s[stn]['geometry']['coordinates'][1]
    if lat == None:
        lat = 0
    elif lat >= 90:
        lat = lat-180

    lng = s[stn]['geometry']['coordinates'][0]
    if lng == None:
        lng = 0
    elif lng >= 180:
        lng = lng-360

    fd_oldest = s[stn]['properties']['fd_span']['oldest']
    if fd_oldest == None:
        fd_oldest = ''
    else: 
        fd_oldest = s[stn]['properties']['fd_span']['oldest']
    
    fd_latest = s[stn]['properties']['fd_span']['latest']
    if fd_latest == None:
        fd_latest = ''
    else: 
        fd_latest = s[stn]['properties']['fd_span']['latest']
    
    rq_oldest = s[stn]['properties']['rq_span']['oldest']
    if rq_oldest == None:
        rq_oldest = ''
    else: 
        rq_oldest = s[stn]['properties']['rq_span']['oldest']
    
    rq_latest = s[stn]['properties']['rq_span']['latest']
    if rq_latest == None:
        rq_latest = ''
    else: 
        rq_latest = s[stn]['properties']['rq_span']['latest']

    print('  <station>')
    if uhslc_id != '':
        print('    <uhslc_id>%s</uhslc_id>' % uhslc_id)
    else:
        # print('    <uhslc_id/>')
        print('    <uhslc_id></uhslc_id>')
    if gloss_id != '':
        print('    <gloss_id>%s</gloss_id>' % gloss_id)
    else:
        # print('    <gloss_id/>'/)
        print('    <gloss_id></gloss_id>')
    # print('    <name>%s</name>' % s[stn]['properties']['name'])
    print('    <name>%s</name>' % s[stn]['properties']['name'].replace("&","&amp;"))
    print('    <country>%s</country>' % s[stn]['properties']['country'])
    print('    <latitude>%.5f</latitude>' % lat)
    print('    <longitude>%.5f</longitude>' % lng)
    print('    <fast_delivery_data>')
    if fd_oldest != '':
        print('      <oldest>%s</oldest>' % fd_oldest)
        print('      <latest>%s</latest>' % fd_latest)
    else:
        # print('      <oldest/>')
        # print('      <latest/>')
        print('      <oldest></oldest>')
        print('      <latest></latest>')
    print('    </fast_delivery_data>')
    print('    <research_quality_data>')
    if rq_oldest != '':
        print('      <oldest>%s</oldest>' % rq_oldest)
        print('      <latest>%s</latest>' % rq_latest)
    else:
        # print('      <oldest/>')
        # print('      <latest/>')
        print('      <oldest></oldest>')
        print('      <latest></latest>')
    print('    </research_quality_data>')
    print('  </station>')

print('</stations>')

