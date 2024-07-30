# Shamelessly transpiled from https://github.com/oscarlevin/pretext-tools/blob/main/src/formatter.ts

import re
from enum import Enum

from ptx_formatter.tags import docEnvs, docSecs, docStructure, lineEndTags, math_display, nestable_tags, verbatimTags


class BlankLines(Enum):
  """Enum representing the number of blank lines to be created."""
  few = "few"
  """Few blank lines are created."""
  some = "some"
  """Blank lines are introduced more liberally."""
  many = "many"
  """Blank lines are introduced very liberally."""


RE_OPEN_TAG = re.compile(r"^<(\w\S*?)(\s.*?|>)")
RE_CLOSE_TAG = re.compile(r"^</(\w\S*?)(\s.*?|>)")

newlineTags = docStructure + docSecs + docEnvs + nestable_tags + ["xi:include"]

blockTags = docStructure + docSecs + docEnvs + nestable_tags + math_display


def joinLines(fullText: str) -> str:
  verbatim = False
  lines = fullText.splitlines()
  # Start by adding the first two lines of the document.
  joinedLines = lines[0:1]
  # Iterate through lines, joining lines when not in a verbatim block.
  for line in lines[1:]:
    # look for tags in a line
    openTagMatch = RE_OPEN_TAG.search(line.strip())
    closeTagMatch = RE_CLOSE_TAG.search(line.strip())
    if openTagMatch and openTagMatch[1] in verbatimTags:
      # This line starts a verbatim block.
      # Add it to the array of lines and set verbatim to true.
      joinedLines.append(line)
      verbatim = True
    elif closeTagMatch and closeTagMatch[1] in verbatimTags:
      # This line ends a verbatim block.
      # Add it to the array of lines and set verbatim to false.
      joinedLines.append(line)
      verbatim = False
    elif verbatim:
      # We must be inside a verbatim block.
      # Add the line to the array of lines.
      joinedLines.append(line)
    else:
      # We are not inside a verbatim block.
      # Concatenate the line to the previous line in joinedLines
      lastLine = joinedLines.pop()
      if lastLine:
        joinedLines.append(lastLine.strip() + " " + line.strip())
      else:
        joinedLines.append(line.strip())

  return "\n".join(joinedLines)


def formatPretext(
    text: str,
    breakSentences=False,
    blankLines=BlankLines.few,
    addDocumentIdentifier=False,
    indent="  ",
) -> str:
  """Format the provided pretext source code to a standard format.

  Args:
    text (str): the text to be formatted
    breakSentences (bool): Whether to create new lines at the end of each
                    text sentence. (default: False)
    blankLines (BlankLines): How frequently to use blank lines. Can be any
                    `BlankLines` enum value. (default: :obj:`BlankLines.few`)
    addDocumentIdentifier (bool): Whether to introduce an `<?xml ...?>` segment
                           at the start if one is not present. (default False)
    indent (str): string to use for indentation. (default to two spaces)

  Returns:
    str: The formatted text string
  """
  # First clean up document so that each line is a single tag when appropriate.
  text = joinLines(text)
  for btag in blockTags:
    if ("<" + btag) in text:
      # start tag can be <tag>, <tag attr="val">, or <tag xmlns="..."> but shouldn't
      # be self closing (no self closing tag would have xmlns in it)
      startTag = re.compile("<" + btag + "(>|([^/]*?)>|(.*xmlns.*?)>)")
      endTag = re.compile("</" + btag + ">")
      text = startTag.sub(r"\n\g<0>\n", text)
      text = endTag.sub(r"\n\g<0>\n", text)

  for tag in lineEndTags:
    startTag = re.compile("<" + tag + r"(\s.*?)?>")
    endTag = re.compile("</" + tag + ">")
    selfCloseTag = re.compile("<" + tag + r"(\s.*?)?/>")
    text = startTag.sub(r"\n\g<0>", text)
    text = endTag.sub(r"\g<0>\n", text)
    text = selfCloseTag.sub(r"\g<0>\n", text)

  level = 0
  verbatim = False
  lines = text.splitlines()
  fixedLines = []
  for line in lines:
    trimmedLine = line.strip()
    openTagMatch = RE_OPEN_TAG.search(line.strip())
    closeTagMatch = RE_CLOSE_TAG.search(line.strip())
    # // let selfCloseTagMatch = /^<(\w*?)(\s.*?\/>|\/>)$/.exec(trimmedLine);
    if trimmedLine == "" and not verbatim:
      continue
    elif trimmedLine.startswith("<?"):
      # It's the start line of the file:
      fixedLines.append(trimmedLine + "\n")
    elif trimmedLine.startswith("<!--"):
      # It's a comment:
      fixedLines.append(indent * level + trimmedLine)
    elif closeTagMatch:
      # TODO: Can improve the logic here
      if closeTagMatch[1] in blockTags:
        level = max(0, level - 1)
        fixedLines.append(indent * level + trimmedLine)
      elif closeTagMatch[1] in verbatimTags:
        verbatim = False
        fixedLines.append(indent * level + trimmedLine)
      else:
        fixedLines.append(indent * level + trimmedLine)

    elif openTagMatch:
      fixedLines.append(indent * level + trimmedLine)
      if openTagMatch[1] in blockTags:
        level += 1
      elif openTagMatch[1] in verbatimTags:
        verbatim = True
    elif verbatim:
      fixedLines.append(line)
    else:
      if breakSentences:
        trimmedLine = re.sub(r"\.\s+", ".\n" + indent * level, trimmedLine)
      fixedLines.append(indent * level + trimmedLine)

  # Second pass: add empty line between appropriate tags depending
  # on blankLines setting.

  match blankLines:
    case BlankLines.few:
      # do nothing
      pass
    case BlankLines.some:
      for i in range(0, len(fixedLines) - 1):
        if fixedLines[i].strip().startswith("</"):
          for tag in newlineTags:
            startTag = re.compile("<" + tag + "(.*?)>")
            if startTag.match(fixedLines[i + 1]):
              fixedLines[i] += "\n"
        elif fixedLines[i].strip().startswith("<title>"):
          fixedLines[i] += "\n"
    case BlankLines.many:
      for i in range(0, len(fixedLines) - 1):
        if fixedLines[i].strip().startswith("</") or (
            fixedLines[i].strip().startswith("<") and
            fixedLines[i + 1].strip().startswith("<")):
          fixedLines[i] += "\n"

  # Add document identifier line if missing:
  if addDocumentIdentifier and not fixedLines[0].strip().startswith("<?xml"):
    fixedLines.insert(0, '<?xml version="1.0" encoding="UTF-8" ?>\n')

  return "\n".join(fixedLines)


## TODO: Make a test to see how this works.
# Seems to produce extra "<" after some closing tags
