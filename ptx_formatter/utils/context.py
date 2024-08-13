from enum import Enum
from typing import Dict, Iterable, Literal, Mapping, Self

from ptx_formatter.utils.config import Preference, Config
from ptx_formatter.utils.indent import Indent

import re

Mode = Enum('Mode', ['Block', 'Inline', 'Verbatim'])

ESCAPES_REGEX = re.compile("&(amp|gt|lt);")


class Context:
  """Holds a current context in the formatting process. """
  config: Config
  """The tag preferences."""
  indent: Indent
  """The current indent level."""

  def __init__(self: Self, config: Config, indent: Indent = None) -> None:
    self.config = config
    self.indent = indent or Indent(config._base_indent)

  def get_preference(self: Self, tag: str) -> Preference:
    return self.config.get_pref(tag)

  def should_add_doc_id(self: Self) -> bool:
    return self.config._add_doc_id

  def should_use_cdata(self: Self, tag: str, contents: str) -> bool:
    if self.config._cdata == "always":
      return True
    if self.config._cdata == "never":
      return False
    if isinstance(self.config._cdata, Iterable):
      return tag in self.config._cdata
    # Else it's a number. Need to count escaped units in contents
    escaped_count = len(ESCAPES_REGEX.findall(contents))
    return escaped_count >= self.config._cdata

  def get_multiline_attrs(self: Self) -> tuple[Literal["never"] | int, int]:
    return self.config._multiline_attrs

  def must_inline(self: Self, tag: str, is_empty: bool) -> bool:
    pref = self.get_preference(tag)
    return pref == Preference.Inline or (pref == Preference.InlineEmpty and
                                         is_empty)

  def must_block(self: Self, tag: str) -> bool:
    pref = self.get_preference(tag)
    return pref == Preference.Block or pref == Preference.BlockNoIndent

  def get_child_context(self: Self, tag: str) -> Self:
    tagPref = self.get_preference(tag)
    if tagPref == Preference.BlockNoIndent:
      return self
    return Context(self.config, self.indent.incr())

  def must_emptyline_before(self: Self, tag: str) -> bool:
    return tag in self.config._emptyline_before

  def must_emptyline_after(self: Self, tag: str) -> bool:
    return tag in self.config._emptyline_after
