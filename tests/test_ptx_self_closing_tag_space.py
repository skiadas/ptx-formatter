from tests.expressionTestCase import ExpressionTestCase


class TestPtxSelfClosingTagSpace(ExpressionTestCase):

  def test_when_self_closing_space_is_true_then_space_added(self):
    self.assertStaysSame("""
<section>
  <image />
  <image src="http://somewhere.com" />
</section>""".strip())

  def test_when_self_closing_space_is_false_then_no_space_added(self):
    self.config.set_self_closing_space(False)
    self.assertStaysSame("""
<section>
  <image/>
  <image src="http://somewhere.com"/>
</section>""".strip())
