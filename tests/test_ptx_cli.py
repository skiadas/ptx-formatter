import difflib
import unittest
import pytest
from typer.testing import CliRunner

from ptx_formatter.cli import app

from shutil import copyfile
from os.path import dirname, join

sampleFiles = ["fewNewlines.ptx", "fewWithListing.ptx"]


class TestPtxCli(unittest.TestCase):

  @pytest.fixture(autouse=True)
  def init(self, tmp_path):
    self.tmp_path = tmp_path

  def setUp(self) -> None:
    self.runner = CliRunner()
    self.maxDiff = None
    for filename in sampleFiles:
      copyfile(join(dirname(__file__), "files", filename),
               self.tmp_path / filename)
    return super().setUp()

  def test_formatter_reads_from_file_and_writes_to_file(self):
    inFile = self.tmp_path / sampleFiles[0]
    outFile = self.tmp_path / ("result" + sampleFiles[0])
    result = self.runner.invoke(app, ["-f", inFile, "-o", outFile])
    self.assertEqual(result.exit_code, 0)
    self.assertFilesEqual(inFile, outFile)

  def test_formatter_can_read_from_stdin_and_write_to_stdout(self):
    inputContents = "".join(getLines(self.tmp_path / sampleFiles[0])[2:])
    result = self.runner.invoke(app, [], input=inputContents)
    self.assertEqual(result.exit_code, 0)
    self.assertEqual(result.output, inputContents)

  def test_formatter_can_rewrite_file_in_place(self):
    inputFile = self.tmp_path / sampleFiles[0]
    backupFile = self.tmp_path / ("backup" + sampleFiles[0])
    # Create backup file with indentation 2
    self.runner.invoke(app, ["-f", inputFile, "-o", backupFile, "-i", "2"])
    # Change input file in-place with indentation 2
    result = self.runner.invoke(app, ["-p", inputFile, "-i", "2"])
    self.assertEqual(result.exit_code, 0)
    self.assertFilesEqual(inputFile, backupFile)

  def assertFilesEqual(self, inFile, outFile):
    diff = difflib.unified_diff(getLines(inFile), getLines(outFile))
    errors = [l for l in diff]
    if errors != []:
      print("".join(errors))
      self.fail("files differ")


def getLines(filepath):
  with open(filepath, "r", encoding="utf-8") as f:
    return f.readlines()
