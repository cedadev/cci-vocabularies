import csv
import os

from rdflib.namespace import OWL, RDF, RDFS, SKOS

from vocabularies.settings import CITO, NAME_SPACE_MAP, CSV_DIRECTORY, MODEL_DIRECTORY


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
LINKS = "links"


def write_ttl(in_file_name, out_file_name, class_name, class_label, prefix):
    concept_scheme = f"{class_name}ConceptScheme"
    out_file = os.path.join(MODEL_DIRECTORY, out_file_name)
    with open(out_file, "w", encoding="utf-8") as ttl_writer:
        ttl_writer.write(f"@prefix {prefix}: <{NAME_SPACE_MAP[prefix]}> .\n")
        ttl_writer.write(f"@prefix cito: <{CITO}> .\n")
        ttl_writer.write(f"@prefix owl: <{OWL}> .\n")
        ttl_writer.write(f"@prefix rdf: <{RDF}> .\n")
        ttl_writer.write(f"@prefix rdfs: <{RDFS}> .\n")
        ttl_writer.write(f"@prefix skos: <{SKOS}> .\n\n\n")

        # concept scheme
        ttl_writer.write("#\n")
        ttl_writer.write("# concept scheme\n")
        ttl_writer.write("#\n\n")
        ttl_writer.write(f"{prefix}:{concept_scheme} a skos:ConceptScheme .\n")

        # concepts
        ttl_writer.write("#\n")
        ttl_writer.write("# concepts\n")
        ttl_writer.write("#\n\n")

        glossary = _parse_file(in_file_name)
        for key in glossary.keys():
            for line in glossary[key]:
                ttl_writer.write(
                    f"{prefix}:{line[ALT_LABEL]} a skos:Concept ;\n"
                )  # TODO what to use as uri?
                ttl_writer.write(f"    skos:inScheme {prefix}:{concept_scheme} ;\n")
                ttl_writer.write(f'    skos:prefLabel "{line[LABEL]}"@en ;\n')
                if line[ALT_LABEL] != "":
                    ttl_writer.write(f'    skos:altLabel "{line[ALT_LABEL]}" ;\n')
                if line[DEF] != "":
                    ttl_writer.write(f'    skos:definition "{line[DEF]}"@en ;\n')

                try:
                    citation = line[IPCC]
                except KeyError:
                    citation = None
                if citation == "WGI":
                    ttl_writer.write(
                        "    cito:citesAsSourceDocument <http://www.ipcc.ch/pdf/glossary/ar4-wg1.pdf>;\n"
                    )
                elif citation == "WGII":
                    ttl_writer.write(
                        "    cito:citesAsSourceDocument <http://www.ipcc.ch/pdf/glossary/ar4-wg2.pdf>;\n"
                    )
                elif citation == "WGIII":
                    ttl_writer.write(
                        "    cito:citesAsSourceDocument <http://www.ipcc.ch/pdf/glossary/ar4-wg3.pdf>;\n"
                    )
                elif citation == "WGI (AR4)":
                    ttl_writer.write(
                        "    cito:citesAsSourceDocument <http://www.ipcc.ch/>;\n"
                    )  # TODO find ref
                elif citation:
                    print(f"unknown citation {citation}")
                try:
                    links = line[LINKS]
                    keys = links.keys()
                    sorted_keys = sorted(keys)
                    for key in sorted_keys:
                        if key.startswith("http"):
                            ttl_writer.write(f"    rdfs:seeAlso <{key}> ;\n")
                        elif key:
                            ttl_writer.write(
                                f'    rdfs:seeAlso {prefix}:{key.split("#")[1]} ;\n'
                            )
                except KeyError:
                    pass
                ttl_writer.write(".\n\n")


def _get_display_name(name):
    name_letter = name.split(".")[0].split("_")[1].capitalize()
    if len(name_letter) > 1:
        tmp = ""
        for letter in name_letter:
            if tmp == "":
                tmp = letter
            else:
                tmp = f"{tmp}-{letter.capitalize()}"
        name_letter = tmp
    return f"Glossary {name_letter}"


def _parse_file(in_file_name):
    # dict, key= display name, value = list of lines
    count = 0
    in_file = f"{CSV_DIRECTORY}{in_file_name}"

    with open(in_file, "r", encoding="utf-8") as csvfile:
        cvsreader = csv.reader(csvfile, delimiter="$", quotechar='"')
        glossary = {}
        line = None
        links = {}
        for row in cvsreader:
            count = count + 1
            if count < 2:
                continue
            if row[GLOSSARY_NAME].strip() != "":
                # found new line
                if line is not None:
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
                if row[IPCC].strip() != "":
                    line[IPCC] = row[IPCC].strip()

            links[row[LINK].strip()] = row[LINK_TEXT].strip()

        # end of file write last line to dict
        line[LINKS] = links
        glossary[_get_display_name(line[GLOSSARY_NAME])].append(line)
    return glossary
