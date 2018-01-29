# --------------------------------------------------------------------------- 
import os
import json

if os.path.exists('./meta.geojson'):
    with open('./meta.geojson') as f:
        # meta = json.load(f, object_pairs_hook=OrderedDict)
        meta = json.load(f)

s = meta['features']
length = len(s)

dat_dir = "http://uhslc.soest.hawaii.edu/rqds"
csv_dir = "http://uhslc.soest.hawaii.edu/data/csv/rqds"
nc_dir = "http://uhslc.soest.hawaii.edu/data/netcdf/rqds"
oldnc_dir = "http://uhslc.soest.hawaii.edu/data/nc"

print('    <table id="table" class="tablesorter">')
print('      <thead>')
print('         <tr>')
print('             <th><h3>UH&#35;</h3></th>')
print('             <th><h3>GLOSS&#35;</h3></th>')
print('             <th><h3>Version</h3></th>')
print('             <th><h3>Location</h3></th>')
print('             <th><h3>Country</h3></th>')
print('             <th><h3>Latitude</h3></th>')
print('             <th><h3>Longitude</h3></th>')
print('             <th><h3>Start</h3></th>')
print('             <th><h3>End</h3></th>')
print('             <th class="nosort"><h3>Data</h3></th>')
print('             <th class="nosort"><h3>CSV</h3></th>')
print('             <th class="nosort"><h3>NetCDF</h3></th>')
print('             <th class="nosort"><h3>OldNetCDF</h3></th>')
print('             <th class="nosort"><h3>Meta</h3></th>')
print('         </tr>')
print('       </thead>')
print('       <tbody>')
print('')

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
    
        if s[stn]['properties']['gloss_id'] == 0:
            gloss_id = ''
        else:
            gloss_id = s[stn]['properties']['gloss_id']
    
        lat = s[stn]['geometry']['coordinates'][1]
        if lat == None:
            lat = ''
        elif lat >= 90:
            lat = lat-180

        lng = s[stn]['geometry']['coordinates'][0]
        if lng == None:
            lng = ''
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

        if rq_oldest != '':

            print('           <tr id="uh%03d%s">' % (uhslc_id, vrsn))
            print('               <td>%03d</td>' % uhslc_id)
            if gloss_id != '':
                print('               <td>%03d</td>' % gloss_id)
            else:
                print('               <td></td>')
            print('               <td>%s</td>' % vrsn)
            print('               <td class="left_text">%s</td>' % s[stn]['properties']['name'])
            print('               <td class="left_text">%s</td>' % s[stn]['properties']['country'])
            print('               <td>%.3f</td>' % lat)
            print('               <td>%.3f</td>' % lng)
            print('               <td>%s</td>' % s[stn]['properties']['rq_versions'][vrsn]['begin'])
            print('               <td>%s</td>' % s[stn]['properties']['rq_versions'][vrsn]['end'])
            print('               <td><a href="%s/%s/daily/d%03d%s.dat">daily</a> <a href="%s/%s/hourly/h%03d%s.zip">hourly</a></td>' % (dat_dir,rq_basin,uhslc_id,vrsn,dat_dir,rq_basin,uhslc_id,vrsn))
            print('               <td><a href="%s/%s/daily/d%03d%s.csv">daily</a> <a href="%s/%s/hourly/h%03d%s.csv">hourly</a></td>' % (csv_dir,rq_basin,uhslc_id,vrsn,csv_dir,rq_basin,uhslc_id,vrsn))
            print('               <td><a href="%s/%s/daily/d%03d%s.nc">daily</a> <a href="%s/%s/hourly/h%03d%s.nc">hourly</a></td>' % (nc_dir,rq_basin,uhslc_id,vrsn,nc_dir,rq_basin,uhslc_id,vrsn)) 
            print('               <td><a href="%s/rqd/OS_UH-RQD%03d%s_20161203_R.nc">daily</a> <a href="%s/rqh/OS_UH-RQH%03d%s_20160323_R.nc">hourly</a></td>' % (oldnc_dir,uhslc_id,vrsn.upper(),oldnc_dir,uhslc_id,vrsn.upper()))
            print('              <td><a href="http://uhslc.soest.hawaii.edu/rqds/%s/doc/qa%03d%s.dmt">meta</a></td>' % (rq_basin,uhslc_id,vrsn))
            print('           </tr>')
            print('')

print('      </tbody>')
print('   </table>')
print('</div>')

