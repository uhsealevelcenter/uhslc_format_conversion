#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 21 11:28:54 2021

@author: dyoung
"""

import dmt
import pickle
from glob import glob
#from geojson import Feature, Point, FeatureCollection

infile = "test.dmt"

dmt_files = glob('data/*/doc/qa????.dmt')
dmt_files.sort()

# invalid encoding files
# blacklist = ['data/atlantic/doc/qa227a.dmt','data/atlantic/doc/qa271a.dmt','data/atlantic/doc/qa822a.dmt',
#             'data/atlantic/doc/qa824a.dmt','data/indian/doc/qa175a.dmt']

# instead of this run the convert_encoding.sh
blacklist = []

#print(dmt_files)
dmts=[]
for idx, file in enumerate(dmt_files):
    #print(f)
    with open(file) as f:
        if file not in blacklist:
           #print(file)
           foo = f.readlines()
           M = dmt.dmt(foo)
        #print(M.stn_gloss)
        #print(M.stn_name)
        #print(file)
        #print(M.contributor)
        #print(M.originator)

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
