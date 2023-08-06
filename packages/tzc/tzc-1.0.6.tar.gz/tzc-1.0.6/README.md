# tzc - time zone convert

[![PyPI](https://img.shields.io/pypi/v/tzc.svg)](https://pypi.org/project/tzc/)
[![Changelog](https://img.shields.io/github/v/release/rstms/tzc?include_prereleases&label=changelog)](https://github.com/rstms/tzc/releases)
[![Tests](https://github.com/rstms/tzc/workflows/Test/badge.svg)](https://github.com/rstms/tzc/actions?query=workflow%3ATest)
[![License](https://img.shields.io/github/license/rstms/tzc)](https://github.com/rstms/tzc/blob/master/LICENSE)

copies input to output, converting timezone in any lines beginning with an ISO-8601 timestamp

## Installation

Install this tool using `pip`:

    $ pip install tzc

## Usage
```
Usage: tzc [OPTIONS] [INPUT_FILE] [OUTPUT_FILE]

  copy input to output, converting timezone in any lines starting with a
  timestamp

Options:
  --version               Show the version and exit.
  -i, --input-zone TEXT   timezone in file
  -o, --output-zone TEXT  output timezone
  -f, --format TEXT       output format (strptime)
  -s, --short             format output as YYYY-MM-DD HH:MM:SS
  --help                  Show this message and exit.
```

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd tzc
    python -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
