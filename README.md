# cci-vocabularies

Representation of ESA CCI vocabularies in SKOS and OWL


The script `cci-vocab` generates the CCI vocabularies from a series of `xlsx` documents. 
The output is various representations of the vocabularies including html pages.


## Installation

It is recommended to install the code in a virtual environment.

```
python3 -m venv venv
. venv/bin/activate
pip install git+https://github.com/cedadev/cci-vocabularies.git
```

## Running the Script

Ensure the virtual environment has been activated.

```
. venv/bin/activate
```

The call the script.

```
cci-vocab
```

## Updating the Server

To update the triple store on the sterver you must call the script with the `--deploy` flag.

```
cci-vocab --deploy
```

To update the static pages use the `vocab_upload.sh` script, but first update the value of `html_dir` in the script.