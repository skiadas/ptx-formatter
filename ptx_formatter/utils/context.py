from enum import Enum
from typing import Dict, Mapping, Self

from ptx_formatter.utils.config import Preference, Config
from ptx_formatter.utils.indent import Indent

Mode = Enum('Mode', ['Block', 'Inline', 'Verbatim'])


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
