import unittest

from os.path import dirname, join
from ptx_formatter.formatter import formatPretext
from ptx_formatter.utils.config import Config

# Turn this on if you want result files produced
# for manual comparison
WRITE_RESULT_FILES = False

sampleFiles = ["fewNewlines.ptx", "fewWithListing.ptx"]

fixedExpressions = [
    """<premise>
  <p>A paragraph</p>
</premise>""", """<section>
  <premise>
    <p>A paragraph</p>
  </premise>
  <response>
    Some text with some math x &gt; 3
    <p>Another paragraph</p>
  </response>
</section>""", """<block>
  <p>A paragraph</p>
  <p>Another paragraph</p>
</block>""", """<p>
  <ul></ul>
</p>""", """<program>
  <pre>Pre stuff
  Indent being respected
  </pre>
  <input>code here and must escape xml specials

  #include &lt;stdio.h&gt;

  must preserve Indenting
  And ampersand: &amp;
  </input>
  <tests>
Tests here

  must also preserve
  </tests>
</program>""", """
<pretext xmlns:xi="http://www.w3.org/2001/XInclude">
  <xi:include href="./bookinfo.xml" />
</pretext>""".strip()
]


class TestPtxFormatter(unittest.TestCase):

  def test_formatter_keeps_file_same(self):
    self.maxDiff = None
    config = Config.standard()
    config.set_add_doc_id(True)

    for filename in sampleFiles:
      with open(join(dirname(__file__), "files", filename),
                "r",
                encoding="utf-8") as f:
        data = f.read()
        transformedData = formatPretext(data, config)
        if WRITE_RESULT_FILES:
          with open(join(dirname(__file__), "files", "result-" + filename),
                    "w",
                    encoding="utf-8") as f2:
            f2.write(transformedData)
        self.assertEqual(data, transformedData)

  def test_formatter_keeps_expression_same(self):
    self.maxDiff = None
    config = Config.standard()
    config.set_add_doc_id(False)
    for expr in fixedExpressions:
      self.assertEqual(formatPretext(expr, config), expr)
