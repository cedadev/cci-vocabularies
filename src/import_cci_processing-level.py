import csv
from _sqlite3 import Row
from datetime import datetime


# columns in spreadsheet
URI = 0
LABEL = 1
ALT_LABEL = 2
DEF = 4

IN_FILE = '../data/cci-processing-levels.csv'
OUT_FILE = '../model/cci-processing-level.ttl'
CLASS = 'ProcessingLevel'
CONCEPT_SCHEME = '%sConceptScheme' % CLASS
CONCEPT_SCHEME_LABEL = 'Processing Level'

DATE = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

f = open(OUT_FILE, 'w')
f.write('@prefix dc: <http://purl.org/dc/terms/> .\n')
f.write('@prefix cci: <http://localhost/cci#> .\n')
f.write('@prefix owl: <http://www.w3.org/2002/07/owl#> .\n')
f.write('@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n')
f.write('@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n\n\n')

# concept scheme
f.write('#\n')
f.write('# concept scheme\n')
f.write('#\n\n')
f.write('cci:DRSConceptScheme a skos:ConceptScheme ;\n')
f.write('    skos:hasTopConcept cci:%s .\n\n\n' % CONCEPT_SCHEME)

f.write('cci:%s a skos:ConceptScheme, skos:Concept ;\n' % CONCEPT_SCHEME)
f.write('    skos:inScheme cci:DRSConceptScheme ;\n')
f.write('    skos:prefLabel "processing level"@en ;\n')
# f.write('    skos:altLabel ""@en ;\n')
# f.write('    skos:definition ""@en ;\n')
f.write('    dc:date "%s" .\n\n\n' % DATE)

f.write('cci:%s a owl:Class ;\n' % CLASS)
f.write('    rdfs:subClassOf cci:DRS ;\n')
f.write('    rdfs:label "%s"@en ;\n' % CONCEPT_SCHEME_LABEL)
f.write('    dc:date "%s" .\n\n\n' % DATE)

# concepts
f.write('#\n')
f.write('# processing level concepts\n')
f.write('#\n\n')

count = 0

with open(IN_FILE, 'rb') as csvfile:
    cvsreader = csv.reader(csvfile, delimiter='#', quotechar='|')
    for row in cvsreader:
        count = count + 1
        if (count < 2):
            continue

        f.write('cci:%s a skos:Concept ;\n' % row[URI].strip())
        f.write('    rdfs:subClassOf cci:%s ;\n' % CLASS)
        f.write('    skos:inScheme cci:%s ;\n' % CONCEPT_SCHEME)
        f.write('    skos:prefLabel "%s"@en ;\n' % row[LABEL].strip())
        if row[ALT_LABEL] != '':
            f.write('    skos:altLabel "%s" ;\n' % row[ALT_LABEL].strip())
        if len(row) > DEF and not (row[DEF] == ''):
            f.write('    skos:definition "%s"@en ;\n' % row[DEF].strip())
        f.write('    dc:date "%s" .\n\n' % DATE)

f.close()
