import unittest

from ptx_formatter.formatter import formatPretext
from ptx_formatter.utils.config import Config


class TestPtxProcessingInstructions(unittest.TestCase):

  def test_processing_instructions_are_maintained(self):
    config = Config.standard()
    config.set_add_doc_id(False)
    config.set_cdata(3)
    expr = """
<?xml-stylesheet type="text/css" href="../../meta/OxygenXML/frameworks/pretext/oxygen-ptx.css"?>
<section>
  <p>Some text here</p>
</section>""".strip()
    self.assertEqual(formatPretext(expr, config), expr)
