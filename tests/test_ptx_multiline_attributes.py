import unittest

from ptx_formatter.formatter import formatPretext
from ptx_formatter.utils.config import Config


class TestPtxMultilineAttributes(unittest.TestCase):

  def test_no_multiline_attrs_when_setting_false(self):
    config = Config.standard()
    config.set_add_doc_id(False)
    config.set_multiline_attrs("never")
    expr = """<section color="something" color-bg="else"></section>"""
    self.assertEqual(formatPretext(expr, config), expr)

  def test_no_multiline_attrs_when_below_threshold(self):
    config = Config.standard()
    config.set_add_doc_id(False)
    config.set_multiline_attrs(3)
    expr = """<section color="something" color-bg="else"></section>"""
    self.assertEqual(formatPretext(expr, config), expr)

  def test_multiline_attrs_when_meeting_threshold(self):
    config = Config.standard()
    config.set_add_doc_id(False)
    config.set_multiline_attrs(2, 1)
    expr = """<section\n color="something"\n color-bg="else"></section>"""
    self.assertEqual(formatPretext(expr, config), expr)

  def test_multiline_attrs_start_on_open_when_indent_0(self):
    config = Config.standard()
    config.set_add_doc_id(False)
    config.set_multiline_attrs(2, 0)
    expr = """
<section color="something"
         color-bg="else"></section>""".strip()
    self.assertEqual(formatPretext(expr, config), expr)
