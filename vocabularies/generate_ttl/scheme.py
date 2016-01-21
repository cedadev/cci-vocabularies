import csv
from datetime import datetime

from rdflib.namespace import DC, OWL, RDFS, SKOS

from settings import NAME_SPACE_MAP, CSV_DIRECTORY


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


def write_ttl(ontology_name):
    in_file_name = '%s-schemes.csv' % ontology_name
    out_file_name = '%s-schemes.ttl' % ontology_name

    date = datetime.now().strftime('%Y-%m-%d')
    out_file = '../model/%s' % out_file_name
    f = open(out_file, 'w')
    f.write('@prefix %s: <%s> .\n' %
            (ontology_name, NAME_SPACE_MAP[ontology_name]))
    f.write('@prefix dc: <%s> .\n' % DC)
    f.write('@prefix owl: <%s> .\n' % OWL)
    f.write('@prefix rdfs: <%s> .\n' % RDFS)
    f.write('@prefix skos: <%s> .\n\n\n' % SKOS)

    count = 0
    in_file = '%s%s' % (CSV_DIRECTORY, in_file_name)
    with open(in_file, 'rb') as csvfile:
        cvsreader = csv.reader(csvfile, delimiter='`', quotechar='|')
        for row in cvsreader:
            count = count + 1
            if (count < 2):
                continue

            if count == 2:
                # ontology
                f.write('<%s> a owl:Ontology ;\n' %
                        (NAME_SPACE_MAP[ontology_name]))
                f.write('    dc:title "%s" ;\n' % row[TITLE])
                f.write('    dc:rights "%s"@en ;\n' % row[RIGHTS])
                f.write('    dc:publisher "%s"@en ;\n' % row[PUBLISHER])
                f.write('    rdfs:comment \"%s\" ;\n' % _parse(row[DEF]))
                f.write('    rdfs:label \"%s\" ;\n' % _parse(row[PREF_LABEL]))

            elif count == 3:
                # concept scheme
                concept_scheme_uri = row[URI].strip()
                f.write('%s:%s a skos:ConceptScheme ;\n' %
                        (ontology_name, concept_scheme_uri))
                f.write('    skos:prefLabel "%s"@en ;\n' % row[PREF_LABEL])
                f.write('    skos:definition \"%s\"@en ;\n' % _parse(row[DEF]))

            # ontology or concept scheme
            creators = row[CREATOR].split(', ')
            for creator in creators:
                f.write('    dc:creator "%s" ;\n' % creator)
            if row[CONTRIBUTOR]:
                contributors = row[CONTRIBUTOR].split(', ')
                for contributor in contributors:
                    f.write('    dc:contributor "%s" ;\n' % contributor)
            f.write('    owl:versionInfo "%s";\n' % row[VERSION])
            f.write('    dc:date "%s" ;\n' % date)

            if len(row) > SEE_ALSO and row[SEE_ALSO]:
                see_also = row[SEE_ALSO].split(', ')
                for also in see_also:
                    f.write('    rdfs:seeAlso <%s> ;\n' % also)
            f.write('    dc:description \"%s\" ;\n' % _parse(row[DESC]))
            f.write('    .\n\n')
    f.close()


def _parse(obj):
    return obj.replace('"', '%22')
