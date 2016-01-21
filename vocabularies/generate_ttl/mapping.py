import csv

from rdflib.namespace import SKOS

from settings import MAPPING_1, MAPPING_2, MAPPING_BOTH, NAME_SPACE_MAP, \
    CSV_DIRECTORY


# columns in spreadsheet
URI_1 = 0
REL_1 = 1
URI_2 = 2
REL_2 = 3


def write_ttl(in_file_name, out_file_name, mapping, uri_1_prefix,
              uri_2_prefix, predicate_prefix):
    out_file = '../model/%s' % out_file_name
    f = open(out_file, 'w')
    f.write('@prefix %s: <%s> .\n' % (uri_1_prefix,
                                      NAME_SPACE_MAP[uri_1_prefix]))
    f.write('@prefix %s: <%s> .\n' % (uri_2_prefix,
                                      NAME_SPACE_MAP[uri_2_prefix]))
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
                f.write('%s:%s a skos:Concept ;\n' %
                        (uri_1_prefix, row[URI_1].strip()))
                f.write('    %s:%s %s:%s .\n\n' % (
                    predicate_prefix, row[REL_1].strip(), uri_2_prefix,
                    row[URI_2].strip()))
            if ((mapping == MAPPING_2 or mapping == MAPPING_BOTH)
                    and row[REL_2] != ''):
                f.write('%s:%s a skos:Concept ;\n' %
                        (uri_2_prefix, row[URI_2].strip()))
                f.write('    %s:%s %s:%s .\n\n' % (
                    predicate_prefix, row[REL_2].strip(), uri_1_prefix,
                    row[URI_1].strip()))

    f.close()
