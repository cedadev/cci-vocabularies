import os

from settings import CSV_DIRECTORY, DATA_DIRECTORY, ONTOLOGIES

import platform


def generate():
    if platform.system() == 'Linux':
        soffice = 'soffice'
    elif platform.system() == 'Darwin':
        soffice = '/Applications/LibreOffice.app/Contents/MacOS/soffice'

    for ontology in ONTOLOGIES:
        for _file in os.listdir(os.path.join(DATA_DIRECTORY, ontology)):
            if _file.endswith(".ods") and _file.startswith(ontology):
                cmd = ('%s --headless --convert-to csv:"Text - txt - csv'
                       ' (StarCalc)":"96,,Unicode (UTF-8),1" --outdir %s %s'
                       % (soffice, CSV_DIRECTORY,
                          os.path.join(DATA_DIRECTORY, ontology, _file)))
                os.system(cmd)


if __name__ == "__main__":
    generate()
