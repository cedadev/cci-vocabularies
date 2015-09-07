import csv
from _sqlite3 import Row
from datetime import datetime


# columns in spreadsheet
CCI = 0
CCI_LABEL = 1
CCI_REL = 2
CCI_DEF = 3

DATE = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# cci-ecv.ttl
f = open('../model/cci-ecv.ttl', 'w')
f.write('@prefix dc: <http://purl.org/dc/terms/> .\n')
f.write('@prefix cci: <http://localhost/cci> .\n')
f.write('@prefix foaf: <http://xmlns.com/foaf/spec/> .\n')
f.write('@prefix owl: <http://www.w3.org/2002/07/owl#> .\n')
f.write('@prefix skos: <http://www.w3.org/2008/05/skos#> .\n\n\n')

# concept scheme
f.write('#\n')
f.write('# concept scheme\n')
f.write('#\n\n')
f.write('cci:drsConceptScheme a skos:ConceptScheme ;\n')
f.write('    skos:hasTopConcept cci:ecvConceptScheme .\n\n\n')

f.write('cci:ecvConceptScheme a skos:ConceptScheme, skos:Concept, owl:Class ;\n')
f.write('    skos:inScheme cci:cciConceptScheme ;\n')
f.write('    skos:prefLabel "ecv"@en ;\n')
f.write('    skos:altLabel "essential climate variable"@en ;\n')
# f.write('    skos:definition ""@en ;\n')
f.write('    dc:date "%s" .\n\n\n' % DATE)

# ecv concepts
f.write('#\n')
f.write('# ecv concepts\n')
f.write('#\n\n')

count = 0

with open('../data/cci-ecv.csv', 'rb') as csvfile:
    cvsreader = csv.reader(csvfile, delimiter='#', quotechar='|')
    for row in cvsreader:
        count = count + 1
        if (count < 2):
            continue
        
        f.write('cci:%s a skos:Concept ;\n' % row[CCI])
        f.write('    skos:inScheme cci:ecvConceptScheme ;\n')
        f.write('    skos:prefLabel "%s"@en ;\n' % row[CCI_LABEL])
        if row[CCI_REL] != '':
            f.write('    skos:transitiveBroader cci:%s ;\n' % row[CCI_REL])
        if len(row) > CCI_DEF and not (row[CCI_DEF] == ''):
            f.write('    skos:definition "%s"@en ;\n' % row[CCI_DEF])
        f.write('    dc:date "%s" .\n\n' % DATE)

f.close()
