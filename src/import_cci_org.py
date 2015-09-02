import csv
from _sqlite3 import Row
from datetime import datetime

DATE = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# cci-org.ttl
f = open('../model/cci-org.ttl', 'w')
f.write('@prefix dc: <http://purl.org/dc/terms/> .\n')
f.write('@prefix cci: <http://localhost/cci> .\n')
f.write('@prefix foaf: <http://xmlns.com/foaf/spec/> .\n')
f.write('@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n')
f.write('@prefix skos: <http://www.w3.org/2008/05/skos#> .\n\n\n')

# concept scheme
f.write('#\n')
f.write('# concept scheme\n')
f.write('#\n\n')
f.write('cci:cciConceptScheme a skos:ConceptScheme ;\n')
f.write('    skos:hasTopConcept cci:org .\n\n\n')

# top concepts
f.write('#\n')
f.write('# top concepts\n')
f.write('#\n\n')
f.write('cci:org a skos:Concept, owl:Class ;\n')
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
                
        f.write('cci:org%s a skos:Concept ;\n' % count)
        f.write('    skos:inScheme cci:cciConceptScheme ;\n')
        f.write('    skos:prefLabel "%s"@en ;\n' % row[0])
        if len(row) > 1 and not (row[1] == ''):
            f.write('    skos:altLabel "%s"@en ;\n' % row[1])
        if len(row) > 2 and not (row[2] == ''):
            f.write('    rdfs:seeAlso <http://isni.org/isni/%s> ;\n' % row[2])
        f.write('    dc:date "%s" .\n\n' % DATE)
f.close()
