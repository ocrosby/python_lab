# Python

## Overview

This document contains miscellaneous notes about the Python language.

### Python 3.12

Python 3.12 is the latest version of the Python programming language. It was released on October 4, 2021.

#### Installing Python 3.12

```shell
brew install python@3.12
```

After installing Python 3.12 you will need to update your `PATH` environment variable to include the new Python installation.

```shell
export PATH="/usr/local/opt/python@3.12/bin:$PATH"
```

## PYTHONPATH

The PYTHONPATH environment variable is a list of directories that the Python interpreter will search for modules 
when importing them. It is similar to the PATH environment variable, which tells the shell where to look for executable files.

## Creating a virtual environment for a project

```shell
python3.12 -m venv venv
```

## Activating a virtual environment

```shell
source venv/bin/activate
```

## Deactivating a virtual environment

```shell
deactivate
```

### Python 3.12 Features

- [PEP 679 -- Literal types](https://peps.python.org/pep-0679/)
- [PEP 681 -- Syntactic sugar for specifying types](https://peps.python.org/pep-0681/)
- [PEP 682 -- Pattern matching](https://peps.python.org/pep-0682/)
- [PEP 684 -- Union operators in `typing`](https://peps.python.org/pep-0684/)
- [PEP 685 -- More precise Typing for `isinstance`](https://peps.python.org/pep-0685/)
- [PEP 686 -- Precise line numbers for debugging and other tools](https://peps.python.org/pep-0686/)