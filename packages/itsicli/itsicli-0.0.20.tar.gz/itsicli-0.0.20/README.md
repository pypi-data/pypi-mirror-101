# The ITSI Command Line Interface (CLI)

## Setup Virtualenv


```
python3 -m venv /path/to/new/virtual/environment

source /path/to/new/virtual/environment/bin/activate
```


## Using "itsi-content-pack"

The `itsi-content-pack` command that is shipped with the Python package assists in creating and managing ITSI Content Packs.

The general end-to-end workflow is as follows and example provided in each step:
### Initialize content pack
If you are just creating the content pack, not updating the itsi cli and itsi models
you can just install the newest package
```
pip install --upgrade itsicli
pip install --upgrade itsimodels
```
If you are developing on the itsi cli and itsi models
update PYTHON path to include `itsi-models` and `itsi-cli` folders to utilize your local changes
update PATH to `itsi-cli/bin` so we can invoke `itsi-content-pack` command from anywhere
```
export PYTHONPATH=<path to repo itsi-cli>:<path to repo itsi-models>
export PATH=$PATH:<path to repo itsi-cli/bin>
```
### Create a directory to hold content pack files
This folder will be referred to as `CP_BASE_DIR`. The name of the folder should be the same as the content pack id and
start with `DA-ITSI-CP-`.
```
mkdir DA-ITSI-CP-mycontentpack
cd DA-ITSI-CP-mycontentpack
```
### Initialize content pack app
Inside DA-ITSI-CP-* that you just created, initialize **itsi-content-pack** with `init`
```
itsi-content-pack init
```
Follow the prompt to provide a content pack id and title. Please prefix id with `DA-ITSI-CP-`. Once completed,
three directory will be created
- itsi
- default
- appserver
### Create a Content Pack
Once the content pack is initialized, we can create actual objects for this content pack other than the three directories above. 
We add objects in json format grouped in subdirectory by object types. 
However, objects could also optionally be imported from an ITSI backup file
```
itsi-content-pack importbackup path-to-backup-zip-file
```
### Continue to add, remove, or edit content from the Content Pack
You can add or remove objects inside each object type directory, make sure to update manifest.json as part of your changes.
### Add any supporting Splunk knowledge objects
This DA-ITSI-CP-* is a Splunk app, so feel free to add lookups, transforms, props, etc that are Splunk compatible.
### Validate the Content Pack through the `validate` command
Inside DA-ITSI-CP-*, run following command to validate if this content pack is compatible with ITSI.
```
itsi-content-pack validate
```
1. Submit the Content Pack to either:
    - Splunkbase (must first run the `build` command)
    - The ITSI Content Library via a pull request on Github repo: itsi-content


## Build the distribution archive

:exclamation: __Please build the package on linux box__

Install the build dependencies:
```
pip install --upgrade setuptools wheel
```

### Generate the Python package
Clean up distribution:
```
make clean
```

Generate the Python distribution archive:
```
make
```

### Upload to the Python Package Index

Install the dependencies required for uploading to the index:

```
pip install --upgrade twine
```

Upload to PyPI:

```
make upload
```

## Troubleshooting

Log file name:
```
itsi_contentpacks_itsicli.log
itsi_contentpacks_itsimodels.log
```

If you have $SPLUNK_HOME environment set, then you can find the log file in:
```
$SPLUNK_HOME/var/log/splunk/
```
Otherwise, you will find the log file in ```~/```