import csv


# columns in spreadsheet
CCI_URI = 3
REL = 1
GCOS_URI = 0


def write_ttl(in_file_name, out_file_name):
    out_file = '../model/%s' % out_file_name
    f = open(out_file, 'w')
    f.write('@prefix cci: <http://localhost/cci#> .\n')
    f.write('@prefix gcos: <http://localhost/gcos#> .\n')
    f.write('@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n\n')
    
    count = 0
    in_file = '../data/%s' % in_file_name
    with open(in_file, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='#', quotechar='|')
        for row in csvreader:
            count = count + 1
            if (count < 2) or row[REL] == '':
                continue
    
            f.write('gcos:%s a skos:Concept ;\n' % row[GCOS_URI])
            f.write('    skos:%s cci:%s .\n\n' % (row[REL], row[CCI_URI]))
        
    f.close()    
