from tests.expressionTestCase import ExpressionTestCase


class TestPtxNewlineSettings(ExpressionTestCase):

  def test_inlined_elements_should_not_get_extra_spaces_inserted(self):
    self.assertStaysSame("""
<section>
  <p>Some text <em>here</em><em>back-to-back</em> more</p>
</section>""".strip())
