from typing import Self


class Indent:
  """Keeps track of indent levels and appropriate spacing amounts"""

  level: int
  """The indent level. Starts at 0, and can be increased/decreased. Negative indent levels are not allowed."""

  _base_indent: str
  """The string to be used for a single indent level."""

  _current_indent: str
  """The string to be used for indenting at the current level."""

  def __init__(self: Self, base_indent: str | int, level: int = 0):
    self.level = level
    if isinstance(base_indent, str):
      self._base_indent = base_indent
    else:
      self._base_indent = " " * base_indent
    self._set_current_indent()

  def __str__(self: Self) -> str:
    return self._current_indent

  def _set_current_indent(self: Self) -> None:
    self._current_indent = self._base_indent * self.level

  def incr(self: Self, level=1) -> Self:
    """Returns a new `Indent object with an indent incremented
       by a number of `level`s (default 1)."""
    return Indent(self._base_indent, self.level + 1)

  def decr(self: Self, level=1) -> Self:
    """Decrements the indent by a number of `level`s
      (default 1). An error is raised if the resulting level
      is negative. Returns a new `Indent` object"""
    if (self.level < level):
      raise RuntimeError(
          f"Cannot decrease indent level {self.level} by {level}")
    return Indent(self._base_indent, self.level - 1)
