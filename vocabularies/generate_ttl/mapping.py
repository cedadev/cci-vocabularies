import csv

from rdflib.namespace import SKOS

from settings import MAPPING_1, MAPPING_2, MAPPING_BOTH, COLLECTION_MAP, \
    CSV_DIRECTORY, ONTOLOGY_MAP


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
        f.write('@prefix %s: <%s> .\n' % (predicate_prefix, ONTOLOGY_MAP[predicate_prefix]))
    except KeyError:
        pass
    f.write('@prefix skos: <%s> .\n\n\n' % SKOS)

    count = 0
    in_file = '%s%s' % (CSV_DIRECTORY, in_file_name)
    with open(in_file, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='`', quotechar='"')
        for row in csvreader:
            count = count + 1
            if (count < 2):
                continue
            if ((mapping == MAPPING_1 or mapping == MAPPING_BOTH)
                    and row[REL_1] != ''):
                f.write('mapa:%s a skos:Concept ;\n' %
                        (row[URI_1].strip()))
                f.write('    %s:%s mapb:%s .\n\n' % (
                    predicate_prefix, row[REL_1].strip(), row[URI_2].strip()))
            if ((mapping == MAPPING_2 or mapping == MAPPING_BOTH)
                    and row[REL_2] != ''):
                f.write('mapb:%s a skos:Concept ;\n' % (row[URI_2].strip()))
                f.write('    %s:%s mapa:%s .\n\n' % (
                    predicate_prefix, row[REL_2].strip(), row[URI_1].strip()))

    f.close()
