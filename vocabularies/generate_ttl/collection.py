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


def write_ttl(ontology_name):
    # if needed, create a new directory
    Path(MODEL_DIRECTORY).mkdir(parents=True, exist_ok=True)
    in_file = os.path.join(CSV_DIRECTORY, "{}-collections.csv".format(ontology_name))
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
    prefix = "%s-%s-collection" % (ontology_name, uri)
    out_file_name = "%s.ttl" % prefix

    date = datetime.now().strftime("%Y-%m-%d")
    out_file = os.path.join(MODEL_DIRECTORY, out_file_name)
    with open(out_file, "w", encoding="utf-8") as ttl_writer:
        # prefixes
        ttl_writer.write(
            "@prefix %s: <%s%s> .\n" % (prefix, COLLECTION_MAP[ontology_name], uri)
        )
        ttl_writer.write("@prefix dc: <%s> .\n" % DC)
        ttl_writer.write("@prefix owl: <%s> .\n" % OWL)
        ttl_writer.write("@prefix rdfs: <%s> .\n" % RDFS)
        ttl_writer.write("@prefix skos: <%s> .\n\n\n" % SKOS)

        # collection
        ttl_writer.write(
            "<%s%s> a skos:Collection ;\n" % (COLLECTION_MAP[ontology_name], uri)
        )
        ttl_writer.write('    skos:prefLabel "%s"@en ;\n' % row[PREF_LABEL])
        ttl_writer.write('    skos:definition "%s"@en ;\n' % _parse(row[DESC]))
        ttl_writer.write('    dc:title "%s" ;\n' % row[PREF_LABEL])
        ttl_writer.write('    dc:publisher "%s"@en ;\n' % row[PUBLISHER])
        ttl_writer.write('    rdfs:comment "%s" ;\n' % _parse(row[ABSTRACT]))
        creators = row[CREATOR].split(", ")
        for creator in creators:
            ttl_writer.write('    dc:creator "%s" ;\n' % creator)
        ttl_writer.write('    owl:versionInfo "%s";\n' % row[VERSION])
        ttl_writer.write('    dc:date "%s" ;\n' % date)
        ttl_writer.write('    dc:description "%s" ;\n' % _parse(row[DESC]))
        ttl_writer.write("    .\n\n")


def _parse(obj):
    return obj.replace('"', "%22")
