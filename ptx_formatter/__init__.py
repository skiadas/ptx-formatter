"""
Documentation for ptx_formatter API.

This documentation is useful for those interested in using
the formatter as a Python library. If you are interested
in the command-line tool, visit the project's GitHub page.

## Basic usage

You simply need to import `formatPretext` and provide it with a
the source string. It returns the formatted string.

```python
from ptx_formatter import formatPretext

s = formatPretext(source)
print(s)
```

## Configuration

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
