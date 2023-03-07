
# rsync -au data/atlantic/doc/qa227a.dmt data/atlantic/doc/qa271a.dmt data/atlantic/doc/qa822a.dmt data/atlantic/doc/qa824a.dmt data/indian/doc/qa175a.dmt backup

mkdir -p backup

cp data/dat/rqds/atlantic/doc/qa227a.dmt backup
cp data/dat/rqds/atlantic/doc/qa271a.dmt backup
cp data/dat/rqds/atlantic/doc/qa822a.dmt backup
cp data/dat/rqds/atlantic/doc/qa824a.dmt backup
cp data/dat/rqds/indian/doc/qa175a.dmt backup

iconv -f ISO-8859-1 -t UTF-8 backup/qa227a.dmt > data/dat/rqds/atlantic/doc/qa227a.dmt
iconv -f ISO-8859-1 -t UTF-8 backup/qa271a.dmt > data/dat/rqds/atlantic/doc/qa271a.dmt
iconv -f ISO-8859-1 -t UTF-8 backup/qa822a.dmt > data/dat/rqds/atlantic/doc/qa822a.dmt
iconv -f ISO-8859-1 -t UTF-8 backup/qa824a.dmt > data/dat/rqds/atlantic/doc/qa824a.dmt
iconv -f ISO-8859-1 -t UTF-8 backup/qa175a.dmt > data/dat/rqds/indian/doc/qa175a.dmt

