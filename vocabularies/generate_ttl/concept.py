import csv

from rdflib.namespace import OWL, RDF, RDFS, SKOS

from settings import NAME_SPACE_MAP, GLOSSARY, CITO, CSV_DIRECTORY, CMIP, GCOS


# columns in spreadsheet
URI = 0
LABEL = 1
ALT_LABEL = 2
DEF = 3
SEE_ALSO = 4
CITES = 5
HIERARCHY = 5


def write_ttl(ontology_name):
    # look up the concept scheme uri
    count = 0
    in_file = '%s%s-schemes.csv' % (CSV_DIRECTORY, ontology_name)
    with open(in_file, 'rb') as csvfile:
        cvsreader = csv.reader(csvfile, delimiter='`', quotechar='"')
        for row in cvsreader:
            count = count + 1
            if count == 3:
                concept_scheme_uri = row[URI].strip()

    # write out the top concepts
    file_name = '%s-top-concepts' % (ontology_name)
    _write_concepts(file_name, ontology_name, concept_scheme_uri, None)

    # write out the concepts for each top concept
    in_file = '%s%s-top-concepts.csv' % (CSV_DIRECTORY, ontology_name)
    count = 0
    with open(in_file, 'rb') as csvfile:
        cvsreader = csv.reader(csvfile, delimiter='`', quotechar='"')
        for row in cvsreader:
            count = count + 1
            if count < 2:
                continue
            top_concept_uri = row[URI].strip()
            file_name = '%s-%s' % (ontology_name, top_concept_uri.lower())
            _write_concepts(file_name, ontology_name, concept_scheme_uri,
                            top_concept_uri)


def _write_concepts(file_name, ontology_name, concept_scheme_uri,
                    top_concept_uri):
    in_file_name = '%s.csv' % file_name
    out_file_name = '%s.ttl' % file_name
    out_file = '../model/%s' % out_file_name
    f = open(out_file, 'w')
    f.write('@prefix %s: <%s> .\n' %
            (ontology_name, NAME_SPACE_MAP[ontology_name]))

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
    in_file = '%s%s' % (CSV_DIRECTORY, in_file_name)
    with open(in_file, 'rb') as csvfile:
        cvsreader = csv.reader(csvfile, delimiter='`', quotechar='"')
        for row in cvsreader:
            count = count + 1
            if (count < 2) or row[URI].strip() == '':
                # header
                continue
            if len(row[URI].strip()) > 8:
                print ("ERROR: URI fragment too long for NERC: %s:%s:%s" %
                       (ontology_name, top_concept_uri, row[URI].strip()))
            if top_concept_uri:
                f.write('%s:%s a skos:Concept, %s:%s;\n' %
                        (ontology_name, row[URI].strip(),
                         ontology_name, top_concept_uri))
            else:
                f.write('%s:%s a skos:Concept, owl:Class;\n' %
                        (ontology_name, row[URI].strip()))
            f.write('    skos:inScheme %s:%s ;\n' %
                    (ontology_name, concept_scheme_uri))
            f.write('    skos:prefLabel "%s"@en ;\n' % row[LABEL].strip())
            if row[ALT_LABEL] != '':
                f.write('    skos:altLabel "%s"@en ;\n' %
                        row[ALT_LABEL].strip())
            if len(row) > DEF and not (row[DEF] == ''):
                f.write('    skos:definition "%s"@en ;\n' % row[DEF].strip())
            if len(row) > SEE_ALSO and not (row[SEE_ALSO] == ''):
                if top_concept_uri == "org":
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
            if top_concept_uri:
                # this is NOT a top concept
                if ((ontology_name != CMIP and ontology_name != GCOS)
                        or (len(row) <= HIERARCHY)
                        or (len(row) > HIERARCHY and row[HIERARCHY] == '1')):
                    f.write('    skos:broader %s:%s;\n' %
                            (ontology_name, top_concept_uri))
            else:
                # this is a top concept
                f.write('    skos:topConceptOf %s:%s ;\n' %
                        (ontology_name, concept_scheme_uri))
                f.write('    rdfs:isDefinedBy <%s> ;\n' %
                        (NAME_SPACE_MAP[ontology_name]))
            f.write('.\n\n')

            if top_concept_uri:
                # relationship from top concept
                f.write('%s:%s skos:narrower %s:%s .\n\n' % (
                    ontology_name, top_concept_uri, ontology_name,
                    row[URI].strip()))
            else:
                # add line to concept scheme
                f.write('%s:%s skos:hasTopConcept %s:%s .\n\n' % (
                    ontology_name, concept_scheme_uri, ontology_name,
                    row[URI].strip()))
    f.close()
