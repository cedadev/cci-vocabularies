import csv

from rdflib.namespace import OWL, RDF, RDFS, SKOS

from settings import CITO, NAME_SPACE_MAP, CSV_DIRECTORY


# columns in spreadsheet
URI = 0
LABEL = 2
ALT_LABEL = 1
DEF = 3
# SEE_ALSO = 6

GLOSSARY_NAME = 0
IPCC = 4
LINK_TEXT = 5
LINK = 6
LINKS = 'links'


def write_ttl(in_file_name, out_file_name, class_name, class_label, prefix):
    concept_scheme = '%sConceptScheme' % class_name
    out_file = '../model/%s' % out_file_name
    f = open(out_file, 'w')
    f.write('@prefix %s: <%s> .\n' % 
            (prefix, NAME_SPACE_MAP[prefix]))
    f.write('@prefix cito: <%s> .\n' % CITO)
    f.write('@prefix owl: <%s> .\n' % OWL)
    f.write('@prefix rdf: <%s> .\n' % RDF)
    f.write('@prefix rdfs: <%s> .\n' % RDFS)
    f.write('@prefix skos: <%s> .\n\n\n' % SKOS)

    # concept scheme
    f.write('#\n')
    f.write('# concept scheme\n')
    f.write('#\n\n')
    f.write('%s:%s a skos:ConceptScheme .\n' % (prefix, concept_scheme))

    # concepts
    f.write('#\n')
    f.write('# concepts\n')
    f.write('#\n\n')
    
    glossary = _parse_file(in_file_name)
    for key in glossary.keys():
        for line in glossary[key]:
            f.write('%s:%s a skos:Concept ;\n' % (prefix, line[ALT_LABEL])) # TODO what to use as uri?
            f.write('    skos:inScheme %s:%s ;\n' % (prefix, concept_scheme))
            f.write('    skos:prefLabel "%s"@en ;\n' % line[LABEL])
            if line[ALT_LABEL] != '':
                f.write('    skos:altLabel "%s" ;\n' % line[ALT_LABEL])
            if line[DEF] != '':
                f.write('    skos:definition "%s"@en ;\n' % line[DEF])

            try:
                citation = line[IPCC]
            except KeyError:
                citation = None
            if citation == 'WGI':
                f.write('    cito:citesAsSourceDocument <http://www.ipcc.ch/pdf/glossary/ar4-wg1.pdf>;\n')
            elif citation == 'WGII':
                f.write('    cito:citesAsSourceDocument <http://www.ipcc.ch/pdf/glossary/ar4-wg2.pdf>;\n')
            elif citation == 'WGIII':
                f.write('    cito:citesAsSourceDocument <http://www.ipcc.ch/pdf/glossary/ar4-wg3.pdf>;\n')
            elif citation == 'WGI (AR4)':
                f.write('    cito:citesAsSourceDocument <http://www.ipcc.ch/>;\n') # TODO find ref
            elif citation:
                print 'unknown citation %s' % citation
            try:
                links = line[LINKS]
                keys = links.keys()
                sorted_keys = sorted(keys)
                for key in sorted_keys:
                    if key.startswith('http'):
                        f.write('    rdfs:seeAlso <%s> ;\n' % key)
                    elif key:
                        f.write('    rdfs:seeAlso %s:%s ;\n' % (prefix, key.split('#')[1]))
            except KeyError:
                pass
            f.write('.\n\n')
    f.close()


def _get_display_name(name):
    name_letter = name.split('.')[0].split('_')[1].capitalize()
    if len(name_letter) > 1:
        tmp = ''
        for letter in name_letter:
            if tmp == '':
                tmp = letter
            else:
                tmp = '%s-%s' % (tmp, letter.capitalize())
        name_letter = tmp
    return 'Glossary %s' % name_letter


def _parse_file(in_file_name):
    # dict, key= display name, value = list of lines
    count = 0
    in_file = '%s%s' % (CSV_DIRECTORY, in_file_name)

    with open(in_file, 'rb') as csvfile:
        cvsreader = csv.reader(csvfile, delimiter='$', quotechar='"')
        glossary = {}
        line = None
        links = {}
        for row in cvsreader:
            count = count + 1
            if (count < 2):
                continue
            if row[GLOSSARY_NAME].strip() != '':
                # found new line
                if line != None:
                    # add old line to glossary
                    line[LINKS] = links
                    try:
                        glossary[_get_display_name(line[GLOSSARY_NAME])].append(line)
                    except KeyError:
                        glossary[_get_display_name(line[GLOSSARY_NAME])] = [line]
                line = {}
                links = {}
                line[GLOSSARY_NAME] = row[GLOSSARY_NAME].strip()
                line[LABEL] = row[LABEL].strip()
                line[ALT_LABEL] = row[ALT_LABEL].strip()
                line[DEF] = row[DEF].strip()
                if row[IPCC].strip() != '':
                    line[IPCC] = row[IPCC].strip()

            links[row[LINK].strip()] = row[LINK_TEXT].strip()

        # end of file write last line to dict
        line[LINKS] = links
        glossary[_get_display_name(line[GLOSSARY_NAME])].append(line)
    return glossary
