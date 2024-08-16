# PtxFormatter

PtxFormatter is an opinionated but customizable formatter for PreText. It can be used as a command-line tool or as a Python library.

See the [docs](https://skiadas.github.io/ptx-formatter/) for installation instructions.

Quick installation instructions:
```shell
pipx install --python 3.12 --fetch-missing-python  git+https://github.com/skiadas/ptx-formatter.git
ptx-format --help
```

Quick usage:
```shell
ptx-format inputfile.ptx                 # input from file, output to stdout
ptx-format inputfile.ptx outputfile.ptx  # input from file, output to file
ptx-format                               # input from stdin output to stdout
ptx-format -p inputfile.ptx              # in-place processing of inputfile.ptx
ptx-format -pr source                    # in-place recursive processing of *.ptx files in source directory and subdirectories
```
