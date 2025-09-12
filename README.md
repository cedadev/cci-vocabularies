# cci-vocabularies

Representation of ESA CCI vocabularies in SKOS and OWL

**Latest Update 30/05/2025** This repository is now `pre-built` before being updated in rancher. To update this repository, make any changes to data files as normal, then run the `cci-vocab` command. This will auto-generate all necessary static webpages based on your changes. You can then recommit the `app/` folder which contains those newly built files, as well as your other changes. Once these changes have all been committed, the repository can be redeployed on the Kubernetes staging cluster by going to `gitlab.ceda.ac.uk/cedadev/cci-vocab-server` and updating the commit hash used by the Dockerfile.

Alternatively for a more standardised deployment regiment, create a git release at `github.com/cedadev/cci-vocabularies`, following the format vX.Y.Z where:
- Z is for small bug fixes/typos/syntax issues
- Y is for added content (new entries in spreadsheets etc.)
- X is for 'version-breaking' changes, eg the addition of a brand new facet or a whole new page of links.

The release tag can then be used in place of a commit hash in the Dockerfile for both `vocab` and `triplestore`. See the Gitlab repo for more details on deployment to Kubernetes. (Note: Deployment to OTC in 2025 will be a manual process - see the `gitlab.ceda.ac.uk/cci-odp/otc-helm-charts` repo for details.)

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

Then run the command to generate all vocab server content.

```
cci-vocab
```

This will create all changes required to the `app/` files which are then served in the deployment on rancher (when this repository version is used.)
All app files should now be committed to the main repository, simply perform:

```
git add app/
git commit -m "Update message for what has changed with source files"
```

## Updating the Vocab Server

Redeploy the vocab server application via Gitlab (to either the rancher cluster or OTC):
- Test locally before any deployments can happen:

- Create a github release (vX.X.X) for your new version. Click on 'releases' to the right of this window on the front page of the repo and follow instructions for creating a new release.

- On gitlab, in the `.gitlab-ci.yml` file, set the APP_VERSION to your new release (note: GIT VERSION adds the `v` so you just set the number for APP_VERSION.

- Push to gitlab and the staging version will be redeployed with your changed version.

- Contact Daniel Westwood or Rhys Evans for deployment to OTC as the process is more involved.
