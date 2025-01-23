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

## Update a Vocabulary

The vocabularies are generated from a series of `xlsx` files that can be found in the 
[data](data/) directory. See the [README.md](data/README.md) in the [data](data/) directory
for more information.

## Generating the Vocabularies

Ensure the virtual environment has been activated.

```
. venv/bin/activate
```

The call the script.

```
cci-vocab
```

## Updating the Server

To update the triple store on the server you must call the script with the `--deploy` flag.

```
cci-vocab --deploy
```

To update the static pages use the `vocab_upload.sh` script, but first ensure that the value
of `html_dir` in the script is set to the correct value.