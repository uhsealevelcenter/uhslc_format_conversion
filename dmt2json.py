#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 21 11:28:54 2021

@author: dyoung
"""

import dmt
import pickle
import json
from glob import glob
#from geojson import Feature, Point, FeatureCollection

#dmt_files = glob('data/*/doc/qa????.dmt')
dmt_files = glob('data/dat/rqds/*/doc/qa????.dmt')
dmt_files.sort()

# invalid encoding files
blacklist = ['data/dat/rqds/atlantic/doc/qa227a.dmt','data/dat/rqds/atlantic/doc/qa271a.dmt','data/dat/rqds/atlantic/doc/qa822a.dmt',
             'data/dat/rqds/atlantic/doc/qa824a.dmt','data/dat/rqds/indian/doc/qa175a.dmt']

# instead of this run the convert_encoding.sh
#blacklist = []

#print(dmt_files)
dmts=[]
for idx, file in enumerate(dmt_files):
    print(file)
    if not file in blacklist:
        with open(file) as f:
           foo = f.readlines()
           M = dmt.dmt(foo)
    else:
        with open(file, encoding="ISO-8859-1") as f:
           foo = f.readlines()
           M = dmt.dmt(foo)


    d = {"name":M.stn_name, 
             "country": M.stn_country,
             "timezone":M.stn_timezone,
             "timemeridian":M.stn_timemeridian,
             "gloss":M.stn_gloss,
             "toga":M.stn_toga,
             "nodc":M.stn_nodc,
             "jasl":M.stn_jasl,
             "contributor":M.contributor,
             "originator":M.originator,
             "originatornum":M.stn_originatornum,
        }
    dmts.append(d)
    
pickle.dump(dmts, open( "dmts.pkl", "wb" ) )

with open('dmts.json', 'w') as f:
    json.dump(dmts, f)


