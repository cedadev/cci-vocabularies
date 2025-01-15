import os
from pathlib import Path

import pandas as pd
from vocabularies.settings import CSV_DIRECTORY, DATA_DIRECTORY, ONTOLOGIES


def generate():
    for ontology in ONTOLOGIES:
        # if needed, create a new directory
        Path(CSV_DIRECTORY).mkdir(parents=True, exist_ok=True)
        for _file in os.listdir(os.path.join(DATA_DIRECTORY, ontology)):
            if _file.endswith(".xlsx") and _file.startswith(ontology):
                # read in xlsx file
                read_file = pd.read_excel(os.path.join(DATA_DIRECTORY, ontology, _file))
                out_file = _file.split(".xlsx")[0] + ".csv"

                # export to csv file
                read_file.to_csv(
                    os.path.join(CSV_DIRECTORY, out_file),
                    index=None,
                    header=True,
                    sep="`",
                )


if __name__ == "__main__":
    generate()
