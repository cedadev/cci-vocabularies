import csv
from _sqlite3 import Row
from datetime import datetime

DATE = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

f = open('../model/gcos.ttl', 'w')
f.write('@prefix dc: <http://purl.org/dc/terms/> .\n')
f.write('@prefix gcos: <http://localhost/gcos> .\n')
f.write('@prefix foaf: <http://xmlns.com/foaf/spec/> .\n')
f.write('@prefix skos: <http://www.w3.org/2008/05/skos#> .\n\n\n')

# concept scheme
f.write('#\n')
f.write('# concept scheme\n')
f.write('#\n\n')
f.write('gcos:ecvConceptScheme a skos:ConceptScheme ;\n')
f.write('    skos:prefLabel "A SKOS Concept Scheme for GCOS ECV"@en ;\n')
f.write('    skos:definition "Concepts used within GCOS"@en ;\n')
f.write('    skos:hasTopConcept gcos:atmospheric ;\n')
f.write('    skos:hasTopConcept gcos:terrestrial ;\n')
f.write('    skos:hasTopConcept gcos:oceanic ;\n')
f.write('    dc:creator [ foaf:name "Antony Wilson" ] ;\n')
f.write('    dc:date "%s" .\n\n' % DATE)

# gcos concepts
f.write('#\n')
f.write('# gcos concepts\n')
f.write('#\n\n')

# columns in spreadsheet
GCOS = 0
GCOS_LABEL = 1
GCOS_REL = 2
GCOS_DEF = 3

count = 0

with open('../data/gcos-ecv.csv', 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter='#', quotechar='|')
    for row in csvreader:
        count = count + 1
        if (count < 2):
            continue
        
        f.write('gcos:%s a skos:Concept ;\n' % row[GCOS])
        f.write('    skos:inScheme gcos:ecvConceptScheme ;\n')
        f.write('    skos:prefLabel "%s"@en ;\n' % row[GCOS_LABEL])
        if row[GCOS_REL] != '':
            f.write('    skos:transitiveBroader gcos:%s ;\n' % row[GCOS_REL])
        if len(row) > GCOS_DEF and not (row[GCOS_DEF] == ''):
            f.write('    skos:definition "%s"@en ;\n' % row[GCOS_DEF])
        f.write('    dc:date "%s" .\n\n' % DATE)

f.close()
