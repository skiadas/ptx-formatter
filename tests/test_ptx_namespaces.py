from tests.expressionTestCase import ExpressionTestCase


class TestPtxCdataFormatting(ExpressionTestCase):

  def test_multiple_namespaces_on_pretext_tag(self):
    self.assertStaysSame("""
<pretext xmlns:html="http://www.w3.org/1999/xhtml" xmlns:xi="http://www.w3.org/2001/XInclude">
  <xi:include href="./sage/groups-info.xml" />
</pretext>""".strip())

  def test_namespaces_go_last_and_ids_go_first(self):
    self.assertStaysSame("""
<pretext xml:id="something" color="purple" xmlns:xi="http://www.w3.org/2001/XInclude">
  <xi:include href="./sage/groups-info.xml" />
</pretext>""".strip())
