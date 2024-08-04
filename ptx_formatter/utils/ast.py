"""
Classes to represent the abstract syntax tree result of
the XML file parse
"""

from abc import ABC, abstractmethod
from typing import Dict, Self, TypeAlias

from ptx_formatter.utils.context import Context
from ptx_formatter.utils.config import Preference
from xml.sax.saxutils import escape as xmlescape

Attrs: TypeAlias = Dict[str, str]


class Child(ABC):

  @abstractmethod
  def render_inline(self: Self, ctx: Context) -> str:
    """Render the child in inline mode."""
    pass

  @abstractmethod
  def render_block(self: Self, ctx: Context) -> str:
    """Render the child in block mode."""


class Text(Child):
  """Simple class that holds a text string."""

  txt: str

  def __init__(self: Self, txt: str):
    self.txt = txt

  def render_inline(self: Self, ctx: Context) -> str:
    return xmlescape(self.txt)

  def render_block(self: Self, ctx: Context) -> str:
    return f"{ctx.indent}{self.txt}"


class Comment(Child):
  """Simple class that holds a comment line."""

  txt: str

  def __init__(self: Self, txt: str):
    self.txt = txt

  def __str__(self: Self) -> str:
    return f"<!--{self.txt}-->"

  def render_inline(self: Self, ctx: Context) -> str:
    return f"<!--{self.txt}-->"

  def render_block(self: Self, ctx: Context) -> str:
    return f"{ctx.indent}<!--{self.txt}-->"


class Element(Child):
  """Holds an actual element, with its open and close tags,
     attributes and child elements.

     An element with tag None is meant to be the root of the tree."""

  tag: str | None
  attrs: Attrs
  children: list[Child]

  def __init__(self: Self,
               tag: str = None,
               attrs: Attrs = {},
               children: list[Child] = []):
    self.tag = tag
    self.attrs = attrs
    self.children = children or []

  def __str__(self: Self):
    return f"<{self.tag} ...>"

  def addChild(self: Self, child: Child) -> Self:
    self.children.append(child)
    return self

  def render_inline(self: Self, ctx: Context) -> str:
    if self.children == []:
      return self._self_closing_tag(True)
    childStrings = [ch.render_inline(ctx) for ch in self.children]
    return f"{self._open_tag(True)}{''.join(childStrings)}{self._close_tag()}"

  def render_block(self: Self, ctx: Context) -> str:
    if self.tag is None:
      return self._render_root(ctx)
    if self._is_verbatim_tag(ctx):
      return self._render_verbatim(ctx)
    if self._will_inline(ctx):
      return f"{ctx.indent}{self.render_inline(ctx)}"
    # Otherwise we render block
    if self.children == []:
      # Special case of empty block, render open+close tags
      return f"{ctx.indent}{self._open_tag(False)}{self._close_tag()}"
    childCtx = ctx.get_child_context(self.tag)
    children = []
    for ch in self.children:
      block = ch.render_block(childCtx)
      if block.lstrip() != "":
        children.append(block)
    openTag = f"{ctx.indent}{self._open_tag(False)}\n"
    closeTag = f"{ctx.indent}{self._close_tag()}"
    return f"{openTag}{'\n'.join(children)}\n{closeTag}"

  def _open_tag(self: Self, inline: bool):
    attrs = [f' {k}="{v}"' for k, v in self.attrs.items()]

    return f"<{self.tag}{''.join(attrs)}>"

  def _self_closing_tag(self: Self, inline: bool):
    attrs = [f' {k}="{v}"' for k, v in self.attrs.items()]

    return f"<{self.tag}{''.join(attrs)} />"

  def _close_tag(self: Self):
    return f"</{self.tag}>"

  def _is_empty(self: Self) -> bool:
    return self.children == []

  def _is_verbatim_tag(self: Self, ctx: Context):
    pref = ctx.get_preference(self.tag)
    return pref == Preference.Verbatim

  def _render_verbatim(self: Self, ctx: Context):
    openTag = self._open_tag(False)
    closeTag = self._close_tag()
    contents = "".join([c.render_inline(ctx) for c in self.children])
    return f"{ctx.indent}{openTag}{contents.rstrip(" ")}{ctx.indent}{closeTag}"

  def _render_root(self: Self, ctx: Context):
    content = "\n".join([ch.render_block(ctx) for ch in self.children])
    if ctx.should_add_doc_id():
      return """<?xml version="1.0" encoding="UTF-8" ?>\n\n""" + content
    else:
      return content

  def _will_inline(self: Self, ctx: Context):
    """Will inline if:
       - tag prefers inlined, or
       - tag does not force block and all the element's
         children prefer to be inlined"""
    if self._must_inline(ctx):
      return True
    if self._must_block(ctx):
      return False
    for ch in self.children:
      if isinstance(ch, Element):
        if not ch._must_inline(ctx):
          return False
    return True

  def _must_inline(self: Self, ctx: Context):
    return ctx.must_inline(self.tag, self._is_empty())

  def _must_block(self: Self, ctx: Context):
    return ctx.must_block(self.tag)
