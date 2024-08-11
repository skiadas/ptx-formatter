import re
from typing import Dict, Self, Set
from ptx_formatter.utils.ast import Attrs

NAMESPACED_PATTERN = re.compile(r"^\{([^\}]+)\}(.+)$")


class Namespace:
  """Manages the active namespaces for the formatter."""

  _active_ns: Dict[str, str]
  """A dictionary mapping between uris and the corresponding
     namespace abbreviations"""
  _new_ns: Set[str]
  """Any possible newly-introduced namespace. Only exists
     for the small amount of time between the calls to start_ns
     and start."""

  def __init__(self: Self):
    self._active_ns = {'http://www.w3.org/XML/1998/namespace': 'xml'}
    self._new_ns = set()

  def adjust_str(self: Self, s: str) -> str:
    m = NAMESPACED_PATTERN.search(s)
    if m is not None:
      prefix = self._active_ns[m[1]]
      return f"{prefix}:{m[2]}"
    else:
      return s

  def adjust_attrs(self: Self, attrs: Attrs) -> Attrs:
    return {self.adjust_str(k): v for k, v in attrs.items()}

  def process_new_ns(self: Self):
    for value in self._new_ns:
      if value is not None:
        key = f"xmlns:{self._active_ns[value]}"
        yield key, value
    self._new_ns = set()

  def remove_prefix(self: Self, prefix: str):
    uri = self._find_uri_for_prefix(prefix)
    del self._active_ns[uri]

  def add_prefix(self: Self, prefix: str, uri: str):
    self._active_ns[uri] = prefix
    # We need to remember the newly introduced ns
    # so we add it to the attributes list
    self._new_ns.add(uri)

  def _find_uri_for_prefix(self: Self, prefix: str) -> str | None:
    for uri, _prefix in self._active_ns.items():
      if _prefix == prefix:
        return uri
    return None
