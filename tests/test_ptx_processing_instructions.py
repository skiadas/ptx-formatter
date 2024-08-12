from tests.expressionTestCase import ExpressionTestCase


class TestPtxProcessingInstructions(ExpressionTestCase):

  def test_processing_instructions_are_maintained(self):
    self.assertStaysSame("""
<?xml-stylesheet type="text/css" href="../../meta/OxygenXML/frameworks/pretext/oxygen-ptx.css"?>
<section>
  <p>Some text here</p>
</section>""".strip())
