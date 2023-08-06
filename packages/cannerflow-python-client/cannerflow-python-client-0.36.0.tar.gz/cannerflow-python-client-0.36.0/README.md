![pypi](https://img.shields.io/pypi/v/cannerflow-python-client.svg)

# Introduction

This package provides a client interface to query Cannerflow
a distributed SQL engine. It supports Python 3.6.x, 3.7.x, and 3.8.x.

# Installation

```
$ pip install cannerflow-python-client
```

# Quick Start

## Client

As client to use the `cannerflow-python-client` package.

```python
import cannerflow

client = cannerflow.client.bootstrap(
    endpoint="http://localhost:3000",
    workspace_id=WORKSPACE_ID,
    headers={
        'X-CANNERFLOW-SECRET': JUPYTER_SECRET,
        'X-CANNERFLOW-WORKSPACE-ID': WORKSPACE_ID
    }
)
queries = client.list_saved_query()
query = client.use_saved_query('region')
raws = query.get_all()
```

# Development Need

If you would like to download the source code and develop new feature or fix bug, please follow the guide below to build development environment.

# Prerequisite

Before you build development environment, please make sure we prepared the python version we supported and [poetry](https://python-poetry.org/) package which the python package and dependency management tools.

## Python version

We support python version `3.6.x`, `3.7.x` and `3.8.x`, if you use the `pyenv`(https://github.com/pyenv/pyenv) to management different python version, please make sure you have switch to the version we supported.

## 1. Install Poetry

```sh
$> pip install poetry
$> poetry about

Poetry - Package Management for Python

Poetry is a dependency manager tracking local dependencies of your projects and libraries.
See https://github.com/python-poetry/poetry for more information.
```

## 2. Setup virtual environment and install packages by poetry

Using the poetry to build virtual environment and install the required package which `pyproject.toml` records.

```sh
$> cd cannerflow-python-client
cannerflow-python-client $> poetry install      # install development required packages, will update poetry.lock and create .venv directory
cannerflow-python-client $> poetry shows        # show the required packages installed
cannerflow-python-client $> poetry shows --tree # check the packages installed with dependencies
cannerflow-python-client $> poetry shell        # enter virtual environments
(.venv) cannerflow-python-client $>
```

## 3. Run testing files to test results

### 3.1 Setup Environment variable.

The tests code put int `tests/` and you need to setup three environment variable, you could check the meaning from [Development - Python Client)[https://flow.cannerdata.com/docs/integration/development_python].

There are two method you could setup `WORKSPACE_ID`, `ENDPOINT` and `CANNERFLOW_PERSONAL_ACCESS_TOKEN`.

#### Setup Environment by `export`

Here is the **example**.

```sh
export WORKSPACE_ID="2fae9bf7-a883-4f25-9566-c0d379c44440"
export ENDPOINT="http://localhost:3000"
export CANNERFLOW_PERSONAL_ACCESS_TOKEN="Y2xpZW50Xzk5ODZmYjMyLTUyYTItNGE5Mi05ZDkxLTFlMzdjNzhiMGE0NjplNmQ2OWQ0ZDJmODc3ZWQwOGI2ZTQyNTk0ZmYxZDM0Mg="
```

#### Setup Environment by `pytest.ini`

There is another way to setup that change the environment variable by edit `env` key in `pytest.ini`.

```ini
[pytest]
env =
    ENDPOINT=http://localhost:3000
    WORKSPACE_ID=9abc63f8-50bb-46a3-aea5-804b6d0d3fa3
    CANNERFLOW_PERSONAL_ACCESS_TOKEN=Y2xpZW50Xzk5ODZmYjMyLTUyYTItNGE5Mi05ZDkxLTFlMzdjNzhiMGE0NjplNmQ2OWQ0ZDJmODc3ZWQwOGI2ZTQyNTk0ZmYxZDM0Mg=
```

### 3.2 Run tests by `pytest` command

You could run test cases by `pytest`.

```sh
(.venv) cannerflow-python-client $> pytest
# Run pytest to test Specific file.
(.venv) cannerflow-python-client $> pytest tests/test_client.py
```

Or you could run tests by python.

```sh
(.venv) cannerflow-python-client $> python -m pytest tests
```

## Publish

After you finished the development and would like to publish to remote repository like [pypi](https://pypi.org/project/cannerflow-python-client/).

```sh
# Update version in __init__.py
vim cannerflow/__init__.py
# Removed old distribution
rm -rf dist
# Build source distribution (please follow the more detail about setuptools document)
python setup.py sdist
# upload to pypi and type account & password
twine upload dist/*
```
