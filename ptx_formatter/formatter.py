"""
Formatter for PreText and other XML files
"""
from typing import Self
import xml.etree.ElementTree as ET

from ptx_formatter.utils.ast import Element, Attrs, Comment, Text, Processing
from ptx_formatter.utils.context import Context
from ptx_formatter.utils.namespace import Namespace
from ptx_formatter.utils.config import Config


def formatPretext(
    text: str,
    config: Config = None,
) -> str:
  """Format the provided (valid) XML trees using the provided `ptx_formatter.Config`
  object. Use a standard Config object if one is not provided.
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
    tag = self._ns.adjust_str(tag)
    attrs = self._ns.adjust_attrs(attrs)
    attrs.update(self._ns.process_new_ns())
    self._pending.append(self._current)
    self._current = Element(tag, attrs)

  def end(self, closeTag: str):
    closeTag = self._ns.adjust_str(closeTag)
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

  def pi(self: Self, target: str, text: str):
    self._current.addChild(Processing(f"{target} {text}"))
