A collection of useful utilities shared a cross a number of [Bits In Glass](https://www.bitsinglass.com) projects.

### What is this repository for? ###

This repository a collection of useful, common utilities used over and over again in a number of 
[BIG](https://www.bitsinglass.com) projects.

This is a library to be included in other projects.

### How do I get set up? ###

Dependencies should be installed automatically (they are listed in the `setup.py` file), but here is the `pip` 
command for those who like to do things manually:

    pip install --upgrade pyjwt wheel toml PyYAML dacite

To run the unit tests, you will need additional dependencies:

    pip install --upgrade pytest pytest-mock

Alternatively, run those commands from the project root directory:

    pip install --upgrade -r requirements.txt
    pip install --upgrade -r test-requirements.txt

To run unit tests (using `pytest`), execute the following command from the project root directory:

    pytest -v tests/*
