import unittest

from os.path import dirname, join
from ptx_formatter.formatter import formatPretext

sampleFiles = []  # TODO: create test files


class TestPtxFormatter(unittest.TestCase):

  def test_formatter_keeps_file_same(self):
    self.maxDiff = None
    for filename in sampleFiles:
      with open(join(dirname(__file__), "files", filename),
                "r",
                encoding="utf-8") as f:
        data = f.read()
        transformedData = formatPretext(data)
        with open(join(dirname(__file__), "files", "result-" + filename),
                  "w",
                  encoding="utf-8") as f2:
          f2.write(transformedData)
        self.assertEqual(data, transformedData)
