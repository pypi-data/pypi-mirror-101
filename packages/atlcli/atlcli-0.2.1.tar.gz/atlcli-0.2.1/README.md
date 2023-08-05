# Altassian CLI
## Introduction
Altassian CLI is a Atlassian product CLI that allows you to create release notes, get infos about the repositories and repositories.

## Requirements
* Python 3.+
* Virtualenv
* PIP 3+

## Project setup

In order to run the project you will first need to create a Virtual environment in python by running the following command.

```
pip install virtualenv
mkdir venv
python3 -m virtualenv ./venv
cd venv/bin
source activate
pip install -r requirements.txt
```

## Installing locally
```
pip install . # While in root of project
```

## Concourse
```yaml
- task: generate release note
    config:
      platform: linux
      image_resource:
        type: docker-image
        source:
          repository: <repository link here>
      run:
        path: /bin/sh
        args:
          - -c
          - |            
            atlcli --help

```
## Usage
A guide for the tool can be found on the [Usage](./doc/Usage.md) page.

## Features
* Note de livraison qui affiche les etapes de livraison (comme les notes de livraison mpm)
* Changelog
* Conversion de wiki markup a storage format et ajout des checklist manquante


### Addding pip dependencies
After adding a new module to the project you will need to update the requirements.txt file in order for it to have the new module. You cand do this by running the following command.

```
pip freeze > requirements.txt
```
## Troubleshoot

Add trusted-host files.pythonhosted.org to pip if you have issues with cert validation if you are behind a proxy.
```
pip config set global.trusted-host "pypi.org files.pythonhosted.org pypi.python.org"
```
## Doc
https://pypi.org/project/atlassian-python-api/
https://click.palletsprojects.com/en/7.x/
https://confluence.atlassian.com/doc/macros-139387.html
https://confluence.atlassian.com/doc/confluence-wiki-markup-251003035.html

# Note
This software is still under development. For feature requests please open up an Issue. I can't guarantee I will be able to work on it.

# License

Copyright (c) 2021 Joshua Ghali. All rights reserved.

Licensed under the [MIT](./LICENSE) license.