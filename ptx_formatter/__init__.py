"""
# PtxFormatter

PtxFormatter is an opinionated but customizable formatter for PreText. It can be used as a command-line tool or as a Python library.

## Installation

Easiest way to get started is to grab the newest version with [pipx](https://pipx.pypa.io/stable/):

```shell
pipx install --python 3.12 --fetch-missing-python git+https://github.com/skiadas/ptx-formatter.git
```
Or grab a wheel URL from our [releases page](https://github.com/skiadas/ptx-formatter/releases) and use that instead:
```shell
pipx install --python 3.12 --fetch-missing-python https://github.com/skiadas/ptx-formatter/releases/download/v0.0.2b/ptx_formatter-0.0.2-py3-none-any.whl
```

You should now have a command ready to use:
```shell
ptx-format --version
ptx-format --help
```

For alternative installations, wheels and tarballs are available from the [releases page](https://github.com/skiadas/ptx-formatter/releases). You can install them for example with:

```shell
pip install --user url_to_wheel
```
You will need to be running Python 3.12 or newer, and will need to add the dependencies.

## Command line Usage

You can use `ptx-format` with standard input and output, like so:
```shell
ptx-format < inputFile.ptx   > outputFile.ptx
```
You can also specify one or both files as arguments:
```shell
ptx-format -f inputFile.ptx -o outputFile.ptx
```

The command allows a number of options. See also `ptx-format --help`.

### Options

* `--add-doc-type / --skip-doc-type`: Whether to include or skip the XML doc identifier <?xml ...>. The identifier will by default be added if the output is a file and skipped if the output is stdout.
* `-f, --file FILENAME`: File to use as input. If omitted, read the contents of standard input.
* `-o, --output FILENAME`: File to use as output. If omitted, write the results to standard output.
* `-i, --indent INTEGER`: Number of characters for space-indent. Overwrites the standard configuration. Ignored if tab_indent is set.
* `-t, --tab-indent`: Indent using tabs instead. Overwrites the standard configuration.
* `-c, --config-file FILENAME`: File to use as configuration. If omitted, a standard configuration file is loaded.
* `--show-config`: Print the current configuration and exit. This is in a TOML form that could be saved to a file and used as a start file.
* `--version`: Print the version and exit.
* `--help`: Show this message and exit.


## Basic API usage

You simply need to import `formatPretext` and provide it with a
the source string. It returns the formatted string.

```python
from ptx_formatter import formatPretext

s = formatPretext(source)
print(s)
```

### API Configuration

You can customize the output further by providing a `Config`
object, likely created by calling the `Config.fromFile` method.

Configurations can be stored to and loaded from [TOML](https://toml.io/en/)
format files. An example file is produced by the `Config.print` function.

The following entries are expected/allowed:

- `indent`, with value a number of spaces or a string to use for indent
- `include-doc-id`, a boolean to specify whether the document
  identifier should be included or not
- `tags`, a table whose entry keys are specific tag classifications
  (see just below) and whose values are arrays of the tags belonging
  to that classification. Only tags that need to be handled in a certain
  way need to be included. The allowed classifications are:
  - `verbatim` for tags whose contents are to be rendered verbatim
  - `inline` for tags that are to be inlined
  - `inline-empty` for tags that are to be inline only when empty
  - `block` for tags that are to be rendered in block mode
  - `block-no-indent` for tags that are to be rendered in block
    mode but that don't increase the indent level for their contents.

"""

from ptx_formatter.formatter import formatPretext, Config

__all__ = [formatPretext, Config]
