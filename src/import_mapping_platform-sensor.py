import csv
from _sqlite3 import Row
from datetime import datetime

# columns in spreadsheet
PLATFORM_URI = 0
REL = 1
SENSOR_URI = 2

IN_FILE = '../data/cci-platform-sensor-mapping.csv'
OUT_FILE = '../model/cci-platform-sensor-mapping.ttl'

DATE = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

f = open(OUT_FILE, 'w')
f.write('@prefix dc: <http://purl.org/dc/terms/> .\n')
f.write('@prefix cci: <http://localhost/cci#> .\n')
f.write('@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n\n')

count = 0
with open(IN_FILE, 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter='#', quotechar='|')
    for row in csvreader:
        count = count + 1
        if (count < 2):
            continue

        f.write('cci:%s a skos:Concept ;\n' % row[PLATFORM_URI].strip())
        f.write('    cci:hasSensor cci:%s ;\n' % row[SENSOR_URI].strip())
        f.write('    dc:date "%s" .\n\n' % DATE)

        f.write('cci:%s a skos:Concept ;\n' % row[SENSOR_URI].strip())
        f.write('    cci:hasPlatform cci:%s ;\n' % row[PLATFORM_URI].strip())
        f.write('    dc:date "%s" .\n\n' % DATE)

f.close()    
