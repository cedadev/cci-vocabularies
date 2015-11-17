import csv


# columns in spreadsheet
CCI_URI = 0
CF_URI = 2


def write_ttl(in_file_name, out_file_name):   
    out_file = '../model/%s' % out_file_name
    f = open(out_file, 'w')
    f.write('@prefix cci: <http://localhost/cci#> .\n')
    f.write('@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n\n')
    
    count = 0
    in_file = '../data/%s' % in_file_name
    with open(in_file, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csvreader:
            count = count + 1
            if (count < 2):
                continue
        
            if row[CCI_URI] != "":
                cciProject = row[CCI_URI].strip()
            if (not row[CF_URI] == '') and (not row[CF_URI].startswith('?')):
                f.write('cci:%s a skos:Concept ;\n' % cciProject)
                f.write('    skos:narrowMatch <%s> .\n\n' % row[CF_URI].strip())
    
    f.close()    
