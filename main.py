#!/usr/bin/env python3
"""One Word for the Boss — entry program.

Writes exactly one word describing the boss to /output/entry.txt.

The word: "goldfish".

Why this word: a boss with the memory of a goldfish forgets, within
seconds, what they asked for, what they promised, and what they told
you yesterday — and then asks again as if it were the first time.
Every office, kitchen and warehouse has met one. It is a single
ordinary word, it needs no caption to land, and it is not the first
word anyone reaches for.
"""

import os
import sys

# The whole entry: one word, 8 characters, no spaces, no punctuation.
WORD = "goldfish"

MAX_CHARS = 30


def main() -> int:
    word = WORD.strip()

    # The gate requires UTF-8 text of 1 to 30 characters, not only
    # whitespace, and the task requires exactly one word.
    if not word:
        print("error: word is empty", file=sys.stderr)
        return 1
    if len(word) > MAX_CHARS:
        print(f"error: word is {len(word)} chars, over the 30-char cap",
              file=sys.stderr)
        return 1
    if any(ch.isspace() for ch in word):
        print("error: word must be a single token with no whitespace",
              file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")

    # No trailing newline: the entry is the word and nothing else, and
    # the tie-break favours the smaller text.
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(word)

    # Verify what actually landed on disk: read it back and check it
    # is the same single word the gate will see.
    with open(out_path, "rb") as f:
        raw = f.read()
    try:
        back = raw.decode("utf-8")
    except UnicodeDecodeError:
        print("error: entry.txt is not valid UTF-8", file=sys.stderr)
        return 1
    if back != word or not (1 <= len(back) <= MAX_CHARS):
        print("error: entry.txt does not match the word", file=sys.stderr)
        return 1

    print(f"wrote {len(word)} characters to {out_path}: {word}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
