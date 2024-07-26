import unittest

from os.path import dirname, join
from ptx_formatter.formatter import joinLines


class TestJoinLines(unittest.TestCase):

  def test_verbatim_is_not_changed(self):
    input = """<?xml ?>
<listing>
  <tests>
    Some code here

    More code here
      indented more
  </tests>
</listing>"""
    expected = """<?xml ?> <listing>
  <tests>
    Some code here

    More code here
      indented more
</tests> </listing>"""
    output = joinLines(input)
    print(output)
    print(expected)
    self.assertEqual(expected, output)
