from typing import Annotated, Optional

import sys
import typer

from ptx_formatter.formatter import formatPretext, Config
from ptx_formatter.version import __version__


def version_callback(value: bool):
  if value:
    print(f"{__version__}")
    raise typer.Exit()


app = typer.Typer(add_completion=False)


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
        Optional[int],
        typer.Option(
            "--indent",
            "-i",
            help=
            "Number of characters for space-indent. Overwrites the standard configuration. Ignored if tab_indent is set.",
            show_default=False,
        ),
    ] = None,
    tabIndent: Annotated[
        Optional[bool],
        typer.Option(
            "--tab-indent",
            "-t",
            help=
            "Indent using tabs instead. Overwrites the standard configuration."
        )] = None,
    configFile: Annotated[
        Optional[typer.FileText],
        typer.Option(
            "--config-file",
            "-c",
            help=
            "File to use as configuration. If omitted, a standard configuration file is loaded.",
            show_default=False,
        ),
    ] = None,
    showConfig: Annotated[
        bool,
        typer.Option(
            "--show-config",
            help=
            "Print the current configuration and exit. This is in a TOML form that could be saved to a file and used as a start file."
        )] = False,
    version: Annotated[bool,
                       typer.Option("--version",
                                    callback=version_callback,
                                    help="Print the version and exit.",
                                    is_eager=True)] = None,
):
  """
  Reformats a PreText XML document to follow a standard format.
  """
  if addDocId is None:
    addDocId = outputFile is not None
  config = assemble_config(configFile, tabIndent, indent, addDocId)
  if showConfig:
    sys.stdout.write(config.print())
    raise typer.Exit()
  inputString = (inputFile or sys.stdin).read()
  result = formatPretext(inputString, config)
  (outputFile or sys.stdout).write(result)


def main():
  app()


def assemble_config(configFile, indent: int | None, tabIndent: bool | None,
                    addDocId: bool) -> Config:
  if configFile is not None:
    config = Config.fromFile(configFile)
  else:
    config = Config.standard()

  config.set_add_doc_id(addDocId)

  if tabIndent is not None:
    config.set_indent("\t")
  elif indent is not None:
    config.set_indent(indent)
  return config


if __name__ == "__main__":
  main()
