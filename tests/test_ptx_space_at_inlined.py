from tests.expressionTestCase import ExpressionTestCase


class TestPtxSpacingAtInlines(ExpressionTestCase):

  def test_no_space_at_start_or_end_of_inlined_tag(self):
    self.assertBecomes("<p>\n Hey there partner <c>Howdy</c>\n</p>",
                       "<p>Hey there partner <c>Howdy</c></p>")

  def test_non_inlined_example_of_wrong_indent(self):
    self.assertBecomes('''<p>
      This is really not a great class, but it will do as a first example. So what all do we have here?
      <ul>
        <li>
  A class is declared with the keyword `class`. It is followed by the name for the class, which is customarily in "upper camel case" form. Then the customary curly braces demarcate the contents of the class definition.
    </li></ul></p>''',
    '''<p>
  This is really not a great class, but it will do as a first example. So what all do we have here?
  <ul>
    <li>A class is declared with the keyword `class`. It is followed by the name for the class, which is customarily in "upper camel case" form. Then the customary curly braces demarcate the contents of the class definition.</li>
  </ul>
</p>''')
