import os,subprocess

from settings import CSV_DIRECTORY, DATA_DIRECTORY, ONTOLOGIES

import platform


def generate():
    if platform.system() == "Linux":
        soffice = "soffice"
    elif platform.system() == "Darwin":
        soffice = "/Applications/LibreOffice.app/Contents/MacOS/soffice"
    else:
        #soffice = '"C:\Program Files (x86)\OpenOffice 4\program\soffice.exe"'
        soffice = '"C:\Program Files\LibreOffice\program\soffice.exe"'

    for ontology in ONTOLOGIES:
        print(DATA_DIRECTORY)
        print(CSV_DIRECTORY)
        for _file in os.listdir(os.path.join(DATA_DIRECTORY, ontology)):
            if _file.endswith(".ods") and _file.startswith(ontology):
                print _file
                cmd = (
                    '%s --headless --convert-to csv:"Text - txt - csv'
                    ' (StarCalc)":"96,,76,1" --outdir %s %s'
                    % (
                        soffice,
                        CSV_DIRECTORY,
                        os.path.join(DATA_DIRECTORY, ontology, _file),
                    )
                )
                #os.system(cmd)
                subprocess.call(cmd)


                

if __name__ == "__main__":
    generate()
