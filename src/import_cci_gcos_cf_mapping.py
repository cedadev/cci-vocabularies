import csv
from _sqlite3 import Row
from datetime import datetime

f = open('../model/cci-gcos-cf-mapping.ttl', 'w')
f.write('@prefix dc: <http://purl.org/dc/terms/> .\n')
f.write('@prefix cci: <http://localhost/cci> .\n')
f.write('@prefix foaf: <http://xmlns.com/foaf/spec/> .\n')
f.write('@prefix gcos: <http://localhost/gcos> .\n')
f.write('@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n')
f.write('@prefix skos: <http://www.w3.org/2008/05/skos#> .\n\n')

# columns in spreadsheet
CCI = 0
CCI_REL = 1
GCOS = 3
GCOS_REL = 4
CF_URI = 6

LAST_LINE = 43

DATE = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

count = 0
first = True
with open('../data/cci-gcos-cf-mapping.csv', 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter='#', quotechar='|')
    for row in csvreader:
        count = count + 1
        if (count < 3) | (count > LAST_LINE):
            continue

        if row[CCI] != "":
            cciProject = row[CCI]
            gcos = row[GCOS]
            if first:
                first = False
            else:
                f.write('    dc:date "%s" .\n\n' % DATE)

            f.write('cci:%s a skos:Concept ;\n' % cciProject)
            relationship = row[CCI_REL]  # hack
            if relationship == 'closeMatch or exactMatch?':
                relationship = 'closeMatch'
            f.write('    skos:%s gcos:%s ;\n' % (relationship, gcos))
            
        if not row[CF_URI].startswith('?'):
            f.write('    skos:narrowMatch <%s> ;\n' % row[CF_URI])

    f.write('    dc:date "%s" .\n\n' % DATE)
    
    
count = 0
first = True
with open('../data/cci-gcos-cf-mapping.csv', 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter='#', quotechar='|')
    for row in csvreader:
        count = count + 1
        if (count < 3) | (count > LAST_LINE):
            continue

        if row[CCI] != "":
            cciProject = row[CCI]
            gcos = row[GCOS]
            if first:
                first = False
            else:
                f.write('    dc:date "%s" .\n\n' % DATE)

            f.write('gcos:%s a skos:Concept ;\n' % gcos)
            relationship = row[CCI_REL]  # hack
            if relationship == 'closeMatch or exactMatch?':
                relationship = 'closeMatch'
            f.write('    skos:%s cci:%s ;\n' % (relationship, cciProject))
        if not row[CF_URI].startswith('?'):
            f.write('    skos:narrowMatch <%s> ;\n' % row[CF_URI])

    f.write('    dc:date "%s" .\n\n' % DATE)
    
f.close()    
