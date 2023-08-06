import typer
import re
import itertools
from typing import Optional, List, Iterator, Tuple
from pathlib import Path
import logging


app = typer.Typer(add_completion=False)

# This only supports strict tables where each row begins and ends with a "|"
delimiter_pattern = re.compile("^\|[ :]-{3,}[ :](\|[ :]-{3,}[ :])*\|$")
delimiter_seperator_pattern = re.compile(r"-{3,}")


def count_delimiter_row_cells(line: str) -> Optional[int]:
    if delimiter_pattern.match(line) is None:
        return None
    return len(delimiter_seperator_pattern.findall(line))


row_pattern = re.compile(r"^\|(.*?[^\\]\|)+$")
row_separator_pattern = re.compile(r"(?<!\\)\|")


def count_row_cells(line: str) -> Optional[int]:
    line = line.strip()
    if row_pattern.match(line) is None:
        return None
    return len(row_separator_pattern.split(line)) - 2


codeblock_separator_pattern = re.compile(r"^```.*")


def is_codeblock_separator(line: str) -> bool:
    return codeblock_separator_pattern.match(line) is not None


def split_from_codeblocks(
    lines: List[Tuple[int, str]]
) -> Iterator[List[Tuple[int, str]]]:
    last_idx = -1
    current_block = []
    for idx, line in lines:
        if idx != last_idx + 1:
            if current_block:
                yield current_block
                current_block = []
        last_idx = idx
        current_block.append((idx, line))
    if current_block:
        yield current_block


def pad_row(row: str, max_widths: List[int]) -> str:
    cells = row_separator_pattern.split(row)[1:-1]
    cells_resized = [cell.ljust(width) for width, cell in zip(max_widths, cells)]
    row_inner = "|".join(cells_resized)
    return f"|{row_inner}|"


def pad_seperator(row: str, max_widths: List[int]) -> str:
    cells = row_separator_pattern.split(row)[1:-1]
    cells_resized = [
        f"{cell[0]}{cell[1:-1].ljust(width-2, '-')}{cell[-1]}"
        for width, cell in zip(max_widths, cells)
    ]
    row_inner = "|".join(cells_resized)
    return f"|{row_inner}|"


def process_chunk(lines: List[Tuple[int, str]]) -> Iterator[Tuple[int, str]]:
    last_idx = -1
    line_dict = dict(lines)
    delimiter_rows = [
        (idx, count_delimiter_row_cells(line))
        for idx, line in lines
        if count_delimiter_row_cells(line) is not None
    ]
    for idx, cols in delimiter_rows:
        if idx <= last_idx:
            logging.debug(f"Line {idx+1} not a delimiter line due to being a table row")
            continue
        if idx - 1 not in line_dict or count_row_cells(line_dict[idx - 1]) is None:
            logging.debug(
                f"Line {idx+1} not a delimiter line due to previous line not being a row"
            )
            continue
        if idx - 1 in line_dict and count_row_cells(line_dict[idx - 1]) != cols:
            logging.debug(
                f"Line {idx+1} not a delimiter line due to previous line not having an equal number of cells"
            )
            continue
        logging.debug(f"Line {idx} is the beginning of a table")
        rows = itertools.takewhile(
            count_row_cells,
            (line_dict.get(rowidx) for rowidx in itertools.count(start=idx + 1)),
        )
        table_strings = [line_dict[idx - 1], line_dict[idx], *rows]
        logging.debug(f"Table = {table_strings!r}")
        columns = count_row_cells(table_strings[0])
        max_widths = [5] * columns
        for row in table_strings:
            cells = row_separator_pattern.split(row)[1:-1]
            for i in range(columns):
                max_widths[i] = max(max_widths[i], len(cells[i]))
        logging.debug(f"max_width = {max_widths!r}")
        logging.debug("Before:")
        logging.debug(
            "*" * 10 + " BEFORE " + "*" * 10 + "\n" + "\n".join(table_strings)
        )
        table_strings[0] = pad_row(table_strings[0], max_widths)
        table_strings[1] = pad_seperator(table_strings[1], max_widths)
        table_strings[2:] = [pad_row(row, max_widths) for row in table_strings[2:]]
        logging.debug("*" * 10 + " AFTER " + "*" * 10 + "\n" + "\n".join(table_strings))
        first_row_idx = idx - 1
        for i, row in enumerate(table_strings):
            yield first_row_idx + i, row


def reformat(target: Path, inline: bool):
    with target.open("r") as f:
        file_contents = f.read()
    lines = file_contents.split("\n")
    enum_lines = list(enumerate(lines))
    codeblock_idxs = set()
    codeblock_delimiters = [
        idx for idx, line in enum_lines if is_codeblock_separator(line)
    ]
    codeblock_starts = codeblock_delimiters[::2]
    codeblock_ends = codeblock_delimiters[1::2]
    for start, end in zip(codeblock_starts, codeblock_ends):
        logging.debug(f"Codeblock from {start}-{end}")
        codeblock_idxs.update(range(start, end + 1))
    noncodeblock_lines = [
        (idx, line) for idx, line in enum_lines if idx not in codeblock_idxs
    ]
    noncodeblock_chunks = split_from_codeblocks(noncodeblock_lines)
    new_lines = lines[:]
    for chunk in noncodeblock_chunks:
        for idx, line in process_chunk(chunk):
            new_lines[idx] = line
    typer.echo("\n".join(new_lines))
    if inline:
        with target.open("w") as f:
            f.write("\n".join(new_lines))


@app.command()
def main(
    target: Path,
    inline: bool = typer.Option(
        False,
        "--inline",
        "-i",
        help="Change the file",
    ),
    recursive: bool = typer.Option(
        False,
        "--recursive",
        "-r",
        help="If targeting a directory, format all markdown files in the directory",
    ),
):
    if not target.exists():
        typer.secho(
            f"Target does not exist",
            err=True,
            fg=typer.colors.YELLOW,
        )
        raise typer.Abort()

    if target.is_file():
        reformat(target, inline)
    elif target.is_dir():
        if recursive:
            for path in target.glob("**/*.md"):
                reformat(path, inline)
        else:
            typer.secho(
                f"Target is a directory, either target a file or pass -r to recurse",
                err=True,
                fg=typer.colors.YELLOW,
            )
            raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
