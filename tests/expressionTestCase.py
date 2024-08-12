from typing import Self
import unittest

from ptx_formatter.formatter import formatPretext
from ptx_formatter.utils.config import Config


class ExpressionTestCase(unittest.TestCase):
  """Base class for our testing of expressions. It contains a
  standard configuration file that excludes the xml document identifier"""

  def __init__(self: Self, methodName: str):
    super().__init__(methodName)
    self.config = Config.standard()
    self.config.set_add_doc_id(False)

  def assertStaysSame(self: Self, expr: str):
    return self.assertEqual(formatPretext(expr, self.config), expr)
