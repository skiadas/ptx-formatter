from glob import glob
from pathlib import Path
import time
from typing import Annotated, Optional
from rich.progress import track

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
def _mainPtx(
    addDocId: Annotated[
        Optional[bool],
        typer.Option(
            "--add-doc-type/--skip-doc-type",
            help=
            "Whether to include or skip the XML doc identifier <?xml ...>. The identifier will by default be added if the output is a file and skipped if the output is stdout.",
            show_default=False,
        )] = None,
    inPlace: Annotated[
        bool,
        typer.Option(
            "--in-place",
            "-p",
            help=
            "Whether to process in-place. If this option is present, there should be no output file.",
            show_default=False,
        ),
    ] = False,
    recursive: Annotated[
        bool,
        typer.Option(
            "--recursive",
            "-r",
            help=
            "Enter recursive mode, converting all *.ptx files. Requires in-place and a directory as inputfile.",
            show_default=False,
        ),
    ] = False,
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
    input_file: Annotated[
        Optional[Path],
        typer.Argument(
            help=
            "File to use as input. If omitted, read the contents of standard input.",
            show_default=False,
        ),
    ] = None,
    output_file: Annotated[
        Optional[Path],
        typer.Argument(
            help=
            "File to use as output. If omitted, write the results to standard output.",
            show_default=False,
        ),
    ] = None,
):
  """
  Reformats a PreText XML document to follow a standard format.
  """
  if addDocId is None:
    addDocId = output_file is not None or inPlace
  config = assemble_config(configFile, indent, tabIndent, addDocId)
  if showConfig:
    sys.stdout.write(config.print())
    raise typer.Exit()
  if recursive:
    if not inPlace or input_file is None or not input_file.is_dir():
      print("ERROR: recursive option requires --in-place and a directory.")
      raise typer.Abort()
    return process_recursive(input_file, config)
  if inPlace:
    if output_file is not None:
      print("ERROR: Cannot specify both --in-place and an output file.")
      raise typer.Abort()
    output_file = input_file
  inputString = read_file_or_stdin(input_file)
  formatted = formatPretext(inputString, config)
  write_file_or_stdout(output_file, formatted)


def process_recursive(directory: Path, config: Config) -> None:
  files = glob("**/*.ptx", root_dir=directory, recursive=True)
  if sys.stdout.isatty():
    for file in track(files, description="Processing ..."):
      write_in_place(directory / file, config)
  else:
    for file in files:
      write_in_place(directory / file, config)
  raise typer.Exit()


def read_file_or_stdin(input_file: Path | None) -> str:
  if input_file is None:
    return sys.stdin.read()
  with open(input_file, "r", encoding="utf-8") as f:
    return f.read()


def write_file_or_stdout(output_file: Path | None, data: str) -> str:
  if output_file is None:
    return sys.stdout.write(data)
  with open(output_file, "w", encoding="utf-8") as f:
    return f.write(data)


def write_in_place(inPlaceFile, config):
  with open(inPlaceFile, "r") as f:
    inputString = f.read()
  result = formatPretext(inputString, config)
  with open(inPlaceFile, "w") as f:
    f.write(result)


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
