import csv
from _sqlite3 import Row
from datetime import datetime


# columns in spreadsheet
URI = 0
LABEL = 1
ALT_LABEL = 2
DEF = 3

IN_FILE = '../data/cmip-realms.csv'
OUT_FILE = '../model/cmip-realm.ttl'
CONCEPT_SCHEME = 'CmipRealmConceptScheme'

DATE = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

f = open(OUT_FILE, 'w')
f.write('@prefix dc: <http://purl.org/dc/terms/> .\n')
f.write('@prefix cmip: <http://localhost/cmip#> .\n')
f.write('@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n')
f.write('@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n\n\n')

# concept scheme
f.write('#\n')
f.write('# concept scheme\n')
f.write('#\n\n')
f.write('cmip:DRSConceptScheme a skos:ConceptScheme ;\n')
f.write('    skos:hasTopConcept cmip:%s .\n\n\n' % CONCEPT_SCHEME)

f.write('cmip:%s a skos:ConceptScheme, skos:Concept ;\n' % CONCEPT_SCHEME)
f.write('    rdfs:subClassOf cmip:DRSConceptScheme ;\n')
f.write('    skos:inScheme cmip:DRSConceptScheme ;\n')
f.write('    skos:prefLabel "realm"@en ;\n')
# f.write('    skos:altLabel ""@en ;\n')
# f.write('    skos:definition ""@en ;\n')
f.write('    dc:date "%s" .\n\n\n' % DATE)

# concepts
f.write('#\n')
f.write('# realm concepts\n')
f.write('#\n\n')

count = 0

with open(IN_FILE, 'rb') as csvfile:
    cvsreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in cvsreader:
        count = count + 1
        if (count < 2):
            continue

        f.write('cmip:%s a skos:Concept ;\n' % row[URI].strip())
        f.write('    rdfs:subClassOf cmip:%s ;\n' % CONCEPT_SCHEME)
        f.write('    skos:inScheme cmip:%s ;\n' % CONCEPT_SCHEME)
        f.write('    skos:prefLabel "%s"@en ;\n' % row[LABEL].strip())
        if row[ALT_LABEL] != '':
            f.write('    skos:altLabel "%s" ;\n' % row[ALT_LABEL].strip())
        if len(row) > DEF and not (row[DEF] == ''):
            f.write('    skos:definition "%s"@en ;\n' % row[DEF].strip())
        f.write('    dc:date "%s" .\n\n' % DATE)

f.close()
