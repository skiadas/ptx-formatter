# PtxFormatter

PtxFormatter is an opinionated but customizable formatter for PreText. It can be used as a command-line tool or as a Python library.

## Installation

A wheel and tarball are available. You can install them with:

```shell
pip install --user path_to_wheel
```

TODO: Add pipx instructions

You should now have a command ready to use:
```shell
ptx-format --version
ptx-format --help
```

## Usage

### As a Python library

You can use the ptx formatter in other Python code by adding the package as a dependency with your favorite package manager. Then in your code you can do:
```python
from ptx_formatter import formatPretext
```
See the documentation pages for details.

### From command line

You can use `ptx-format` with standard input and output, like so:
```shell
ptx-format < inputFile.ptx   > outputFile.ptx
```
You can also specify one or both files as arguments:
```shell
ptx-format -f inputFile.ptx -o outputFile.ptx
```

The command allows a number of options. See also `ptx-format --help`.

#### Options

* `--add-doc-type / --skip-doc-type`: Whether to include or skip the XML doc identifier <?xml ...>. The identifier will by default be added if the output is a file and skipped if the output is stdout.
* `-f, --file FILENAME`: File to use as input. If omitted, read the contents of standard input.
* `-o, --output FILENAME`: File to use as output. If omitted, write the results to standard output.
* `-i, --indent INTEGER`: Number of characters for space-indent. Overwrites the standard configuration. Ignored if tab_indent is set.
* `-t, --tab-indent`: Indent using tabs instead. Overwrites the standard configuration.
* `-c, --config-file FILENAME`: File to use as configuration. If omitted, a standard configuration file is loaded.
* `--show-config`: Print the current configuration and exit. This is in a TOML form that could be saved to a file and used as a start file.
* `--version`: Print the version and exit.
* `--help`: Show this message and exit.

