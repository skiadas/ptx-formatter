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

## Formatting Style and Customization

Elements in the PtxFormatter can be rendered broadly in two modes:
**block** and **inline**.

### Block and Inline modes

In block mode the open and close tags of the
element are in their own lines (except for empty elements) and the contents
are indented and typically take on one line each:
```xml
<p>
  Example of block mode. The contents are indented.
  <m>x = 2</m>
  And each has its own line.
</p>
<!-- Empty element in block mode has open and close tags -->
<p></p>
```

In inline mode the contents form one long line, including the
open and close tags. Empty elements use the self-closing tag form:
```xml
<p>Example of inline mode. The contents are all in one line. <m>x = 2</m> and they are combined.</p>
<!-- Empty element in inline mode uses self-closing tag form -->
<p />
```
There is also **verbatim** mode, used for code chunks. More on verbatim mode later.

### Normal formatting rules

The normal operation of the formatter is as follows:

- If an element contains only text, then it renders in inline mode
- If an element contains other elements, or comments, then it renders
  in block mode

For example the default setting will produce the following format:
```xml
<section>
  <p>The paragraphs are inline as they have only text.</p>
  <p>The section is block as it contains one or more elements.</p>
</section>
```

### Rule overrides

This default behavior can be changed in a number of ways:

- We can specify certain tags that are **inline-only**. Then other
  elements contain such tags, they treat them effectively as text elements
  and will combine them with any surrounding text. This is convenient for
  tags used to mark parts of a text. Here is an example:
  ```xml
  <section>
    <p>The <em>emphasized tag</em> was marked as inline-only and keeps this element as inline.</p>
  </section>
  ```
  You can also specify a tag as **inline-when-empty**. This would cause
  empty elements of that tag to be treated as inline-only.
- You can specify certain tags to be **block-only**. These tags
  will always render their contents in block form. For example:
  ```xml
  <p>
    Here the p tag is specified as block-only, and renders this text in block form.
  </p>
  ```
- A special **block-no-indent** setting can be used if you want some tags to exhibit
  the block mode behavior but without indenting their contents.

### Verbatim mode and CDATA

Certain tags can be designated as "verbatim", and the contents of those
tags are rendered as-is. This is often used for code chunks and other extrinsic
languages.

A challenge in those situations is that certain characters carry a
special meaning in an XML document, namely `<`, `>` and `&`, and they
need to be escaped. Depending on the nature of the verbatim text, there might
be a large number of these symbols, making it harder to read the resulting code.
In those cases you can opt to use a CDATA block to avoid having to escape
these characters. Here's an example:
```
<pre>
<![CDATA[
We can freely use the less-than, greater-than, and ampersand
characters in a CDATA block
x > 4 && x < 2
]]>
</pre>
<pre>
Without CDATA, we must escape them
x &amp;gt; 4 &amp;&amp; x &amp;lt; 2
</pre>
```
You can customize how you want the formatter to handle such cases in a verbatim
tag block with the `use-cdata` configuration option. You can choose to:
- always or never use CDATA (set the value to `"always"` or `"never"`)
- use CDATA when a certain number of characters would need to be escaped (set the value to an integer)
- use CDATA with a specific list of tags (set the value to a list of tag strings)

### Empty lines

Some people like to have empty lines immediately preceding or following
certain tags. You can customize this behavior as well, by specifying a list
of tags when empty lines should appear before them as well as a list of tags
where empty lines should appear after them.

### Multiple attributes

Open tags that contain multiple attributes can easily grow too long. The formatter
supports a variety of ways to customize the appearance of multiple attributes
on the same tag, via the configuration options `multiline-attributes` and `multiline-attribute-indent`.
The default setting is for `multiline-attributes` to equal the string `"never"`, in
which case attributes simply line up on the same line as the opening tag, like so:
```xml
<section back-color="blue" front-color="red">
  Attributes are on the same line as opening tag by default.
</section>
```
You can instead specify an integer value for `multiline-attributes`. Then the layout
will change whenever the number of attributes equal or more than this value:
```xml
<section
 back-color="blue"
 front-color="red">
  With multiline-attributes set to 2, tags with 2 or more attributes will render
  them in multiple lines like this example.
</section>
```
The value of `multiline-attributes-indent` is then used to determine how much
the attributes should be indented. In the example above the value used was 1.

Setting `multiline-attributes-indent` to the special value of 0 changes the behavior.
In that case the first attribute is placed inline with the opening tag, and subsequent
attributes line up with it.
```xml
<section back-color="blue"
         front-color="red">
  With multiline-attribute-indent set to 0, the first attribute goes inline and the
  others line up with it
</section>
```

## Configuration

You can customize the output further by providing a `Config`
object, likely created by calling the `Config.fromFile` method. From the command
line you can use the appropriate flag to specify a configuration file.

Configurations can be stored to and loaded from [TOML](https://toml.io/en/)
format files. An example file is produced by the `Config.print` function, or by
using `--show-config` in the command line.

The following entries are expected/allowed:

- `indent`, with value a number of spaces or a string to use for indent
- `include-doc-id`, a boolean to specify whether the document
  identifier should be included or not
- `emptyline-before` and `emptyline-after` are list of tag strings that specify
  that empty lines should be introduced immediately before or after these elements.
- `use-cdata` can be used to determine when cdata should be used in verbatim tags.
  It can be either the strings `"always"` or `"never"`, or a number indicating the
  number of escaped elements that would cause cdata to be used to avoid the escaping,
  or a list of string tags indicating that cdata should always be used within those
  tags and not otherwise.
- `multiline-attributes` and `multiline-attribute-indent` can be used to customize
  the behavior of attributes in the open tag of an element. The multiline-attributes
  value can be the string `"never"`, in which case all attributes appear
  in the same line as the open tag. Alternatively, it could be a number indicating
  that if the number of attributes meets or exceeds this number then the attributes
  will appear in multiple lines. In that case the multiline-attribute-indent value
  is consulted. If it is 0 then the first of the attributes is in the same line
  as the opening tag and the other attributes line up with it. If it is some other number
  then all attributes go on their own lines indented by that amount.
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
