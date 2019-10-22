import csv
import os

from rdflib.namespace import SKOS

from vocabularies.settings import MAPPING_1, MAPPING_2, MAPPING_BOTH, \
    COLLECTION_MAP, CSV_DIRECTORY, ONTOLOGY_MAP


# columns in spreadsheet
URI_1 = 0
REL_1 = 1
URI_2 = 2
REL_2 = 3


def write_ttl(in_file_name, out_file_name, mapping, uri_1_prefix, uri_1_sufix,
              uri_2_prefix, uri_2_sufix, predicate_prefix):
    out_file = '../model/%s' % out_file_name
    f = open(out_file, 'w')
    f.write('@prefix mapa: <%s%s> .\n' % (
            COLLECTION_MAP[uri_1_prefix], uri_1_sufix))
    f.write('@prefix mapb: <%s%s> .\n' % (
            COLLECTION_MAP[uri_2_prefix], uri_2_sufix))
    try:
        f.write('@prefix %s: <%s> .\n' %
                (predicate_prefix, ONTOLOGY_MAP[predicate_prefix]))
    except KeyError:
        pass
    f.write('@prefix skos: <%s> .\n\n\n' % SKOS)

    count = 0
    in_file = os.path.join(CSV_DIRECTORY, in_file_name)
    with open(in_file, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='`', quotechar='"')
        for row in csvreader:
            count = count + 1
            if (count < 2):
                continue
            url_1 = _get_url('mapa', row[URI_1])
            url_2 = _get_url('mapb', row[URI_2])
            if ((mapping == MAPPING_1 or mapping == MAPPING_BOTH)
                    and row[REL_1] != ''):
                f.write('%s %s:%s %s .\n\n' % (url_1,
                                               predicate_prefix, row[REL_1].strip(), url_2))
            if ((mapping == MAPPING_2 or mapping == MAPPING_BOTH)
                    and row[REL_2] != ''):
                f.write('%s %s:%s %s .\n\n' % (url_2,
                                               predicate_prefix, row[REL_2].strip(), url_1))

    f.close()


def _get_url(mapping, url):
    url = url.strip()
    if 'http' in url:
        return '<{}>'.format(url)
    return '{mapping}:{url}'.format(mapping=mapping, url=url)
