"""
Formatter for PreText and other XML files
"""
from typing import Self
import xml.etree.ElementTree as ET

from ptx_formatter.utils.ast import Element, Attrs, Comment, Text
from ptx_formatter.utils.context import Context
from ptx_formatter.utils.namespace import Namespace
from ptx_formatter.utils.config import Config


def formatPretext(
    text: str,
    config: Config = None,
) -> str:
  """Format the provided (valid) XML trees. You can configure
  the output to some extent by providing your own `ptx_formatter.Config`
  object.

  The formatter follows a simple approach that aims to
  accommodate the option of inline tags. The formatting
  behavior is mainly this:

  - Elements that contain other elements within them are rendered
    in "block mode", with the open and close tags on their
    own lines, and with the contents suitably indented and on
    separate lines.
  - Elements that only contain text render in "inline mode",
    with the open and close tags on the same line as their contents.
  - Certain tags can be designated as "inline tags". When an element
    contains only text and inline tags, it renders in "inline mode".
    This is useful for tags that are meant to enhance the content of
    a normal line of text, like the `span` or `code` tags in HTML.
  - Certain tags can be designated as "block tags". These will always
    render in block mode.
  - Empty tags are rendered in auto-close form when inline, and as
    adjacent open-close tags when in block.
  """
  formatter = Formatter(text, config or Config.standard())
  return formatter.format()


class Formatter(ET.TreeBuilder):
  final_string: str | None = None
  """The resulting formatted string. Returned from `format`"""
  _pending: list[Element]
  """The list of currently open elements contexts."""
  _current: Element
  """The current context whose contents are processed"""
  _ns: Namespace
  """Manages the active namespaces."""

  def __init__(self: Self, text: str, config: Config = None):
    self.base_ctx = Context(config or Config.standard())
    self._ns = Namespace()
    self._pending = []
    self.root = Element()
    self._current = self.root
    ET.fromstring(text, parser=ET.XMLParser(target=self))

  def format(self: Self) -> str:
    if self.final_string is None:
      self.final_string = self.root.render_block(self.base_ctx)
    return self.final_string

  def start(self, tag: str, attrs: Attrs):
    # Need to fix the namespace-related attributes
    attrs = self._ns.adjust_attrs(attrs)
    attrs.update(self._ns.process_new_ns())
    self._pending.append(self._current)
    self._current = Element(tag, attrs)

  def end(self, closeTag: str):
    if closeTag != self._current.tag:
      raise RuntimeError(f"tag {self._current.tag} was matched by {closeTag}")
    self._current = self._pending.pop().addChild(self._current)

  def data(self, text: str):
    self._current.addChild(Text(text))

  def comment(self: Self, text: str):
    self._current.addChild(Comment(text))

  def start_ns(self: Self, prefix: str, uri: str):
    self._ns.add_prefix(prefix, uri)

  def end_ns(self: Self, prefix: str):
    self._ns.remove_prefix(prefix)
