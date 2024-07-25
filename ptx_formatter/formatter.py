# Shamelessly transpiled from https://github.com/oscarlevin/pretext-tools/blob/main/src/formatter.ts

import re
from enum import Enum


class BlankLines(str, Enum):
  few = "few"
  some = "some"
  many = "many"


RE_OPEN_TAG = re.compile(r"^<(\w\S*?)(\s.*?|>)$")
RE_CLOSE_TAG = re.compile(r"^</(\w\S*?)(\s.*?|>)(.?)$")

docStructure = [
    "abstract",
    "acknowledgement",
    "appendix",
    "article",
    "author",
    "backmatter",
    "biography",
    "book",
    "chapter",
    "colophon",
    "contributor",
    "contributors",
    "copyright",
    "credit",
    "dedication",
    "docinfo",
    "editor",
    "feedback",
    "frontmatter",
    "google",
    "html",
    "index",
    "macros",
    "mathbook",
    "preface",
    "pretext",
    "references",
    "search",
    "shortlicense",
    "solutions",
    "subsection",
    "titlepage",
    "website",
]

docSecs = [
    "assemblage",
    "chapter",
    "conclusion",
    "introduction",
    "objectives",
    "outcomes",
    "paragraphs",
    "part",
    "postlude",
    "prelude",
    "reading-questions",
    "sbsgroup",
    "section",
    "stack",
    "subsection",
    "subsubsection",
    "task",
    "technology",
    "worksheet",
]

docEnvs = [
    "activity",
    "algorithm",
    "answer",
    "axiom",
    "biblio",
    "blockquote",
    "case",
    "choice",
    "choices",
    "claim",
    "conjecture",
    "console",
    "corollary",
    "definition",
    "demonstration",
    "description",
    "example",
    "exercise",
    "exploration",
    "fact",
    "hint",
    "image",
    "images",
    "insight",
    "investigation",
    "lemma",
    "list",
    "listing",
    "note",
    "openconjecture",
    "openproblem",
    "openquestion",
    "page",
    "poem",
    "principle",
    "problem",
    "program",
    "project",
    "proof",
    "proposition",
    "question",
    "remark",
    "shortdescription",
    "solution",
    "stanza",
    "statement",
    "subtask",
    "table",
    "tabular",
    "theorem",
    "warning",
    "webwork",
]

lineEndTags = [
    "address",
    "attribution",
    "caption",
    "cd",
    "cell",
    "cline",
    "date",
    "department",
    "description",
    "edition",
    "entity",
    "holder",
    "idx",
    "institution",
    "journal",
    "line",
    "location",
    "minilicense",
    "mrow",
    "personname",
    "pg-macros",
    "pubtitle",
    "row",
    "subtitle",
    "title",
    "usage",
    "volume",
    "year",
    "xi:include",
    # Added by us
    "premise",
    "response"
]

# empty tags that should be on their own line
docEmpty = [
    "cell",
    "col",
    "notation-list",
    "brandlogo",
    "cross-references",
    "input",
    "video",
    "slate",
    "webwork",
]

list_like = ["ol", "ul", "dl"]

math_display = ["me", "men", "md", "mdn"]

footnote_like = ["fn"]

nestable_tags = [
    "ul",
    "ol",
    "li",
    "p",
    "task",
    "figure",
    "sidebyside",
    "notation",
    "row",
]

# note that c is special, because it is inline verbatim
verbatimTags = [
    "latex-image-preamble",
    "latex-image",
    "latex-preamble",
    "slate",
    "sage",
    "sageplot",
    "asymptote",
    "macros",
    "program",
    "input",
    "output",
    "tests",  # Added by us
    "prompt",
    "pre",
    "pg-code",
    "tikzpicture",
    "tikz",
    "code",
    "c",
]

newlineTags = docStructure + docSecs + docEnvs + nestable_tags + ["xi:include"]

blockTags = docStructure + docSecs + docEnvs + nestable_tags + math_display


def joinLines(fullText: str) -> str:
  verbatim = False
  lines = fullText.splitlines()
  # Start by adding the first two lines of the document.
  joinedLines = lines[0:2]
  # Iterate through lines, joining lines when not in a verbatim block.
  for line in lines[2:]:
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
    allText: str,
    breakSentences=False,
    blankLines=BlankLines.few,
    addDocumentIdentifier=False,
    indent="  ",
) -> str:
  # First clean up document so that each line is a single tag when appropriate.
  allText = joinLines(allText)

  for btag in blockTags:
    if ("<" + btag) in allText:
      # start tag can be <tag>, <tag attr="val">, or <tag xmlns="..."> but shouldn't
      # be self closing (no self closing tag would have xmlns in it)
      startTag = re.compile("<" + btag + "(>|([^/]*?)>|(.*xmlns.*?)>)")
      endTag = re.compile("</" + btag + ">(.?)")
      allText = startTag.sub(r"\n\g<0>\n", allText)
      allText = endTag.sub(r"\n\g<0>\n", allText)

  for tag in lineEndTags:
    startTag = re.compile("<" + tag + "(.*?)>")
    endTag = re.compile("</" + tag + ">(.?)")
    selfCloseTag = re.compile("<" + tag + "(.*?)/>")
    allText = startTag.sub(r"\n\g<0>", allText)
    allText = endTag.sub(r"\g<0>\n", allText)
    allText = selfCloseTag.sub(r"\g<0>\n", allText)

  level = 0
  verbatim = False
  lines = allText.splitlines()
  fixedLines = []
  for line in lines:
    trimmedLine = line.strip()
    openTagMatch = RE_OPEN_TAG.search(line.strip())
    closeTagMatch = RE_CLOSE_TAG.search(line.strip())
    # // let selfCloseTagMatch = /^<(\w*?)(\s.*?\/>|\/>)$/.exec(trimmedLine);
    if trimmedLine == "":
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
