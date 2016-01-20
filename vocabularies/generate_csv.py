import os

from settings import CSV_DIRECTORY, DATA_DIRECTORY, ONTOLOGIES


def generate():
    for ontology in ONTOLOGIES:
        for _file in os.listdir(DATA_DIRECTORY):
            if _file.endswith(".ods") and _file.startswith(ontology):
                cmd = ('soffice --headless --convert-to csv:"Text - txt - csv (StarCalc)":"96,,Unicode (UTF-8),1" --outdir %s %s%s'
                       % (CSV_DIRECTORY, DATA_DIRECTORY, _file))
                os.system(cmd)

if __name__ == "__main__":
    generate()

