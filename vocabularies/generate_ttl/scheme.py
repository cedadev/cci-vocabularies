import csv
from datetime import datetime

from rdflib.namespace import DC, OWL, RDFS, SKOS

from vocabularies.settings import SCHEME_MAP, CSV_DIRECTORY, ONTOLOGY_MAP


# columns in spreadsheet
URI = 0
PREF_LABEL = 1
ALT_LABEL = 2
DEF = 3
SEE_ALSO = 4
CITES = 5
HIERARCHY = 5
CREATOR = 6
CONTRIBUTOR = 7
ABSTRACT = 8
DESC = 9
VERSION = 10
RIGHTS = 12
PUBLISHER = 13


def write_ttl(ontology_name):
    # write out the data for each top concept
    in_file = '%s%s-schemes.csv' % (CSV_DIRECTORY, ontology_name)
    count = 0
    with open(in_file, 'rb') as csvfile:
        cvsreader = csv.reader(csvfile, delimiter='`', quotechar='"')
        for row in cvsreader:
            count = count + 1
            if count < 2:
                continue
            _write_concept_scheme(ontology_name, row)


def _write_concept_scheme(ontology_name, row):
    uri = row[URI].strip()
    prefix = '%s-%s' % (ontology_name, uri)
    out_file_name = '%s-scheme.ttl' % prefix

    date = datetime.now().strftime('%Y-%m-%d')
    out_file = '../model/%s' % out_file_name
    f = open(out_file, 'w')
    # prefixes
    f.write('@prefix %s_ontology: <%s> .\n' %
            (ontology_name, ONTOLOGY_MAP[ontology_name]))
    f.write('@prefix %s: <%s/%s> .\n' %
            (prefix, SCHEME_MAP[ontology_name], uri))
    f.write('@prefix dc: <%s> .\n' % DC)
    f.write('@prefix owl: <%s> .\n' % OWL)
    f.write('@prefix rdfs: <%s> .\n' % RDFS)
    f.write('@prefix skos: <%s> .\n\n\n' % SKOS)

    # add to top scheme
    f.write('%s_ontology: a skos:ConceptScheme ;\n' %
            (ontology_name))
    f.write('    skos:hasTopConcept %s: .\n\n' %
            (prefix))

    # concept scheme
    f.write('%s: a skos:ConceptScheme ;\n' %
            (prefix))
    f.write('    skos:prefLabel "%s"@en ;\n' % row[PREF_LABEL])
    f.write('    skos:definition \"%s\"@en ;\n' % _parse(row[DEF]))
    f.write('    dc:title "%s" ;\n' % row[PREF_LABEL])
    f.write('    dc:rights "%s"@en ;\n' % row[RIGHTS])
    f.write('    dc:publisher "%s"@en ;\n' % row[PUBLISHER])
    f.write('    rdfs:comment \"%s\" ;\n' % _parse(row[ABSTRACT]))
    creators = row[CREATOR].split(', ')
    for creator in creators:
        f.write('    dc:creator "%s" ;\n' % creator)
    if row[CONTRIBUTOR]:
        contributors = row[CONTRIBUTOR].split(', ')
        for contributor in contributors:
            f.write('    dc:contributor "%s" ;\n' % contributor)
    f.write('    owl:versionInfo "%s";\n' % row[VERSION])
    f.write('    dc:date "%s" ;\n' % date)

    if row[SEE_ALSO]:
        see_also = row[SEE_ALSO].split(', ')
        for also in see_also:
            f.write('    rdfs:seeAlso <%s> ;\n' % also)
    f.write('    dc:description \"%s\" ;\n' % _parse(row[DESC]))
    f.write('    .\n\n')
    f.close()


def _parse(obj):
    return obj.replace('"', '%22')
