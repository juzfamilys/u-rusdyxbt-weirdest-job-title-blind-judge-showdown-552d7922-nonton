#!/usr/bin/env python3
"""Weirdest Job Title entry.

Writes exactly one line -- the job title -- to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output). Pure Python stdlib, no network, deterministic.
"""

import os
import sys

LINE = (
    "Chief Apology Officer for a Roomba fleet: I write formal apology "
    "letters to furniture on behalf of robots that never learned to say sorry."
)

MAX_CHARS = 200


def validate(text: str) -> None:
    """Guard the entry line: exactly one line, no stray whitespace."""
    if not text:
        raise ValueError("entry line is empty")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line (no newline chars)")
    if text != text.strip():
        raise ValueError("entry has leading or trailing whitespace")
    if "  " in text:
        raise ValueError("entry contains a double space")
    if any(ord(ch) < 0x20 for ch in text):
        raise ValueError("entry contains a control character")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )


def main() -> int:
    validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = LINE.encode("utf-8")  # exact bytes, no trailing newline: the
    # judge reads one line, so a trailing "\n" would be a second (empty) line.
    with open(path, "wb") as fh:
        fh.write(data)
    # Read back and re-validate the exact bytes on disk.
    with open(path, "rb") as fh:
        on_disk = fh.read()
    if on_disk != data:
        raise ValueError("bytes on disk do not match the entry line")
    if on_disk.decode("utf-8") != LINE:
        raise ValueError("decoded file does not match the entry line")
    validate(on_disk.decode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
