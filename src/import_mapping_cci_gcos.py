import csv
from _sqlite3 import Row
from datetime import datetime

# columns in spreadsheet
CCI_URI = 2
REL = 1
GCOS_URI = 0

IN_FILE = '../data/cci-gcos-mapping.csv'
OUT_FILE = '../model/cci-gcos-mapping.ttl'

DATE = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

f = open(OUT_FILE, 'w')
f.write('@prefix dc: <http://purl.org/dc/terms/> .\n')
f.write('@prefix cci: <http://localhost/cci#> .\n')
f.write('@prefix gcos: <http://localhost/gcos#> .\n')
f.write('@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n\n')

count = 0
with open(IN_FILE, 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in csvreader:
        count = count + 1
        if (count < 2) or row[REL] == '':
            continue
        
        f.write('cci:%s a skos:Concept ;\n' % row[CCI_URI])
        f.write('    skos:%s gcos:%s ;\n' % (row[REL], row[GCOS_URI]))
        f.write('    dc:date "%s" .\n\n' % DATE)
        
        f.write('gcos:%s a skos:Concept ;\n' % row[GCOS_URI])
        f.write('    skos:%s cci:%s ;\n' % (row[REL], row[CCI_URI]))
        f.write('    dc:date "%s" .\n\n' % DATE)
    
f.close()    
