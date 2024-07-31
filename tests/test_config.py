from typing import Self
import unittest

from os.path import dirname, join

from ptx_formatter.utils.config import Config, Preference


class TestConfig(unittest.TestCase):

  def test_load_file(self: Self):
    config = Config.standard()
    self.assertEqual(config.base_indent, "  ")
    self.assertEqual(config.add_doc_id, True)
    self.assertEqual(config.get_pref("ul"), Preference.Block)
    self.assertEqual(config.get_pref("var"), Preference.InlineEmpty)
