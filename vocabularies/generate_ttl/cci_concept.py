import csv


# columns in spreadsheet
URI = 0
LABEL = 1
ALT_LABEL = 2
DEF = 3
SEE_ALSO = 4


def write_ttl(in_file_name, out_file_name, class_name, class_label):
    concept_scheme = '%sConceptScheme' % class_name
    out_file = '../model/%s' % out_file_name
    f = open(out_file, 'w')
    f.write('@prefix cci: <http://localhost/cci#> .\n')
    f.write('@prefix owl: <http://www.w3.org/2002/07/owl#> .\n')
    f.write('@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n')
    f.write('@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n\n\n')
    
    # concept scheme
    f.write('#\n')
    f.write('# concept scheme\n')
    f.write('#\n\n')
    f.write('cci:%s a skos:ConceptScheme ;\n' % concept_scheme)
    f.write('    rdfs:seeAlso cci:%s .\n\n' % class_name)
    
    f.write('cci:%s a owl:Class ;\n' % class_name)
    f.write('    rdfs:subClassOf cci:DRS ;\n')
    f.write('    rdfs:seeAlso cci:%s ;\n' % concept_scheme)
    f.write('    rdfs:label "%s"@en .\n\n\n' % class_label)
    
    # concepts
    f.write('#\n')
    f.write('# concepts\n')
    f.write('#\n\n')
    
    count = 0
    in_file = '../data/%s' % in_file_name
    with open(in_file, 'rb') as csvfile:
        cvsreader = csv.reader(csvfile, delimiter='#', quotechar='|')
        for row in cvsreader:
            count = count + 1
            if (count < 2):
                continue
    
            f.write('cci:%s a skos:Concept ;\n' % row[URI].strip())
            f.write('    rdfs:subClassOf cci:%s ;\n' % class_name)
            f.write('    skos:inScheme cci:%s ;\n' % concept_scheme)
            f.write('    skos:prefLabel "%s"@en ;\n' % row[LABEL].strip())
            if row[ALT_LABEL] != '':
                f.write('    skos:altLabel "%s" ;\n' % row[ALT_LABEL].strip())
            if len(row) > DEF and not (row[DEF] == ''):
                f.write('    skos:definition "%s"@en ;\n' % row[DEF].strip())
            if len(row) > SEE_ALSO and not (row[SEE_ALSO] == ''):
                f.write('    rdfs:seeAlso <http://isni.org/isni/%s> ;\n' % row[SEE_ALSO].strip())
            f.write('.\n\n')
    f.close()
