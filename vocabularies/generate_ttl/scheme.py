import csv
from datetime import datetime


# columns in spreadsheet
URI = 0
TITLE = 1
RIGHTS = 2
PUBLISHER = 3
PREF_LABEL = 4
ALT_LABEL = 5
CREATOR = 6
CONTRIBUTOR = 7
DEF = 8
DESC = 9
VERSION = 10
SEE_ALSO = 11

def write_ttl(in_file_name, out_file_name, ontology_name):
    date = datetime.now().strftime('%Y-%m-%d')
    out_file = '../model/%s' % out_file_name
    f = open(out_file, 'w')
    f.write('@prefix %s: <http://localhost/%s#> .\n' % (ontology_name, ontology_name))
    f.write('@prefix dc: <http://purl.org/dc/elements/1.1/> .\n')
    f.write('@prefix owl: <http://www.w3.org/2002/07/owl#> .\n')
    f.write('@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n')
    f.write('@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n\n\n')
    
    count = 0
    in_file = '../data/%s' % in_file_name
    with open(in_file, 'rb') as csvfile:
        cvsreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in cvsreader:
            count = count + 1
            if (count < 2):
                continue
            if row[URI] == 'Ontology':
                f.write('<http://vm62.nubes.stfc.ac.uk/%s/%s> a owl:Ontology ;\n' % (ontology_name, ontology_name))
                f.write('    dc:title \'%s\' ;\n' % row[TITLE])
                f.write('    dc:rights \'%s\'@en ;\n' % row[RIGHTS])
                f.write('    dc:publisher \'%s\'@en ;\n' % row[PUBLISHER])
                f.write('    rdfs:comment \'%s\' ;\n' % row[DEF])
            else:
                f.write('%s:%s a skos:ConceptScheme ;\n' %  (ontology_name, row[URI]))
                f.write('    skos:prefLabel "%s"@en ;\n' % row[PREF_LABEL])
                if row[ALT_LABEL]:
                    f.write('    skos:altLabel "%s"@en ;\n' % row[ALT_LABEL])
                f.write('    skos:definition \'%s\'@en ;\n' % row[DEF])

            if row[SEE_ALSO]:
                see_also = row[SEE_ALSO].split(', ')
                for also in see_also:
                    f.write('    rdfs:seeAlso %s ;\n' % also)
            creators = row[CREATOR].split(', ')
            for creator in creators:
                f.write('    dc:creator "%s" ;\n' % creator)
            if row[CONTRIBUTOR]:
                contributors = row[CONTRIBUTOR].split(', ')
                for contributor in contributors:
                    f.write('    dc:contributor "%s" ;\n' % contributor)                        
            f.write('    dc:description \'%s\' ;\n' % row[DESC])
            f.write('    owl:versionInfo \'%s\';\n' % row[VERSION])                        
            f.write('    dc:date "%s" .\n\n' % date)
    f.close()
