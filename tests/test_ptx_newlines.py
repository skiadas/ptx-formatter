from tests.expressionTestCase import ExpressionTestCase


class TestPtxNewlineSettings(ExpressionTestCase):

  def test_newline_added_after_specified_tags(self):
    self.config.set_emptyline_after(["title"])
    self.config.set_emptyline_before([])
    self.assertStaysSame("""
<section>
  <title>Some title here</title>

  <p>Some text here</p>
</section>""".strip())

  def test_newline_added_before_specified_tags(self):
    self.config.set_emptyline_after([])
    self.config.set_emptyline_before(["p"])
    self.assertStaysSame("""
<section>
  <title>Some title here</title>

  <p>Some text here</p>
</section>""".strip())

  def test_no_newline_added_after_last_tag_or_before_first_tag(self):
    self.config.set_emptyline_after(["title"])
    self.config.set_emptyline_before(["title"])
    self.assertStaysSame("""
<section>
  <title>Some title here</title>
</section>""".strip())

  def test_no_double_newlines(self):
    self.config.set_emptyline_after(["p"])
    self.config.set_emptyline_before(["p"])
    self.assertStaysSame("""
<section>
  <p>Something here</p>

  <p>Something else here</p>
</section>""".strip())

  def test_block_rendering_with_last_element_string_should_not_get_extra_newlines(
      self):
    self.assertStaysSame(r"""<chapter>
  <title>test formatting</title>
  <p>
    The Pythagorean Theorem states
    <me>
      r = \sqrt{{x^2}+{y^2}}
    </me>
    .
  </p>
  <p>
    <md>
      <mrow>(a+b)^2</mrow>
    </md>
    .  Now...
  </p>
</chapter>""")
