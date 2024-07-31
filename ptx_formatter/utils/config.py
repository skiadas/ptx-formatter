"""
Represents various settings for the formatter
"""
from enum import Enum

from os.path import dirname, join
from typing import Dict, Mapping, Self, TextIO
import tomlkit

Preference = Enum(
    'Preference',
    ['No', 'Verbatim', 'Inline', 'InlineEmpty', 'Block', 'BlockNoIndent'])


class Config:
  _tag_prefs: Dict[str, Preference]
  """Preferences regarding how various tags should be formatted."""
  base_indent: str
  """The base indent to be used. Defaults to 2 spaces."""
  add_doc_id: bool
  """Whether to add the xml identifier at the start."""

  def __init__(self: Self, base_indent: str | int = 2):
    self._tag_prefs = {}
    self.set_indent(base_indent)
    self.add_doc_id = False

  def get_pref(self: Self, tag: str) -> Preference:
    return self._tag_prefs.get(tag, Preference.No)

  def add_tag_prefs(self: Self, prefs: Mapping[str, Preference]):
    self._tag_prefs = dict(prefs.items())

  def set_indent(self: Self, base_indent: str | int):
    if isinstance(base_indent, int):
      self.base_indent = " " * base_indent
    else:
      self.base_indent = base_indent

  def set_add_doc_id(self: Self, add_doc_id: bool):
    self.add_doc_id = add_doc_id

  def print(self: Self) -> str:
    """Forms a TOML file description of the configuration."""
    doc = tomlkit.TOMLDocument()
    doc.add(
        tomlkit.comment(
            "Set the indent as a number of spaces or a string. Defaults to 2 spaces."
        ))
    doc.add("indent", self.base_indent)
    doc.add(tomlkit.nl())
    doc.add(
        tomlkit.comment(
            "Specify whether a document id should be included. This option is only relevant when not using the cli, as the cli will overwrite the setting here."
        ))
    doc.add("include-doc-id", self.add_doc_id)
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
            "block-no-indent tags will increase the indent of their contents."))
    tags.add("block-no-indent", self._make_array(Preference.BlockNoIndent))
    return tomlkit.dumps(doc)

  @classmethod
  def standard(cls) -> Self:
    return cls.fromFile(join(dirname(__file__), "..", "config.toml"))

  @classmethod
  def fromFile(cls, fp: TextIO | str):
    config = cls()
    opts = _read_opts(fp)
    config.set_indent(opts.get('indent', 2))
    config.set_add_doc_id(opts.get('include-doc-id', False))
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
