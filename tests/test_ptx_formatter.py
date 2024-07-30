import unittest

from os.path import dirname, join
from ptx_formatter.formatter import formatPretext

# Turn this on if you want result files produced
# for manual comparison
WRITE_RESULT_FILES = False

sampleFiles = ["fewNewlines.ptx",
               "fewWithListing.ptx"]  # TODO: create more test files

fixedExpressions = [
    """<premise>
  <p>A paragraph</p>
</premise>""", """<premise>
  <p>A paragraph</p>
</premise>
<response>
  <p>Another paragraph</p>
</response>""", """<p>A paragraph</p>
<p>Another paragraph</p>""", """<p>
<ul>
</ul>
</p>""", """<program>
  <pre>Pre stuff
  Indent being respected
  </pre>
  <input>code here

  must preserve Indenting
  </input>
  <tests>
Tests here

  must also preserve
  </tests>
</program>"""
]


class TestPtxFormatter(unittest.TestCase):

  def test_formatter_keeps_file_same(self):
    self.maxDiff = None
    for filename in sampleFiles:
      with open(join(dirname(__file__), "files", filename),
                "r",
                encoding="utf-8") as f:
        data = f.read()
        transformedData = formatPretext(data) + "\n"
        if WRITE_RESULT_FILES:
          with open(join(dirname(__file__), "files", "result-" + filename),
                    "w",
                    encoding="utf-8") as f2:
            f2.write(transformedData)
        self.assertEqual(data, transformedData)

  def test_formatter_keeps_expression_same(self):
    self.maxDiff = None
    for expr in fixedExpressions:
      self.assertEqual(formatPretext(expr), expr)
