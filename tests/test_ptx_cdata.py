from tests.expressionTestCase import ExpressionTestCase


class TestPtxCdataFormatting(ExpressionTestCase):

  def test_cdata_created_if_setting_always(self):
    self.config.set_cdata("always")
    self.assertStaysSame("""
<pre><![CDATA[
  f(x) > 5 & g(x) < 2
]]></pre>""".strip())

  def test_cdata_not_created_if_setting_never(self):
    self.config.set_cdata("never")
    self.assertStaysSame("""
<pre>
  f(x) &gt; 5 &amp; g(x) &lt; 2
</pre>""".strip())

  def test_cdata_controlled_via_tag_list(self):
    self.config.set_cdata(["pre"])
    self.assertStaysSame("""
<section>
  <pre><![CDATA[
    f(x) > 5 & g(x) < 2
  ]]></pre>
  <input>
    f(x) &gt; 5 &amp; g(x) &lt; 2
  </input>
</section>""".strip())

  def test_cdata_controlled_via_number_of_escapes(self):
    self.config.set_cdata(3)
    self.assertStaysSame("""
<section>
  <pre><![CDATA[
    f(x) > 5 & g(x) < 2
  ]]></pre>
  <input>
    f(x) &gt; 5 &amp; g(x) = 2
  </input>
</section>""".strip())
