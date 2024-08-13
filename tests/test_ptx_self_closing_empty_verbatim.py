from tests.expressionTestCase import ExpressionTestCase


class TestPtxSelfClosing(ExpressionTestCase):

  def test_specific_self_closing_tags(self):
    self.assertStaysSame("""
<section>
  <pre src="http://somewhere.com" />
</section>""".strip())
