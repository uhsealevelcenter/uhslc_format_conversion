
from glob import glob
from time import sleep
import os
import readwrite as rw
import shutil
import urllib.request
import zipfile

#import datetime
#import string
#import sys


# mkdir -p fast global
os.makedirs('fast', exist_ok=True)
os.makedirs('global', exist_ok=True)

os.makedirs('data/dat/rqds', exist_ok=True)
os.makedirs('data/dat/fast', exist_ok=True)
os.makedirs('data/csv', exist_ok=True)
os.makedirs('data/netcdf', exist_ok=True)

print ('Download RQ\n')
url = 'https://uhslc.soest.hawaii.edu/rqds/global.zip'
zfn =  os.path.basename(url)
with urllib.request.urlopen(url) as response, open(zfn, 'wb') as out_file:
    shutil.copyfileobj(response, out_file)
with zipfile.ZipFile(zfn,"r") as zip_ref:
    zip_ref.extractall('data/dat')
    for f in glob('data/dat/global/*'):
       shutil.move(f, 'data/dat/rqds')
#       shutil.rmtree('data/dat/global')

basins = ['atlantic','pacific','indian']
for basin in basins:
    try:
        hourly_files = glob('data/dat/rqds/' + basin + '/hourly/' + '*zip')
        pb = rw.ProgressBar(len(hourly_files), '\nUnpacking ' + basin + ' hourly RQ ...')
        for idx, f in enumerate(hourly_files):
            with zipfile.ZipFile(f,"r") as zip_ref:
                zip_ref.extractall(f[:-4])
            pb.update()
    except Exception as e:
        msg = 'While processing ' + str(f) + ':\n' + str(e)
        print(msg)


print ('Download FD\n')
url = 'https://uhslc.soest.hawaii.edu/woce/all.zip'
zfn =  os.path.basename(url)
with urllib.request.urlopen(url) as response, open(zfn, 'wb') as out_file:
    shutil.copyfileobj(response, out_file)
with zipfile.ZipFile(zfn,"r") as zip_ref:
    zip_ref.extractall('data/dat/fast')

