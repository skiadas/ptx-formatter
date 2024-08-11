import unittest

from os.path import dirname, join
from ptx_formatter.formatter import formatPretext
from ptx_formatter.utils.config import Config


class TestPtxCdataFormatting(unittest.TestCase):

  def test_cdata_created_if_setting_always(self):
    config = Config.standard()
    config.set_add_doc_id(False)
    config.set_cdata("always")
    expr = """
<pre><![CDATA[
  f(x) > 5 & g(x) < 2
]]></pre>""".strip()
    self.assertEqual(formatPretext(expr, config), expr)

  def test_cdata_not_created_if_setting_never(self):
    config = Config.standard()
    config.set_add_doc_id(False)
    config.set_cdata("never")
    expr = """
<pre>
  f(x) &gt; 5 &amp; g(x) &lt; 2
</pre>""".strip()
    self.assertEqual(formatPretext(expr, config), expr)

  def test_cdata_controlled_via_tag_list(self):
    config = Config.standard()
    config.set_add_doc_id(False)
    config.set_cdata(["pre"])
    expr = """
<section>
  <pre><![CDATA[
    f(x) > 5 & g(x) < 2
  ]]></pre>
  <input>
    f(x) &gt; 5 &amp; g(x) &lt; 2
  </input>
</section>""".strip()
    self.assertEqual(formatPretext(expr, config), expr)

  def test_cdata_controlled_via_number_of_escapes(self):
    config = Config.standard()
    config.set_add_doc_id(False)
    config.set_cdata(3)
    expr = """
<section>
  <pre><![CDATA[
    f(x) > 5 & g(x) < 2
  ]]></pre>
  <input>
    f(x) &gt; 5 &amp; g(x) = 2
  </input>
</section>""".strip()
    self.assertEqual(formatPretext(expr, config), expr)
