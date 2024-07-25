# DEX

Recently I've had a need to be able to execute large batches of requests in a very quick way and record the output of each.

This utility is an attempt to automate a bit of that.

## Installation

Create a virtual directory:

```Shell
python3 -m venv venv
```

Activate the virtual environment and install the package in editable mode.

```Shell
source venv/bin/activate
```

```Shell
pip install -e .
```

This will install the `dex` command line utility in editable mode.

This means that you can make changes to the code and they will be reflected in the command line utility.

