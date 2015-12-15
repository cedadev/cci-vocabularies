import csv

from rdflib.namespace import OWL, RDF, RDFS, SKOS

from settings import NAME_SPACE_MAP, GLOSSARY, CITO, CSV_DIRECTORY



# columns in spreadsheet
URI = 0
LABEL = 1
ALT_LABEL = 2
DEF = 3
SEE_ALSO = 4
CITES = 5

def write_ttl(in_file_name, out_file_name, class_name, class_label, prefix):
    concept_scheme = '%sConceptScheme' % class_name
    out_file = '../model/%s' % out_file_name
    f = open(out_file, 'w')
    f.write('@prefix %s: <%s> .\n' % 
            (prefix, NAME_SPACE_MAP[prefix]))
    if prefix == GLOSSARY:
        f.write('@prefix cito: <%s> .\n' % CITO)
    f.write('@prefix owl: <%s> .\n' % OWL)
    f.write('@prefix rdf: <%s> .\n' % RDF)
    f.write('@prefix rdfs: <%s> .\n' % RDFS)
    f.write('@prefix skos: <%s> .\n\n\n' % SKOS)

    # bag
    f.write('%s:DRS a rdf:Bag ;\n' % prefix)
    f.write('    rdfs:member %s:%s .\n\n\n' % (prefix, class_name))

    # class
    f.write('%s:%s a owl:Class ;\n' % (prefix, class_name))
    f.write('    rdfs:seeAlso %s:%s ;\n' % (prefix, concept_scheme))
    f.write('    rdfs:label "%s"@en .\n\n\n' % class_label)

    # concept scheme
    f.write('#\n')
    f.write('# concept scheme\n')
    f.write('#\n\n')
    f.write('%s:%s a skos:ConceptScheme ;\n' % (prefix, concept_scheme))
    f.write('    rdfs:seeAlso %s:%s .\n\n' % (prefix, class_name))

    # concepts
    f.write('#\n')
    f.write('# concepts\n')
    f.write('#\n\n')
    
    count = 0
    in_file = '%s%s' % (CSV_DIRECTORY, in_file_name)
    with open(in_file, 'rb') as csvfile:
        cvsreader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for row in cvsreader:
            count = count + 1
            if (count < 2) or row[URI].strip() == '':
                continue

            f.write('%s:%s a skos:Concept, owl:Class ;\n' % (prefix, row[URI].strip()))
            f.write('    rdfs:subClassOf %s:%s ;\n' % (prefix, class_name))
            f.write('    skos:inScheme %s:%s ;\n' % (prefix, concept_scheme))
            f.write('    skos:prefLabel "%s"@en ;\n' % row[LABEL].strip())
            if row[ALT_LABEL] != '':
                f.write('    skos:altLabel "%s"@en ;\n' % row[ALT_LABEL].strip())
            if len(row) > DEF and not (row[DEF] == ''):
                f.write('    skos:definition "%s"@en ;\n' % row[DEF].strip())
            if len(row) > SEE_ALSO and not (row[SEE_ALSO] == ''):
                see_also = row[SEE_ALSO].strip()
                if class_name == "Organisation":
                    f.write('    rdfs:seeAlso <http://isni.org/isni/%s> ;\n' % see_also)
            if prefix == GLOSSARY and len(row) > CITES and not (row[CITES] == ''):
                f.write('    cito:citesAsSourceDocument <%s>;\n' % row[CITES].strip())
                
            f.write('.\n\n')
    f.close()
