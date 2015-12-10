import csv

from rdflib.namespace import SKOS

from settings import NAME_SPACE_MAP


# columns in spreadsheet
URI = 0


def write_ttl(in_file_name, out_file_name, class_name, prefix):
    concept_scheme = '%sConceptScheme' % class_name
    out_file = '../model/%s' % out_file_name
    f = open(out_file, 'w')
    f.write('@prefix %s: <%s> .\n' % 
            (prefix, NAME_SPACE_MAP[prefix]))
    f.write('@prefix skos: <%s> .\n\n\n' % SKOS)

    count = 0
    in_file = '../data/%s' % in_file_name
    with open(in_file, 'rb') as csvfile:
        cvsreader = csv.reader(csvfile, delimiter='#', quotechar='"')
        for row in cvsreader:
            count = count + 1
            if (count < 2):
                continue

            f.write('%s:%s skos:hasTopConcept %s:%s .\n' % (prefix, concept_scheme, prefix, row[URI].strip()))
            f.write('%s:%s skos:topConceptOf %s:%s .\n\n\n' % (prefix, row[URI].strip(), prefix, concept_scheme))

    f.close()
