from tests.expressionTestCase import ExpressionTestCase


class TestPtxNewlineSettings(ExpressionTestCase):

  def test_spacing_between_inlined_tags_is_preserved(self):
    self.assertStaysSame("""
<section>
  <p>An inlined <c>tag</c> and <em>spacing</em> <c>around</c> <em>only if</em><c>present</c></p>
</section>""".strip())
