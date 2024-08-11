import unittest

from ptx_formatter.formatter import formatPretext
from ptx_formatter.utils.config import Config


class TestPtxCdataFormatting(unittest.TestCase):

  def test_multiple_namespaces_on_pretext_tag(self):
    config = Config.standard()
    config.set_add_doc_id(False)
    config.set_cdata(3)
    expr = """
<pretext xmlns:html="http://www.w3.org/1999/xhtml" xmlns:xi="http://www.w3.org/2001/XInclude">
  <xi:include href="./sage/groups-info.xml" />
</pretext>""".strip()
    self.assertEqual(formatPretext(expr, config), expr)

  def test_namespaces_go_last_and_ids_go_first(self):
    config = Config.standard()
    config.set_add_doc_id(False)
    config.set_cdata(3)
    expr = """
<pretext xml:id="something" color="purple" xmlns:xi="http://www.w3.org/2001/XInclude">
  <xi:include href="./sage/groups-info.xml" />
</pretext>""".strip()
    self.assertEqual(formatPretext(expr, config), expr)
