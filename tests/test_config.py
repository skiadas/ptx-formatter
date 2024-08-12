from typing import Self
import unittest

from ptx_formatter.utils.config import Config, Preference


class TestConfig(unittest.TestCase):

  def test_load_file(self: Self):
    config = Config.standard()
    self.assertEqual(config._base_indent, "  ")
    self.assertEqual(config._add_doc_id, True)
    self.assertEqual(config.get_pref("ul"), Preference.Block)
    self.assertEqual(config.get_pref("var"), Preference.InlineEmpty)
