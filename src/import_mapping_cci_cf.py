import csv
from _sqlite3 import Row
from datetime import datetime

# columns in spreadsheet
CCI_URI = 0
CF_URI = 2

IN_FILE = '../data/cci-cfparameters.csv'
OUT_FILE = '../model/cci-cf-mapping.ttl'

DATE = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

f = open(OUT_FILE, 'w')
f.write('@prefix dc: <http://purl.org/dc/terms/> .\n')
f.write('@prefix cci: <http://localhost/cci#> .\n')
f.write('@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n\n')

count = 0
with open(IN_FILE, 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in csvreader:
        count = count + 1
        if (count < 2):
            continue

        if row[CCI_URI] != "":
            cciProject = row[CCI_URI].strip()
        if (not row[CF_URI] == '') and (not row[CF_URI].startswith('?')):
            f.write('cci:%s a skos:Concept ;\n' % cciProject)
            f.write('    skos:narrowMatch <%s> ;\n' % row[CF_URI].strip())
            f.write('    dc:date "%s" .\n\n' % DATE)

f.close()    
