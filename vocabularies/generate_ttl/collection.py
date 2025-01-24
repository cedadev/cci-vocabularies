import csv
from datetime import datetime
import os
from pathlib import Path

from rdflib.namespace import DC, OWL, RDFS, SKOS

from vocabularies.settings import CSV_DIRECTORY, COLLECTION_MAP, MODEL_DIRECTORY


# columns in spreadsheet
URI = 0
PREF_LABEL = 1
ALT_LABEL = 2
CREATOR = 3
ABSTRACT = 4
DESC = 5
VERSION = 6
PUBLISHER = 7
RIGHTS = 8


def write_ttl(ontology_name):
    # if needed, create a new directory
    Path(MODEL_DIRECTORY).mkdir(parents=True, exist_ok=True)
    in_file = os.path.join(CSV_DIRECTORY, f"{ontology_name}-collections.csv")
    count = 0
    with open(in_file, "r", encoding="utf-8") as csvfile:
        cvsreader = csv.reader(csvfile, delimiter="`", quotechar='"')
        for row in cvsreader:
            count = count + 1
            if count < 2:
                continue
            _write_collection(ontology_name, row)


def _write_collection(ontology_name, row):
    uri = row[URI].strip()
    prefix = f"{ontology_name}-{uri}-collection"
    out_file_name = f"{prefix}.ttl"

    date = datetime.now().strftime("%Y-%m-%d")
    out_file = os.path.join(MODEL_DIRECTORY, out_file_name)
    with open(out_file, "w", encoding="utf-8") as ttl_writer:
        # prefixes
        ttl_writer.write(
            f"@prefix {prefix}: <{COLLECTION_MAP[ontology_name]}{uri}> .\n"
        )
        ttl_writer.write(f"@prefix dc: <{DC}> .\n")
        ttl_writer.write(f"@prefix owl: <{OWL}> .\n")
        ttl_writer.write(f"@prefix rdfs: <{RDFS}> .\n")
        ttl_writer.write(f"@prefix skos: <{SKOS}> .\n\n\n")

        # collection
        ttl_writer.write(
            f"<{COLLECTION_MAP[ontology_name]}{uri}> a skos:Collection ;\n"
        )
        ttl_writer.write(f'    skos:prefLabel "{row[PREF_LABEL]}"@en ;\n')
        ttl_writer.write(f'    skos:definition "{_parse(row[DESC])}"@en ;\n')
        ttl_writer.write(f'    dc:title "{row[PREF_LABEL]}" ;\n')
        ttl_writer.write(f'    dc:rights "{row[RIGHTS]}"@en ;\n')
        ttl_writer.write(f'    dc:publisher "{row[PUBLISHER]}"@en ;\n')
        ttl_writer.write(f'    rdfs:comment "{_parse(row[ABSTRACT])}" ;\n')
        creators = row[CREATOR].split(", ")
        for creator in creators:
            ttl_writer.write(f'    dc:creator "{creator}" ;\n')
        ttl_writer.write(f'    owl:versionInfo "{row[VERSION]}";\n')
        ttl_writer.write(f'    dc:date "{date}" ;\n')
        ttl_writer.write(f'    dc:description "{_parse(row[DESC])}" ;\n')
        ttl_writer.write("    .\n\n")


def _parse(obj):
    return obj.replace('"', "%22")
