import csv
from _sqlite3 import Row
from datetime import datetime

# columns in spreadsheet
CCI_URI = 0
CCI_LABEL = 1
CCI_ALT_LABEL = 2
CCI_SEE_ALSO = 3

DATE = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# cci-org.ttl
f = open('../model/cci-org.ttl', 'w')
f.write('@prefix dc: <http://purl.org/dc/terms/> .\n')
f.write('@prefix cci: <http://localhost/cci> .\n')
f.write('@prefix foaf: <http://xmlns.com/foaf/spec/> .\n')
f.write('@prefix owl: <http://www.w3.org/2002/07/owl#> .\n')
f.write('@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n')
f.write('@prefix skos: <http://www.w3.org/2008/05/skos#> .\n\n\n')

# concept scheme
f.write('#\n')
f.write('# concept scheme\n')
f.write('#\n\n')
f.write('cci:drsConceptScheme a skos:ConceptScheme ;\n')
f.write('    skos:hasTopConcept cci:orgConceptScheme .\n\n\n')

f.write('cci:orgConceptScheme a skos:ConceptScheme, skos:Concept, owl:Class ;\n')
f.write('    skos:inScheme cci:cciConceptScheme ;\n')
f.write('    skos:prefLabel "org"@en ;\n')
f.write('    skos:altLabel "organisation"@en ;\n')
# f.write('    skos:definition ""@en ;\n')
f.write('    dc:date "%s" .\n\n\n' % DATE)

# org concepts
f.write('#\n')
f.write('# org concepts\n')
f.write('#\n\n')

count = 0

with open('../data/cci-org.csv', 'rb') as csvfile:
    cvsreader = csv.reader(csvfile, delimiter='#', quotechar='|')
    for row in cvsreader:
        count = count + 1
        if (count < 2):
            continue
                
        f.write('cci:%s a skos:Concept ;\n' % row[CCI_URI])
        f.write('    skos:inScheme cci:orgConceptScheme ;\n')
        f.write('    skos:prefLabel "%s"@en ;\n' % row[CCI_LABEL])
        if len(row) > CCI_ALT_LABEL and not (row[CCI_ALT_LABEL] == ''):
            f.write('    skos:altLabel "%s"@en ;\n' % row[CCI_ALT_LABEL])
        if len(row) > CCI_SEE_ALSO and not (row[CCI_SEE_ALSO] == ''):
            f.write('    rdfs:seeAlso <http://isni.org/isni/%s> ;\n' % row[CCI_SEE_ALSO].strip())
        f.write('    dc:date "%s" .\n\n' % DATE)
f.close()
