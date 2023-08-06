[![Build Status](https://travis-ci.org/iiddoo/python-sample-package.svg?branch=master)](https://travis-ci.org/iiddoo/python-sample-package)             [![PyPI version](https://badge.fury.io/py/python-sample-package.svg)](https://badge.fury.io/py/python-sample-package)           [![Coverage Status](https://coveralls.io/repos/github/iiddoo/python-sample-package/badge.svg?branch=dev)](https://coveralls.io/github/iiddoo/python-sample-package?branch=dev)          [![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)


# python-example-package

This is a starter repo for creating a new python package.

## Tests

Simply run: `pytest`


## Code coverge

Generate coverage report with: `py.test --cov=myPackage tests/`

####  script:
####    - pip install --user --upgrade setuptools wheel twine numpy
####    - python3 setup.py sdist bdist_wheel
####    - python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
####  before_script:
####    - bumpversion minor setup.py