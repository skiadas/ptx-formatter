from tests.expressionTestCase import ExpressionTestCase


class TestPtxInlineComments(ExpressionTestCase):

  def test_inline_comments_stay_inline(self):
    self.assertStaysSame("""
<section>
  <!-- comment before -->
  <p>Some text here</p>  <!-- A comment here -->
</section>""".strip())

  def test_consecutive_comments_go_on_separate_lines(self):
    self.assertStaysSame("""
<section>
  <!-- comment before -->
  <!-- Another comment here -->
  <p>Some text here</p>
</section>""".strip())
