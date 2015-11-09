import csv
from _sqlite3 import Row
from datetime import datetime

# columns in spreadsheet
CMIP_URI = 0
REL = 1
GRIB_URI = 2

IN_FILE = '../data/cmip-grib-mapping.csv'
OUT_FILE = '../model/cmip-grib-mapping.ttl'

DATE = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

f = open(OUT_FILE, 'w')
f.write('@prefix dc: <http://purl.org/dc/terms/> .\n')
f.write('@prefix cmip: <http://localhost/cmip#> .\n')
f.write('@prefix grib: <http://localhost/grib#> .\n')
f.write('@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n\n')

count = 0
with open(IN_FILE, 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in csvreader:
        count = count + 1
        if (count < 2):
            continue

        f.write('cmip:%s a skos:Concept ;\n' % row[CMIP_URI])
        f.write('    skos:%s grib:%s ;\n' % (row[REL], row[GRIB_URI]))
        f.write('    dc:date "%s" .\n\n' % DATE)

f.close()    
