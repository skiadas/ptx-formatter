# PtxFormatter

PtxFormatter is a formatter for PreText, based on a translation of the code in the [https://github.com/oscarlevin/pretext-tools](PreText-tools) VSCode extension.

## Installation

A wheel and tarball are available. You can install them with:

```shell
pip install --user path_to_wheel
```

TODO: pipx

You should now have a command ready to use:
```shell
ptx-format --version
ptx-format --help
```

TODO: Figure out how to make autocompletion work

## Usage

### As a Python library

TODO

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

- `--indent n` or `-i n` sets the amount of indent to the specified number `n`. The default is 2.
- `--tab-indent` or `-t` switches to using tabs for indentation. The default is to use spaces.
- `--file filename` or `-f filename` sets the input to be from the provided filename. If omitted, standard input is used.
- `--output filename` or `-o filename` sets the output to be to the provided filename. If omitted, standard output is used.
- `--blank-lines ...` specifies how many blank lines should be created. Allowed values are `few` (the default), `some` or `many`.
- `--break-sentences` will introduce newlines at the end of each sentence.
- `--add-doc-type` or `--skip-doc-type` are used to overwrite the default behavior regarding the initial `<?xml ...` document identifier. These settings only make a difference if the source document does not contain the identifier. The default behavior depends on the output file settings. If an output file is specified via `--output` or `-o`, then a doc identifier will be inserted if it was not present. If the output is to standard out instead, then a doc identifier will not be added if not already present.
