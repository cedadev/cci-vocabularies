import csv
from datetime import datetime
import os

from rdflib.namespace import DC, OWL, RDFS, SKOS

from settings import CSV_DIRECTORY, COLLECTION_MAP


# columns in spreadsheet
URI = 0
PREF_LABEL = 1
ALT_LABEL = 2
CREATOR = 3
ABSTRACT = 4
DESC = 5
VERSION = 6
PUBLISHER = 7


def write_ttl(ontology_name):
    in_file = os.path.join(CSV_DIRECTORY,
                           '{}-collections.csv'.format(ontology_name))
    count = 0
    with open(in_file, 'rb') as csvfile:
        cvsreader = csv.reader(csvfile, delimiter='`', quotechar='"')
        for row in cvsreader:
            count = count + 1
            if count < 2:
                continue
            _write_collection(ontology_name, row)


def _write_collection(ontology_name, row):
    uri = row[URI].strip()
    prefix = '%s-%s-collection' % (ontology_name, uri)
    out_file_name = '%s.ttl' % prefix

    date = datetime.now().strftime('%Y-%m-%d')
    out_file = os.path.join('..', 'model', out_file_name)
    f = open(out_file, 'w')
    # prefixes
    f.write('@prefix %s: <%s%s> .\n' %
            (prefix, COLLECTION_MAP[ontology_name], uri))
    f.write('@prefix dc: <%s> .\n' % DC)
    f.write('@prefix owl: <%s> .\n' % OWL)
    f.write('@prefix rdfs: <%s> .\n' % RDFS)
    f.write('@prefix skos: <%s> .\n\n\n' % SKOS)

    # collection
    f.write('<%s%s> a skos:Collection ;\n' %
            (COLLECTION_MAP[ontology_name], uri))
    f.write('    skos:prefLabel "%s"@en ;\n' % row[PREF_LABEL])
    f.write('    skos:definition "%s"@en ;\n' % _parse(row[DESC]))
    f.write('    dc:title "%s" ;\n' % row[PREF_LABEL])
    f.write('    dc:publisher "%s"@en ;\n' % row[PUBLISHER])
    f.write('    rdfs:comment \"%s\" ;\n' % _parse(row[ABSTRACT]))
    creators = row[CREATOR].split(', ')
    for creator in creators:
        f.write('    dc:creator "%s" ;\n' % creator)
    f.write('    owl:versionInfo "%s";\n' % row[VERSION])
    f.write('    dc:date "%s" ;\n' % date)
    f.write('    dc:description \"%s\" ;\n' % _parse(row[DESC]))
    f.write('    .\n\n')
    f.close()


def _parse(obj):
    return obj.replace('"', '%22')
