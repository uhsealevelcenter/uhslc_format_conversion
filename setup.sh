#!/bin/bash

mkdir -p rqds woce

# cd rqds
curl -O http://uhslc.soest.hawaii.edu/rqds/global.zip
unzip -qod rqds global.zip

for f in rqds/{atlantic,pacific,indian}/hourly/*.zip
do
 f1=`echo $f | sed -e s/.zip//`
 mkdir -p $f1
 echo "Processing $f1"
 unzip -qod $f1 $f
done 

curl -O http://uhslc.soest.hawaii.edu/woce/all.zip
unzip -qo all.zip

