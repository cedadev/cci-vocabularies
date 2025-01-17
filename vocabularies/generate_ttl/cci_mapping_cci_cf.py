import csv
import os

from rdflib.namespace import SKOS

from vocabularies.settings import CCI, CSV_DIRECTORY, COLLECTION_MAP, MODEL_DIRECTORY


# columns in spreadsheet
CCI_URI = 0
CF_URI = 2


def write_ttl(in_file_name, out_file_name):
    out_file = os.path.join(MODEL_DIRECTORY, out_file_name)
    with open(out_file, "w", encoding="utf-8") as ttl_writer:
        ttl_writer.write(f"@prefix {CCI}: <{COLLECTION_MAP[CCI]}ecv/> .\n")
        ttl_writer.write(f"@prefix skos: <{SKOS}> .\n\n\n")

        cci_project = None
        count = 0
        in_file = os.path.join(CSV_DIRECTORY, in_file_name)
        with open(in_file, "r", encoding="utf-8") as csvfile:
            csvreader = csv.reader(csvfile, delimiter="`", quotechar='"')
            for row in csvreader:
                count = count + 1
                if count < 2:
                    continue

                if row[CCI_URI] != "":
                    cci_project = row[CCI_URI].strip()
                if (not row[CF_URI] == "") and (not row[CF_URI].startswith("?")):
                    ttl_writer.write(f"{CCI}:{cci_project} a skos:Concept ;\n")
                    ttl_writer.write(
                        f"    skos:narrowMatch <{row[CF_URI].strip()}> .\n\n"
                    )
