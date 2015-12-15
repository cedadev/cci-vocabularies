import csv

from rdflib.namespace import SKOS

from settings import CCI, CCI_NAME_SPACE, CSV_DIRECTORY


# columns in spreadsheet
CCI_URI = 0
CF_URI = 2


def write_ttl(in_file_name, out_file_name):   
    out_file = '../model/%s' % out_file_name
    f = open(out_file, 'w')
    f.write('@prefix %s: <%s> .\n' % (CCI, CCI_NAME_SPACE))
    f.write('@prefix skos: <%s> .\n\n\n' % SKOS)
    
    count = 0
    in_file = '%s%s' % (CSV_DIRECTORY, in_file_name)
    with open(in_file, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for row in csvreader:
            count = count + 1
            if (count < 2):
                continue

            if row[CCI_URI] != "":
                cciProject = row[CCI_URI].strip()
            if (not row[CF_URI] == '') and (not row[CF_URI].startswith('?')):
                f.write('%s:%s a skos:Concept ;\n' % (CCI, cciProject))
                f.write('    skos:narrowMatch <%s> .\n\n' % row[CF_URI].strip())
    
    f.close()    
