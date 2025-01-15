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
    prefix = "%s-%s" % (ontology_name, uri)
    out_file_name = "%s-scheme.ttl" % prefix

    date = datetime.now().strftime("%Y-%m-%d")
    out_file = os.path.join(MODEL_DIRECTORY, out_file_name)
    with open(out_file, "w", encoding="utf-8") as ttl_writer:
        # prefixes
        ttl_writer.write(
            "@prefix %s_ontology: <%s> .\n"
            % (ontology_name, ONTOLOGY_MAP[ontology_name])
        )
        ttl_writer.write(
            "@prefix %s: <%s/%s> .\n" % (prefix, SCHEME_MAP[ontology_name], uri)
        )
        ttl_writer.write("@prefix dc: <%s> .\n" % DC)
        ttl_writer.write("@prefix owl: <%s> .\n" % OWL)
        ttl_writer.write("@prefix rdfs: <%s> .\n" % RDFS)
        ttl_writer.write("@prefix skos: <%s> .\n\n\n" % SKOS)

        # add to top scheme
        ttl_writer.write("%s_ontology: a skos:ConceptScheme ;\n" % (ontology_name))
        ttl_writer.write("    skos:hasTopConcept %s: .\n\n" % (prefix))

        # concept scheme
        ttl_writer.write("%s: a skos:ConceptScheme ;\n" % (prefix))
        ttl_writer.write('    skos:prefLabel "%s"@en ;\n' % row[PREF_LABEL])
        ttl_writer.write('    skos:definition "%s"@en ;\n' % _parse(row[DEF]))
        ttl_writer.write('    dc:title "%s" ;\n' % row[PREF_LABEL])
        ttl_writer.write('    dc:rights "%s"@en ;\n' % row[RIGHTS])
        ttl_writer.write('    dc:publisher "%s"@en ;\n' % row[PUBLISHER])
        ttl_writer.write('    rdfs:comment "%s" ;\n' % _parse(row[ABSTRACT]))
        creators = row[CREATOR].split(", ")
        for creator in creators:
            ttl_writer.write('    dc:creator "%s" ;\n' % creator)
        if row[CONTRIBUTOR]:
            contributors = row[CONTRIBUTOR].split(", ")
            for contributor in contributors:
                ttl_writer.write('    dc:contributor "%s" ;\n' % contributor)
        ttl_writer.write('    owl:versionInfo "%s";\n' % row[VERSION])
        ttl_writer.write('    dc:date "%s" ;\n' % date)

        if row[SEE_ALSO]:
            see_also = row[SEE_ALSO].split(", ")
            for also in see_also:
                ttl_writer.write("    rdfs:seeAlso <%s> ;\n" % also)
        ttl_writer.write('    dc:description "%s" ;\n' % _parse(row[DESC]))
        ttl_writer.write("    .\n\n")


def _parse(obj):
    return obj.replace('"', "%22")
