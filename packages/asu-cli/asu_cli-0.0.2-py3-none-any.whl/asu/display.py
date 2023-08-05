import json
from types import GeneratorType
from typing import Any, Dict, Generator, List, Optional, Sequence, Union, cast

from rich import box
from rich.console import Console
from rich.live import Live
from rich.table import Table


def as_table(dicts: Optional[Sequence[Dict[str, Any]]], keys: Optional[List[str]] = None) -> List[List[Optional[str]]]:
    """
    Converts a list of dictionaries to a list of lists (table), ordered by specified keys.

    :param dicts: list of dictionaries
    :param keys: ordered list of keys to include in each row, or None to use the keys from the first dict
    :return: list of lists, with None values if there's no value for a key
    """
    if not dicts:
        return []

    if keys is None:
        keys = list(dicts[0].keys())
    return [keys] + [[str(d.get(f, "")) if d.get(f, "") else None for f in keys] for d in dicts]  # type: ignore


def pretty_table(table: Optional[Sequence[Sequence[Optional[str]]]]) -> str:
    """Formats a table as a pretty string for printing."""
    if not table:
        return ""

    padding = 2
    col_width = [0] * len(table[0])
    for row in table:
        for idx, col in enumerate(row):
            if col is not None and len(col) > col_width[idx]:
                col_width[idx] = len(col)

    return "\n".join(
        "".join(
            [
                "".join(
                    (col if col is not None else "").ljust(
                        col_width[idx] + padding
                    )
                    for idx, col in enumerate(row)
                )
            ]
        )
        for row in table
    )


def pretty_print(result: Union[Generator[Sequence[Optional[str]], None, None],
                               List[Dict[str, str]], List[List[Optional[str]]], Dict[str, str], str, None]) -> None:
    """print table/json, instead of showing a dict, or list of dicts."""

    console = Console()

    if isinstance(result, GeneratorType):
        header = next(result)
        column_names = cast(List[str], header)
        table = Table(box=box.SIMPLE)
        for c in column_names:
            table.add_column(c)

        with Live(table, refresh_per_second=1):
            for row in cast(GeneratorType, result):
                table.add_row(*row)

    elif isinstance(result, list):
        if isinstance(result[0], dict):
            rows = as_table(cast(List[Dict[str, str]], result))
        elif isinstance(result[0], list):
            rows = result
        else:
            raise TypeError(f"not implemented for element type {type(result[0]).__name__}")
        if len(rows) == 0:
            console.print("No results")
            return

        column_names = cast(List[str], rows[0])
        table = Table(box=box.SIMPLE)
        for c in column_names:
            table.add_column(c)

        for r in rows[1:]:
            table.add_row(*r)

        console.print(table)
    elif isinstance(result, dict):
        print(json.dumps(result, default=str))
    elif not result:
        print("Done ✨")
    else:
        print(result)
