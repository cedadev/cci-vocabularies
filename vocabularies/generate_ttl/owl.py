import csv
from datetime import datetime
import os

from rdflib.namespace import DC, OWL, RDF, RDFS, SKOS

from vocabularies.settings import CSV_DIRECTORY, MODEL_DIRECTORY, ONTOLOGY_MAP


# columns in spreadsheet
C_URI = 0
C_LABEL = 1
C_DEF = 3
C_SEE_ALSO = 4

# columns in ontology spreadsheet
URI = 0
TITLE = 0
RIGHTS = 1
PUBLISHER = 2
LABEL = 3
CREATOR = 4
CONTRIBUTOR = 5
DEF = 6
DESC = 7
VERSION = 8
SEE_ALSO = 9


def write_ttl(ontology_name):
    date = datetime.now().strftime("%Y-%m-%d")
    # write out the top concepts
    out_file_name = f"{ontology_name}-ontology.ttl"
    out_file = os.path.join(MODEL_DIRECTORY, out_file_name)
    with open(out_file, "w", encoding="utf-8") as ttl_writer:
        # prefixes
        ttl_writer.write(
            f"@prefix {ontology_name}: <{ONTOLOGY_MAP[ontology_name]}> .\n"
        )
        ttl_writer.write(f"@prefix dc: <{DC}> .\n")
        ttl_writer.write(f"@prefix owl: <{OWL}> .\n")
        ttl_writer.write(f"@prefix rdf: <{RDF}> .\n")
        ttl_writer.write(f"@prefix rdfs: <{RDFS}> .\n")
        ttl_writer.write(f"@prefix skos: <{SKOS}> .\n\n\n")

        _write_ontology(ontology_name, date, ttl_writer)
        _write_classes(ontology_name, ttl_writer)


def _write_ontology(ontology_name, date, f):
    in_file_name = f"{ontology_name}-ontology.csv"
    in_file = os.path.join(CSV_DIRECTORY, in_file_name)
    count = 0

    # ontology
    f.write("#\n")
    f.write("# ontology\n")
    f.write("#\n\n")

    with open(in_file, "r", encoding="utf-8") as csvfile:
        cvsreader = csv.reader(csvfile, delimiter="`", quotechar='"')
        for row in cvsreader:
            count = count + 1
            if count < 2:
                # header
                continue
            f.write(f"<{ONTOLOGY_MAP[ontology_name]}> a owl:Ontology ;\n")
            f.write(f'    dc:title "{row[TITLE]}" ;\n')
            f.write(f'    dc:rights "{row[RIGHTS]}"@en ;\n')
            f.write(f'    dc:publisher "{row[PUBLISHER]}"@en ;\n')
            f.write(f'    rdfs:comment "{_parse(row[DEF])}" ;\n')
            f.write(f'    rdfs:label "{_parse(row[LABEL])}" ;\n')

            # ontology
            creators = row[CREATOR].split(", ")
            for creator in creators:
                f.write(f'    dc:creator "{creator}" ;\n')
            if row[CONTRIBUTOR]:
                contributors = row[CONTRIBUTOR].split(", ")
                for contributor in contributors:
                    f.write(f'    dc:contributor "{contributor}" ;\n')
            f.write(f'    owl:versionInfo "{row[VERSION]}";\n')
            f.write(f'    dc:date "{date}" ;\n')

            if len(row) > SEE_ALSO and row[SEE_ALSO]:
                see_also = row[SEE_ALSO].split(", ")
                for also in see_also:
                    f.write(f"    rdfs:seeAlso <{also}> ;\n")
            f.write(f'    dc:description "{_parse(row[DESC])}" ;\n')
            f.write("    .\n\n")
            return


def _write_classes(ontology_name, f):
    in_file_name = f"{ontology_name}-schemes.csv"
    in_file = os.path.join(CSV_DIRECTORY, in_file_name)
    count = 0

    # classes
    f.write("#\n")
    f.write("# classes\n")
    f.write("#\n\n")

    with open(in_file, "r", encoding="utf-8") as csvfile:
        cvsreader = csv.reader(csvfile, delimiter="`", quotechar='"')
        for row in cvsreader:
            count = count + 1
            if (count < 2) or row[C_URI].strip() == "":
                # header
                continue
            f.write(f"<{ONTOLOGY_MAP[ontology_name]}{row[C_URI]}> a owl:Class ;\n")
            f.write(f"    rdfs:isDefinedBy <{ONTOLOGY_MAP[ontology_name]}> ;\n")
            f.write(f'    rdfs:label "{_parse(row[C_LABEL])}" ;\n')
            if len(row) > C_SEE_ALSO and row[C_SEE_ALSO]:
                see_also = row[C_SEE_ALSO].split(", ")
                for also in see_also:
                    f.write(f"    rdfs:seeAlso <{also}> ;\n")
            f.write(f'    dc:description "{_parse(row[C_DEF])}" ;\n')
            f.write("    .\n\n")


def _parse(obj):
    return obj.replace('"', "%22")
