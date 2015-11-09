import csv
from _sqlite3 import Row
from datetime import datetime


# columns in spreadsheet
URI = 0
LABEL = 1
ALT_LABEL = 2
REL = 3
DEF = 4
IN_FILE = '../data/gcos-ecv.csv'
OUT_FILE = '../model/gcos-ecv.ttl'
CLASS = 'ECV'
CONCEPT_SCHEME = '%sConceptScheme' % CLASS
CONCEPT_SCHEME_LABEL = "Essential Climate Variable"

DATE = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

f = open(OUT_FILE, 'w')
f.write('@prefix dc: <http://purl.org/dc/terms/> .\n')
f.write('@prefix gcos: <http://localhost/gcos#> .\n')
f.write('@prefix owl: <http://www.w3.org/2002/07/owl#> .\n')
f.write('@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n')
f.write('@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n\n\n')

# concept scheme
f.write('#\n')
f.write('# concept scheme\n')
f.write('#\n\n')
f.write('gcos:%s a skos:ConceptScheme ;\n' % CONCEPT_SCHEME)
f.write('    skos:prefLabel "A SKOS Concept Scheme for GCOS ECV"@en ;\n')
f.write('    skos:definition "Concepts used within GCOS"@en ;\n')
f.write('    skos:hasTopConcept gcos:atmospheric ;\n')
f.write('    skos:hasTopConcept gcos:terrestrial ;\n')
f.write('    skos:hasTopConcept gcos:oceanic ;\n')
f.write('    dc:date "%s" .\n\n' % DATE)

f.write('gcos:%s a owl:Class ;\n' % CLASS)
f.write('    rdfs:label "%s"@en ;\n' % CONCEPT_SCHEME_LABEL)
f.write('    dc:date "%s" .\n\n\n' % DATE)

# concepts
f.write('#\n')
f.write('# ecv concepts\n')
f.write('#\n\n')

count = 0

with open(IN_FILE, 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter='#', quotechar='|')
    for row in csvreader:
        count = count + 1
        if (count < 2):
            continue

        f.write('gcos:%s a skos:Concept ;\n' % row[URI].strip())
        f.write('    rdfs:subClassOf gcos:%s ;\n' % CLASS)
        f.write('    skos:inScheme gcos:%s ;\n' % CONCEPT_SCHEME)
        f.write('    skos:prefLabel "%s"@en ;\n' % row[LABEL].strip())
        if row[ALT_LABEL] != '':
            f.write('    skos:altLabel "%s"@en ;\n' % row[ALT_LABEL].strip())
        if row[REL] != '':
            f.write('    skos:transitiveBroader gcos:%s ;\n' % row[REL].strip())
        if len(row) > DEF and not (row[DEF] == ''):
            f.write('    skos:definition "%s"@en ;\n' % row[DEF].strip())
        f.write('    dc:date "%s" .\n\n' % DATE)

f.close()
