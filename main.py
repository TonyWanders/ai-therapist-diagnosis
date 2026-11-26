#!/usr/bin/env python3
# Your AI Therapist's Diagnosis
#
# A tiny deterministic entry for the make.fun competition. The program
# writes one fixed funny diagnosis to a text file. There is nothing
# to configure, nothing to fetch and nothing random: the line below is
# a constant, and the file it lands in is chosen from the command line,
# then the OUTPUT_PATH environment variable, then a fixed default.
#
# Usage:
#   python3 main.py [path]
#
# The entry must stay inside the competition gate of 1 to 200
# characters and must not be blank. If it ever fails that gate the
# program complains on stderr and exits with status 1 instead of
# writing anything.

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# The diagnosis. One string, 154 characters, written out in full so
# the output is obvious to anyone reading the source.
DIAGNOSIS = (
    "Diagnosis: chronic validation-seeking. "
    "You ask an AI how you feel, then argue with the answer. "
    "That is progress: you used to argue with yourself for free."
)

# Competition gate, inclusive on both ends.
LOWER_LIMIT = 1
UPPER_LIMIT = 200

# Where the entry goes when no path is given anywhere else.
FALLBACK_PATH = Path("/output/entry.txt")


def resolve_output_path() -> Path:
    """Work out where the entry should be written.

    First argument wins, then $OUTPUT_PATH, then the fallback. An
    empty environment value counts as unset, so it falls through.
    """
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    if value := os.environ.get("OUTPUT_PATH"):
        return Path(value)
    return FALLBACK_PATH


def gate_bounds() -> tuple[int, int]:
    """Return the competition gate as (lower, upper), inclusive."""
    return (LOWER_LIMIT, UPPER_LIMIT)


def validate(text: str) -> int:
    """Check the entry against the competition gate.

    Returns the number of characters when the text is inside 1 to
    200 characters and is not only white space. Raises ValueError
    otherwise, with a message describing what went wrong.
    """
    lower, upper = gate_bounds()
    length = len(text)
    if length < lower:
        raise ValueError("entry is empty, needs at least 1 character")
    if length > upper:
        raise ValueError(
            f"entry is {length} characters, over the {upper} limit"
        )
    if text.isspace():
        raise ValueError("entry is only white space")
    return length


def write_entry(path: Path, text: str) -> int:
    """Validate the text, write it to path, and return its length.

    The parent directory is created when it does not exist yet, so
    running against a fresh /output works. The file is written as
    plain UTF-8 with no trailing newline added, exactly the text
    given. Validation happens before anything touches the disk.
    """
    count = validate(text)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return count


def entry_text() -> str:
    """Return the diagnosis line exactly as it is written out."""
    return DIAGNOSIS


def entry_length() -> int:
    """Return the diagnosis line's character count."""
    return len(entry_text())


def main() -> int:
    """Entry point: write the diagnosis and report what happened."""
    path = resolve_output_path()
    try:
        chars = write_entry(path, entry_text())
    except ValueError as exc:
        print(f"invalid entry: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"could not write entry: {exc}", file=sys.stderr)
        return 1
    print(f"wrote {chars} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
