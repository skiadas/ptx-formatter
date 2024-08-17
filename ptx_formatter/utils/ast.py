"""
Classes to represent the abstract syntax tree result of
the XML file parse
"""

from abc import ABC, abstractmethod
from typing import Dict, Self, TypeAlias

from ptx_formatter.utils.context import Context
from ptx_formatter.utils.config import Preference
from xml.sax.saxutils import escape as xmlescape, unescape as xmlunescape
from functools import cmp_to_key

Attrs: TypeAlias = Dict[str, str]

CDATA_OPEN = "<![CDATA["
CDATA_CLOSE = "]]>"


class Child(ABC):

  @abstractmethod
  def render_inline(self: Self, ctx: Context) -> str:
    """Render the child in inline mode."""
    pass

  @abstractmethod
  def render_block(self: Self, ctx: Context) -> str:
    """Render the child in block mode."""

  @abstractmethod
  def render_verbatim(self: Self, ctx: Context) -> str:
    """Render the child in verbatim mode."""

  @abstractmethod
  def is_inlineable(self: Self, ctx: Context) -> bool:
    """Determine if the child can be inlined."""


class Text(Child):
  """Simple class that holds a text string."""

  txt: str

  def __init__(self: Self, txt: str):
    self.txt = txt

  def __str__(self: Self):
    return "<Text: " + repr(self.txt) + ">"

  def render_inline(self: Self, ctx: Context) -> str:
    return xmlescape(self.txt)

  def render_block(self: Self, ctx: Context) -> str:
    return f"{ctx.indent}{xmlescape(self.txt).lstrip()}"

  def render_verbatim(self: Self, ctx: Context) -> str:
    return xmlescape(self.txt)

  def is_inlineable(self: Self, ctx: Context) -> bool:
    return True

  def append(self: Self, el: Self):
    self.txt += el.txt


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

  def render_verbatim(self: Self, ctx: Context) -> str:
    return f"<!--{self.txt}-->"

  def is_inlineable(self: Self, ctx: Context) -> bool:
    return False


class Processing(Child):
  """Simple class that holds a processing instruction."""

  txt: str

  def __init__(self: Self, txt: str):
    self.txt = txt

  def __str__(self: Self) -> str:
    return f"<?{self.txt}?>"

  def render_inline(self: Self, ctx: Context) -> str:
    return f"<?{self.txt}?>"

  def render_block(self: Self, ctx: Context) -> str:
    return f"{ctx.indent}<?{self.txt}?>"

  def render_verbatim(self: Self, ctx: Context) -> str:
    return f"<?{self.txt}?>"

  def is_inlineable(self: Self, ctx: Context) -> bool:
    return False


class EmptyLine(Child):
  """Simple class that represents an (inserted) empty line."""

  def __str__(self: Self) -> str:
    return f"<emptyline>"

  def render_inline(self: Self, ctx: Context) -> str:
    # TODO: Is this right behavior?
    return "\n"

  def render_block(self: Self, ctx: Context) -> str:
    return "\n"

  def render_verbatim(self: Self, ctx: Context) -> str:
    return "\n"

  def is_inlineable(self: Self, ctx: Context) -> bool:
    return False


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
    if isinstance(child, Text) and len(self.children) > 0 and isinstance(
        self.children[-1], Text):
      # Must combine text instances:
      self.children[-1].append(child)
    else:
      self.children.append(child)
    return self

  def render_inline(self: Self, ctx: Context) -> str:
    if self.children == []:
      return self._self_closing_tag(True, ctx)
    childStrings = [ch.render_inline(ctx) for ch in self.children]
    return f"{self._open_tag(True, ctx)}{''.join(childStrings)}{self._close_tag()}"

  def render_block(self: Self, ctx: Context) -> str:
    self._recognize_inline_comments()
    self._remove_empty_lines()
    self._insert_needed_emptylines(ctx)
    if self.tag is None:
      return self._render_root(ctx)
    if self._is_verbatim_tag(ctx) and self.children != []:
      return self.render_verbatim(ctx)
    if self._will_inline(ctx):
      return f"{ctx.indent}{self.render_inline(ctx)}"
    # Otherwise we render block
    if self.children == []:
      # Special case of empty block, render open+close tags
      return f"{ctx.indent}{self._open_tag(False, ctx)}{self._close_tag()}"
    childCtx = ctx.get_child_context(self.tag)
    childString = self._block_render_children(childCtx)
    openTag = f"{ctx.indent}{self._open_tag(False, ctx)}"
    closeTag = f"{ctx.indent}{self._close_tag()}"
    return f"{openTag}{childString}\n{closeTag}"

  def is_inlineable(self: Self, ctx: Context):
    return ctx.must_inline(self.tag, self._is_empty())

  def _insert_needed_emptylines(self: Self, ctx: Context):
    new_children = []
    for idx, el in enumerate(self.children):
      if isinstance(el, Element):
        tag = el.tag
        if ctx.must_emptyline_before(tag) and not_at_start(new_children):
          new_children.append(EmptyLine())
        new_children.append(el)
        if ctx.must_emptyline_after(tag) and not_at_end(self.children, idx):
          new_children.append(EmptyLine())
      else:
        new_children.append(el)
    self.children = new_children

  def _block_render_children(self, ctx):
    childString = ""
    lastIsInline = False
    lastLineEmpty = False
    for ch in self.children:
      isInlineable = ch.is_inlineable(ctx)
      if isInlineable and lastIsInline:
        # combine in existing line
        childString += ch.render_inline(ctx)
        lastIsInline = True
        lastLineEmpty = False
      else:
        # start new line
        block = ch.render_block(ctx)
        if isinstance(ch, EmptyLine):
          childString += "\n"
          lastLineEmpty = True
        elif block.lstrip() != "":
          if not lastLineEmpty:
            childString = childString.rstrip()
          childString = childString + "\n" + block
          lastIsInline = isInlineable
          lastLineEmpty = False
    return childString

  def _recognize_inline_comments(self: Self):
    for idx, el in enumerate(self.children):
      if isinstance(el, Element):
        nextEl = self._child_at_index(idx + 1)
        nextNextEl = self._child_at_index(idx + 2)
        if isinstance(nextEl, Comment):
          del self.children[idx]
          del self.children[idx]
          self.children.insert(idx, ElementWithInlineComment(el, "", nextEl))
        elif is_only_spaces(nextEl) and isinstance(nextNextEl, Comment):
          del self.children[idx]
          del self.children[idx]
          del self.children[idx]
          self.children.insert(
              idx, ElementWithInlineComment(el, nextEl.txt, nextNextEl))

  def _child_at_index(self: Self, idx: int) -> Child | None:
    if idx < len(self.children):
      return self.children[idx]
    else:
      return None

  def _remove_empty_lines(self: Self):
    self.children = [el for el in self.children if not is_blank_string(el)]

  def _open_tag(self: Self, inline: bool, ctx: Context) -> str:
    return f"{self._tag_start(inline, ctx)}>"

  def _self_closing_tag(self: Self, inline: bool, ctx: Context) -> str:
    space = " " if ctx.use_self_closing_space() else ""
    return f"{self._tag_start(inline, ctx)}{space}/>"

  def _tag_start(self: Self, inline: bool, ctx: Context) -> str:
    attrs = process_attrs(self.attrs)
    attrs_string = self._combine_attrs(attrs, inline, ctx)

    return f"<{self.tag}{attrs_string}"

  def _close_tag(self: Self):
    return f"</{self.tag}>"

  def _is_empty(self: Self) -> bool:
    return self.children == []

  def _is_verbatim_tag(self: Self, ctx: Context):
    pref = ctx.get_preference(self.tag)
    return pref == Preference.Verbatim

  def render_verbatim(self: Self, ctx: Context):
    openTag = self._open_tag(False, ctx)
    closeTag = self._close_tag()
    contents = "".join([c.render_verbatim(ctx) for c in self.children])
    endIndent = str(ctx.indent) if "\n" in contents else ""
    should_use_cdata = ctx.should_use_cdata(self.tag, contents)
    if should_use_cdata:
      contents_unescaped = xmlunescape(contents)
      return f"{ctx.indent}{openTag}{CDATA_OPEN}{contents_unescaped.rstrip(" ")}{endIndent}{CDATA_CLOSE}{closeTag}"
    return f"{ctx.indent}{openTag}{contents.rstrip(" ")}{endIndent}{closeTag}"

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
    if self.is_inlineable(ctx):
      return True
    if self._must_block(ctx):
      return False
    for ch in self.children:
      if not ch.is_inlineable(ctx):
        return False
    return True

  def _must_block(self: Self, ctx: Context):
    return ctx.must_block(self.tag)

  def _combine_attrs(self: Self, items: list[str], inline: bool,
                     ctx: Context) -> str:
    if len(items) == 0:
      return ""
    multiline_attrs, multi_attr_indent = ctx.get_multiline_attrs()
    if inline or multiline_attrs == "never" or multiline_attrs > len(items):
      return ''.join(items)
    else:
      strings = [f"{ctx.indent}{item}" for item in items]
      if multi_attr_indent > 0:
        extra = "\n" + (multi_attr_indent - 1) * " "
        return "".join([extra + s for s in strings])
      else:
        extra = "\n" + (1 + len(self.tag)) * " "
        return strings[0] + "".join([extra + s for s in strings[1:]])


class ElementWithInlineComment(Child):
  """Holds an element that is followed by an inlined comment
  and some spacing. This spacing and comment are to be preserved."""
  el: Element
  spacing: Text
  comment: Comment

  def __init__(self: Self, el: Element, spacing: str, comment: Comment) -> None:
    self.el = el
    self.spacing = spacing
    self.comment = comment

  def render_inline(self: Self, ctx: Context) -> str:
    return (self.el.render_inline(ctx) + self.spacing +
            self.comment.render_inline(ctx))

  def render_block(self: Self, ctx: Context) -> str:
    return (self.el.render_block(ctx) + self.spacing +
            self.comment.render_inline(ctx))

  def render_verbatim(self: Self, ctx: Context) -> str:
    raise NotImplementedError

  def is_inlineable(self: Self, ctx: Context) -> bool:
    return self.el.is_inlineable(ctx)


def process_attrs(attrs: Attrs) -> Attrs:
  sorted_items = sorted(attrs.items(), key=cmp_to_key(compare_attrs))

  return [f' {k}="{v}"' for k, v in sorted_items]


def compare_attrs(a: tuple[str, str], b: tuple[str, str]) -> int:
  k1 = a[0]
  k2 = b[0]
  if k1 == k2:
    return 0
  # Ids should come first
  if k1 == "xml:id":
    return -1
  if k2 == "xml:id":
    return 1
  # Namespace declarations should come last
  if k1.startswith("xmlns") and not k2.startswith("xmlns"):
    return 1
  if k2.startswith("xmlns") and not k1.startswith("xmlns"):
    return -1
  if k1 < k2:
    return -1
  return 1


def not_at_start(children: list[Child]) -> bool:
  return children != [] and not isinstance(children[-1], EmptyLine)


def not_at_end(children: list[Child], idx: int) -> bool:
  return idx < len(children) - 1


def is_blank_string(el: Child) -> bool:
  return isinstance(el, Text) and el.txt.strip() == ""


def is_only_spaces(el: Child) -> bool:
  return isinstance(el, Text) and el.txt.strip(" ") == ""
