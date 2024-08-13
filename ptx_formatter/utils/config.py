"""Represents various settings for the formatter."""
from enum import Enum

from os.path import dirname, join
from typing import Dict, Literal, Mapping, Self, TextIO
import tomlkit

Preference = Enum(
    'Preference',
    ['No', 'Verbatim', 'Inline', 'InlineEmpty', 'Block', 'BlockNoIndent'])


class Config:
  """A configuration object for the formatter. The details in this object
  should only matter to developers. Users of the formatter should
  specify the desired behavior via configuration files."""
  _tag_prefs: Dict[str, Preference]
  """Preferences regarding how various tags should be formatted."""
  _base_indent: str
  """The base indent to be used. Defaults to 2 spaces."""
  _add_doc_id: bool
  """Whether to add the xml identifier at the start."""
  _cdata: Literal["always", "never"] | int | list[str]
  """How to handle cdata. Can be:
  - the keywords `"always"` or `"never"`
  - a list of tags to apply cdata to those tags. They must also be set verbatim.
  - an integer. If the content contains that many characters to be escaped, then use cdata."""
  _multiline_attrs: tuple[Literal["never"] | int, int]
  """
  Sets the behavior for multiline-attributes: Whether they should exist and
  how much to indent.
  - `have_multiline` is either `"never"` or the number of attributes
    that need to be present before multiline is triggered.
  - `multiline_indent is the number of spaces used when indenting multiline arguments.
    The value 0 is special: It indicates that the first attribute goes in the
    open tag line, and subsequent attributes line up with it.
  """
  _emptyline_before: list[str]
  _emptyline_after: list[str]
  """
  Set behavior about whether newlines should be introduced immediately
  following or immediately preceding certain elements, based on the tags listed.
  Note that if a newline should be added because of both the previous tag
  and the next tag, then only one newline is inserted.
  """

  def __init__(self: Self, base_indent: str | int = 2):
    """Create a configuration object with minimal settings."""
    self._tag_prefs = {}
    self.set_indent(base_indent)
    self._add_doc_id = False
    self._cdata = "never"
    self._emptyline_after = []
    self._emptyline_before = []

  def get_pref(self: Self, tag: str) -> Preference:
    """Retrieve the preference setting for a tag string."""
    return self._tag_prefs.get(tag, Preference.No)

  def add_tag_prefs(self: Self, prefs: Mapping[str, Preference]):
    """Add preference settings for tags, in the form of a dictionary."""
    for k, v in prefs.items():
      self._tag_prefs[k] = v

  def set_indent(self: Self, base_indent: str | int):
    """
    Specify the base indent to be used (default is 2 spaces).
    It can be either a string to be used (e.g. `"\t"`) or
    a number of spaces to be used.
    """
    if isinstance(base_indent, int):
      self._base_indent = " " * base_indent
    else:
      self._base_indent = base_indent

  def set_add_doc_id(self: Self, add_doc_id: bool):
    """
    Specify whether an XML document identifier will be
    included at the top of the file.
    """
    self._add_doc_id = add_doc_id

  def set_cdata(self: Self,
                cdata: Literal["always", "never"] | int | list[str]):
    """Specify how to handle cdata. The parameter can be:
    - the keywords `"always"` or `"never"`
    - a list of tags to apply cdata to those tags. They must also be set verbatim.
    - an integer. If the content contains that many characters to be escaped, then use cdata."""
    self._cdata = cdata

  def set_multiline_attrs(self: Self,
                          have_multiline: Literal["never"] | int = "never",
                          multiline_indent: int = 1):
    """
    Sets the behavior for multiline-attributes: Whether they should exist and
    how much to indent.
    - `have_multiline` is either `"never"` or the number of attributes
      that need to be present before multiline is triggered.
    - `multiline_indent is the number of spaces used when indenting multiline arguments.
      The value 0 is special: It indicates that the first attribute goes in the
      open tag line, and subsequent attributes line up with it.
    """
    self._multiline_attrs = (have_multiline, multiline_indent)

  def set_emptyline_before(self: Self, tags: list[str]):
    self._emptyline_before = tags

  def set_emptyline_after(self: Self, tags: list[str]):
    self._emptyline_after = tags

  def print(self: Self) -> str:
    """
    Forms a [TOML](https://toml.io/en/) file description of the configuration.
    This is the same format as expected by `fromFile`.
    """
    doc = tomlkit.TOMLDocument()
    doc.add(
        tomlkit.comment(
            "Set the indent as a number of spaces or a string. Defaults to 2 spaces."
        ))
    doc.add("indent", self._base_indent)
    doc.add(tomlkit.nl())
    doc.add(
        tomlkit.comment(
            "Specify whether a document id should be included. This option is only relevant when not using the cli, as the cli will overwrite the setting here."
        ))
    doc.add("include-doc-id", self._add_doc_id)
    doc.add(tomlkit.nl())
    doc.add(
        tomlkit.comment(
            "Determines when a cdata block should be used in a verbatim tag."))
    doc.add("use-cdata", self._cdata)
    doc.add(tomlkit.nl())
    doc.add(
        tomlkit.comment(
            "Determines whether to place multiple arguments on multiple lines, and how to indent them when doing so."
        ))
    have_multiline, multiline_indent = self._multiline_attrs
    doc.add("multiline-attributes", have_multiline)
    doc.add("multiline-attribute-indent", multiline_indent)
    doc.add(tomlkit.nl())
    doc.add(
        tomlkit.comment(
            "Determine if (extra) newlines should be inserted immediately following or immediately preceding an element"
        ))
    doc.add("emptyline-before", self._emptyline_before)
    doc.add("emptyline-after", self._emptyline_after)
    doc.add(tomlkit.nl())
    doc.add(tomlkit.nl())
    tags = tomlkit.table()
    doc.add(
        tomlkit.comment(
            "Only add to these lists of tags for cases where you want to force the behavior."
        ))
    doc.add("tags", tags)
    tags.add(tomlkit.comment("Verbatim tags."))
    tags.add("verbatim", self._make_array(Preference.Verbatim))
    tags.add(
        tomlkit.comment(
            "Inline tags will prefer to render themselves inline, and will always render their contents inline."
        ))
    tags.add("inline", self._make_array(Preference.Inline))
    tags.add(
        tomlkit.comment(
            "Inline-empty tags will only prefer to render themselves inline when they are empty."
        ))
    tags.add("inline-empty", self._make_array(Preference.InlineEmpty))
    tags.add(
        tomlkit.comment(
            "Block tags will always render themselves and their direct contents in (multiline) block style."
        ))
    tags.add("block", self._make_array(Preference.Block))
    tags.add(
        tomlkit.comment(
            "block-no-indent tags will not increase the indent of their contents."
        ))
    tags.add("block-no-indent", self._make_array(Preference.BlockNoIndent))
    return tomlkit.dumps(doc)

  @classmethod
  def standard(cls) -> Self:
    """Create a standard configuration object."""
    return cls.fromFile(join(dirname(__file__), "..", "config.toml"))

  @classmethod
  def fromFile(cls, fp: TextIO | str):
    """
    Create a configuration object from the
    provided [TOML](https://toml.io/en/) file.

    You can use the result produced by `print` as a blueprint.
    """
    config = cls()
    opts = _read_opts(fp)
    config.set_indent(opts.get('indent', 2))
    config.set_add_doc_id(opts.get('include-doc-id', False))
    config.set_cdata(opts.get('use-cdata', "never"))
    config.set_multiline_attrs(opts.get("multiline-attributes", "never"),
                               opts.get("multiline-attribute-indent", 1))
    config.set_emptyline_before(opts.get("emptyline-before", []))
    config.set_emptyline_after(opts.get("emptyline-after", []))
    prefs = {}
    for k, tagList in opts.get('tags', {}).items():
      pref = preference_from_string(k)
      for tag in tagList:
        prefs[tag] = pref
    config.add_tag_prefs(prefs)
    return config

  def _make_array(self: Self, pref: Preference) -> tomlkit.items.Array:
    items = [k for k, v in self._tag_prefs.items() if v == pref]
    arr = tomlkit.array(items)
    arr.multiline(len(items) > 2)
    return arr


def _read_opts(fp: TextIO | str) -> tomlkit.TOMLDocument:
  if isinstance(fp, str):
    with open(fp, "r") as fp:
      return tomlkit.load(fp)
  else:
    return tomlkit.load(fp)


PREFERENCE_FROM_STRING = {
    "verbatim": Preference.Verbatim,
    "block": Preference.Block,
    "block-no-indent": Preference.BlockNoIndent,
    "inline": Preference.Inline,
    "inline-empty": Preference.InlineEmpty,
}

STRING_FROM_PREFERENCE = {v: k for k, v in PREFERENCE_FROM_STRING.items()}


def preference_from_string(s: str) -> Preference:
  if s in PREFERENCE_FROM_STRING:
    return PREFERENCE_FROM_STRING[s]
  raise RuntimeError("Unknown tag preference: " + s)


def string_from_preference(p: Preference) -> str:
  if p == Preference.No:
    raise RuntimeError("The No preference should not have shown up in config.")
  return STRING_FROM_PREFERENCE[p]
