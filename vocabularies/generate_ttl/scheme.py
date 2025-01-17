import csv
from datetime import datetime
import os

from rdflib.namespace import DC, OWL, RDFS, SKOS

from vocabularies.settings import (
    SCHEME_MAP,
    CSV_DIRECTORY,
    MODEL_DIRECTORY,
    ONTOLOGY_MAP,
)


# columns in spreadsheet
URI = 0
PREF_LABEL = 1
ALT_LABEL = 2
DEF = 3
SEE_ALSO = 4
CITES = 5
HIERARCHY = 5
CREATOR = 6
CONTRIBUTOR = 7
ABSTRACT = 8
DESC = 9
VERSION = 10
RIGHTS = 12
PUBLISHER = 13


def write_ttl(ontology_name):
    # write out the data for each top concept
    in_file = os.path.join(CSV_DIRECTORY, ontology_name + "-schemes.csv")
    count = 0
    with open(in_file, "r", encoding="utf-8") as csvfile:
        cvsreader = csv.reader(csvfile, delimiter="`", quotechar='"')
        for row in cvsreader:
            count = count + 1
            if count < 2:
                continue
            _write_concept_scheme(ontology_name, row)


def _write_concept_scheme(ontology_name, row):
    uri = row[URI].strip()
    prefix = f"{ontology_name}-{uri}"
    out_file_name = f"{prefix}-scheme.ttl"

    date = datetime.now().strftime("%Y-%m-%d")
    out_file = os.path.join(MODEL_DIRECTORY, out_file_name)
    with open(out_file, "w", encoding="utf-8") as ttl_writer:
        # prefixes
        ttl_writer.write(
            f"@prefix {ontology_name}_ontology: <{ONTOLOGY_MAP[ontology_name]}> .\n"
        )
        ttl_writer.write(f"@prefix {prefix}: <{SCHEME_MAP[ontology_name]}/{uri}> .\n")
        ttl_writer.write(f"@prefix dc: <{DC}> .\n")
        ttl_writer.write(f"@prefix owl: <{OWL}> .\n")
        ttl_writer.write(f"@prefix rdfs: <{RDFS}> .\n")
        ttl_writer.write(f"@prefix skos: <{SKOS}> .\n\n\n")

        # add to top scheme
        ttl_writer.write(f"{ontology_name}_ontology: a skos:ConceptScheme ;\n")
        ttl_writer.write(f"    skos:hasTopConcept {prefix}: .\n\n")

        # concept scheme
        ttl_writer.write(f"{prefix}: a skos:ConceptScheme ;\n")
        ttl_writer.write(f'    skos:prefLabel "{row[PREF_LABEL]}"@en ;\n')
        ttl_writer.write(f'    skos:definition "{_parse(row[DEF])}"@en ;\n')
        ttl_writer.write(f'    dc:title "{row[PREF_LABEL]}" ;\n')
        ttl_writer.write(f'    dc:rights "{row[RIGHTS]}"@en ;\n')
        ttl_writer.write(f'    dc:publisher "{row[PUBLISHER]}"@en ;\n')
        ttl_writer.write(f'    rdfs:comment "{_parse(row[ABSTRACT])}" ;\n')
        creators = row[CREATOR].split(", ")
        for creator in creators:
            ttl_writer.write(f'    dc:creator "{creator}" ;\n')
        if row[CONTRIBUTOR]:
            contributors = row[CONTRIBUTOR].split(", ")
            for contributor in contributors:
                ttl_writer.write(f'    dc:contributor "{contributor}" ;\n')
        ttl_writer.write(f'    owl:versionInfo "{row[VERSION]}";\n')
        ttl_writer.write(f'    dc:date "{date}" ;\n')

        if row[SEE_ALSO]:
            see_also = row[SEE_ALSO].split(", ")
            for also in see_also:
                ttl_writer.write(f"    rdfs:seeAlso <{also}> ;\n")
        ttl_writer.write(f'    dc:description "{_parse(row[DESC])}" ;\n')
        ttl_writer.write("    .\n\n")


def _parse(obj):
    return obj.replace('"', "%22")
