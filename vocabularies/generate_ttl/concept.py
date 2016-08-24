import csv

from rdflib.namespace import OWL, RDF, RDFS, SKOS

from settings import SCHEME_MAP, GLOSSARY, CITO, CSV_DIRECTORY, \
    COLLECTION_MAP, ONTOLOGY_MAP


# columns in spreadsheet
URI = 0
LABEL = 1
ALT_LABEL = 2
DEF = 3
SEE_ALSO = 4
CITES = 5
HIERARCHY = 5


def write_ttl(ontology_name):
    # write out the concepts for each concept scheme
    in_file = '%s%s-schemes.csv' % (CSV_DIRECTORY, ontology_name)
    count = 0
    with open(in_file, 'rb') as csvfile:
        cvsreader = csv.reader(csvfile, delimiter='`', quotechar='"')
        for row in cvsreader:
            count = count + 1
            if count < 2:
                continue
            concept_scheme_uri = row[URI].strip()
            file_name = '%s-%s' % (ontology_name, concept_scheme_uri.lower())
            _write_concepts(file_name, ontology_name, concept_scheme_uri)


def _write_concepts(file_name, ontology_name, concept_scheme_uri):
    in_file_name = '%s.csv' % file_name
    out_file_name = '%s.ttl' % file_name
    out_file = '../model/%s' % out_file_name
    f = open(out_file, 'w')
    prefix_ontology = '%s_ontology' % (ontology_name)
    prefix_scheme = '%s_%s_scheme' % (ontology_name, concept_scheme_uri)
    prefix_collection = '%s_%s_coll' % (ontology_name, concept_scheme_uri)
    prefix_concept = '%s_%s_concept' % (ontology_name, concept_scheme_uri)
    f.write('@prefix %s: <%s%s/> .\n' %
            (prefix_concept, COLLECTION_MAP[ontology_name], concept_scheme_uri))
    f.write('@prefix %s: <%s> .\n' %
            (prefix_ontology, ONTOLOGY_MAP[ontology_name]))
    f.write('@prefix %s: <%s%s> .\n' %
            (prefix_collection, COLLECTION_MAP[ontology_name], concept_scheme_uri))
    f.write('@prefix %s: <%s/%s> .\n' %
            (prefix_scheme, SCHEME_MAP[ontology_name], concept_scheme_uri))

    if ontology_name == GLOSSARY:
        f.write('@prefix cito: <%s> .\n' % CITO)

    f.write('@prefix owl: <%s> .\n' % OWL)
    f.write('@prefix rdf: <%s> .\n' % RDF)
    f.write('@prefix rdfs: <%s> .\n' % RDFS)
    f.write('@prefix skos: <%s> .\n\n\n' % SKOS)

    # concepts
    f.write('#\n')
    f.write('# concepts\n')
    f.write('#\n\n')

    count = 0
    check_hierarchy = False
    in_file = '%s%s' % (CSV_DIRECTORY, in_file_name)
    with open(in_file, 'rb') as csvfile:
        cvsreader = csv.reader(csvfile, delimiter='`', quotechar='"')
        for row in cvsreader:
            count = count + 1
            if (count < 2) or row[URI].strip() == '':
                # header
                if len(row) > HIERARCHY and row[HIERARCHY] == 'Hierarchy Level':
                    check_hierarchy = True
                continue
#             if len(row[URI].strip()) > 8:
#                 print ("ERROR: URI fragment too long for NERC: %s:%s:%s" %
#                        (ontology_name, concept_scheme_uri, row[URI].strip()))
            f.write('%s:%s a skos:Concept, %s:%s;\n' %
                    (prefix_concept, row[URI].strip(),
                     prefix_ontology, concept_scheme_uri))
            f.write('    skos:inScheme %s: ;\n' %
                    (prefix_scheme))
            f.write('    skos:prefLabel "%s"@en ;\n' % row[LABEL].strip())
            if row[ALT_LABEL] != '':
                f.write('    skos:altLabel "%s"@en ;\n' %
                        row[ALT_LABEL].strip())
            if len(row) > DEF and not (row[DEF] == ''):
                f.write('    skos:definition "%s"@en ;\n' % row[DEF].strip())
            if len(row) > SEE_ALSO and not (row[SEE_ALSO] == ''):
                if concept_scheme_uri == "org":
                    f.write('    rdfs:seeAlso <http://isni.org/isni/%s> ;\n' %
                            row[SEE_ALSO].strip())
                elif ontology_name == GLOSSARY:
                    pass
                elif not(row[SEE_ALSO].startswith('?')):
                    f.write('    rdfs:seeAlso <%s> ;\n' %
                            row[SEE_ALSO].strip())
            if (ontology_name == GLOSSARY and len(row) > CITES
                    and not (row[CITES] == '')):
                f.write('    cito:citesAsSourceDocument <%s>;\n' %
                        row[CITES].strip())
            if (not check_hierarchy or
                (check_hierarchy and len(row) > HIERARCHY
                 and row[HIERARCHY] == '1')):
                # this is top of any hierarchy if present
                f.write('    skos:topConceptOf %s: ;\n' %
                        (prefix_scheme))
            f.write('.\n\n')

            # add to collection
            f.write('%s: skos:member %s:%s .\n\n' % (
                prefix_collection, prefix_concept, row[URI].strip()))

            # add line to concept scheme
            if (not check_hierarchy or
                (check_hierarchy and len(row) > HIERARCHY
                 and row[HIERARCHY] == '1')):
                # this is top of any hierarchy if present
                f.write('%s: skos:hasTopConcept %s:%s .\n\n' % (
                    prefix_scheme, prefix_concept, row[URI].strip()))
    f.close()
