import csv


# columns in spreadsheet
PLATFORM_URI = 0
REL = 1
SENSOR_URI = 2


def write_ttl(in_file_name, out_file_name):
    out_file = '../model/%s' % out_file_name
    f = open(out_file, 'w')
    f.write('@prefix cci: <http://localhost/cci#> .\n')
    f.write('@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n\n')
    
    count = 0
    in_file = '../data/%s' % in_file_name
    with open(in_file, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='#', quotechar='|')
        for row in csvreader:
            count = count + 1
            if (count < 2):
                continue
    
            f.write('cci:%s a skos:Concept ;\n' % row[PLATFORM_URI].strip())
            f.write('    cci:hasSensor cci:%s .\n\n' % row[SENSOR_URI].strip())
    
            f.write('cci:%s a skos:Concept ;\n' % row[SENSOR_URI].strip())
            f.write('    cci:hasPlatform cci:%s .\n\n' % row[PLATFORM_URI].strip())
    
    f.close()    
