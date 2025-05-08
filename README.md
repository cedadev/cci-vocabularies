# cci-vocabularies

Representation of ESA CCI vocabularies in SKOS and OWL


The script `cci-vocab` generates the CCI vocabularies from a series of `xlsx` documents. 
The output is various representations of the vocabularies including html pages.


## Installation

It is recommended to install the code in a virtual environment.

```
python3 -m venv venv
. venv/bin/activate
git clone https://github.com/cedadev/cci-vocabularies.git
pip install -e cci-vocabularies
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

Set the following parameters: (from inside the `cci-vocabularies` repo)

```
export BASE_PATH=$PWD/vocabularies
export DEPLOY_PATH=$PWD/app
```

Then run the command to generate all vocab server content.

```
cci-vocab
```

All app files should now be committed to the main repository, simply perform:

```
git add $DEPLOY_PATH
git commit -m "Update message for what has changed with source files"
```

## Updating the Vocab Server

Redeploy the vocab server application via Gitlab (to either the rancher cluster or OTC) with the new commit hash from your new version, which should be inserted into the Dockerfile as the new image version.