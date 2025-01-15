import csv
import os

from vocabularies.settings import CSV_DIRECTORY, ONTOLOGIES


# columns in spreadsheet
URI = 0
LABEL = 1
ALT_LABEL = 2

URIS = {}
LABELS = {}
ALT_LABELS = {}


def _vailidate_ontology(ontology_name):
    global URIS, LABELS, ALT_LABELS
    URIS = {}
    LABELS = {}
    ALT_LABELS = {}
    in_file = os.path.join(CSV_DIRECTORY, "{}-schemes.csv".format(ontology_name))
    count = 0
    with open(in_file, "r", encoding="utf-8") as csvfile:
        cvsreader = csv.reader(csvfile, delimiter="`", quotechar='"')
        for row in cvsreader:
            count = count + 1
            if count < 2:
                continue
            top_concept_uri = row[URI].strip()
            file_name = "%s-%s" % (ontology_name, top_concept_uri.lower())
            _read_file(file_name)


def _read_file(file_name):
    in_file = os.path.join(CSV_DIRECTORY, "{}.csv".format(file_name))
    with open(in_file, "r", encoding="utf-8") as csvfile:
        cvsreader = csv.reader(csvfile, delimiter="`", quotechar='"')
        count = 0
        for row in cvsreader:
            count = count + 1
            if count < 2:
                continue
            if row[URI] in URIS.keys():
                print(
                    "ERROR: Duplicate URI      - %s : %s : %s"
                    % (URIS[row[URI]], file_name, row[URI])
                )
            else:
                URIS[row[URI]] = file_name

            # if it is from the NERC vocab we only have the URI
            if row[LABEL] in LABELS.keys() and "http://vocab.nerc" not in row[URI]:
                print(
                    "WARNING: Duplicate Label    - %s : %s : %s"
                    % (LABELS[row[LABEL]], file_name, row[LABEL])
                )
            else:
                LABELS[row[LABEL]] = file_name

            if row[ALT_LABEL] in ALT_LABELS.keys() and row[ALT_LABEL] != "":
                print(
                    "WARNING: Duplicate AltLabel - %s : %s : %s"
                    % (ALT_LABELS[row[ALT_LABEL]], file_name, row[ALT_LABEL])
                )
            else:
                ALT_LABELS[row[ALT_LABEL]] = file_name


def vailidate():
    for ontology in ONTOLOGIES:
        _vailidate_ontology(ontology)


if __name__ == "__main__":
    vailidate()
