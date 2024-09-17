# --------------------------------------------------------------------------- 
import time
import os
import json

if os.path.exists('./meta.geojson'):
    with open('./meta.geojson') as f:
        # meta = json.load(f, object_pairs_hook=OrderedDict)
        meta = json.load(f)

dat_dir = "/srv/htdocs/uhslc.soest.hawaii.edu/rqds"

s = meta['features']
length = len(s)

for stn in range(length):
#for stn in range(2):
    if s[stn]['properties']['rq_versions']:
        versions = list(sorted(s[stn]['properties']['rq_versions'].keys()))
    for v in range(len(versions)):
        vrsn = versions[v]

        rq_basin = s[stn]['properties']['rq_basin']

        if s[stn]['properties']['uhslc_id'] == 0:
            uhslc_id = ''
        else:
            uhslc_id = s[stn]['properties']['uhslc_id']
    
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

        if rq_oldest != '':

            rq_file = ("%s/%s/daily/d%03d%s.dat" % (dat_dir,rq_basin,uhslc_id,vrsn))

#            print("last modified: %s" % time.ctime(os.path.getmtime(rq_file)))
            rq_filetime = time.strftime("%Y %m %d",time.localtime(os.path.getmtime(rq_file)))

            begin = s[stn]['properties']['rq_versions'][vrsn]['begin']
            end = s[stn]['properties']['rq_versions'][vrsn]['end']
            print('%03d %s %s %s %s %s %s' % (uhslc_id, vrsn, begin[0:4], begin[5:7] ,end[0:4], end[5:7], rq_filetime))

