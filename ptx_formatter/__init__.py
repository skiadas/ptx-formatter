from typing import Annotated, Optional
from pathlib import Path
import sys

import typer

from ptx_formatter.formatter import formatPretext, BlankLines

__version__ = "0.0.1"


def version_callback(value: bool):
  if value:
    print(f"{__version__}")
    raise typer.Exit()


app = typer.Typer()


@app.command()
def mainPtx(
    addDocId: Annotated[
        Optional[bool],
        typer.Option(
            "--add-doc-type/--skip-doc-type",
            help=
            "Whether to include or skip the XML doc identifier <?xml ...>. The identifier will by default be added if the output is a file and skipped if the output is stdout.",
            show_default=False,
        )] = None,
    inputFile: Annotated[
        Optional[typer.FileText],
        typer.Option(
            "--file",
            "-f",
            help=
            "File to use as input. If omitted, read the contents of standard input.",
            show_default=False,
        ),
    ] = None,
    outputFile: Annotated[
        Optional[typer.FileTextWrite],
        typer.Option(
            "--output",
            "-o",
            help=
            "File to use as output. If omitted, write the results to standard output.",
            show_default=False,
        ),
    ] = None,
    indent: Annotated[
        int,
        typer.Option(
            "--indent",
            "-i",
            help=
            "Number of characters for space-indent (default 2). Ignored if tab_indent is set.",
            show_default=False,
        ),
    ] = 2,
    tabIndent: Annotated[
        bool,
        typer.Option("--tab-indent", "-t", help="Indent using tabs instead."
                    )] = False,
    version: Annotated[
        bool,
        typer.Option("--version", callback=version_callback, is_eager=True
                    )] = None,
    blankLines: Annotated[
        BlankLines,
        typer.Option(
            "--blank-lines",
            help="How many blank lines to have at the final document.",
            show_default=False,
        )] = BlankLines.few,
    breakSentences: Annotated[
        bool,
        typer.Option(
            "--break-sentences",
            help="If set, a newline will be formed at the end of each sentence.",
            show_default=False)] = False):
  """
  Reformats a PreText XML document to follow a standard format.
  """
  inputString = (inputFile or sys.stdin).read()
  if addDocId is None:
    addDocId = outputFile is not None
  result = formatPretext(inputString,
                         breakSentences=breakSentences,
                         blankLines=blankLines,
                         addDocumentIdentifier=addDocId,
                         indent="\t" if tabIndent else " " * indent)
  (outputFile or sys.stdout).write(result)


def main():
  app()


if __name__ == "__main__":
  main()

# app = typer.Typer()

# @app.callback()
# def callback():
#     """
#     Awesome Portal Gun
#     """

# @app.command()
# def shoot():
#     """
#     Shoot the portal gun
#     """
#     typer.echo("Shooting portal gun")

# @app.command()
# def load():
#     """
#     Load the portal gun
#     """
#     typer.echo("Loading portal gun")
