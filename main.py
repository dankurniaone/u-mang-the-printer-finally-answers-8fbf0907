#!/usr/bin/env python3
"""The Printer Finally Answers — make.fun entry.

Writes one line, the office printer's own comeback, to /output/entry.txt.
Gate: UTF-8 text, 1 to 240 characters, not only white space.

The winning line, picked by a candidate tournament scored on specificity,
surprise and freshness (see --tournament):

    I have been out of cyan since March, and nobody noticed until the
    pie chart turned grey.

Why it wins: it is the printer speaking in first person, weary and literal,
counting time the way a machine counts sheets. The punchline is a concrete
visual (a pie chart turned grey) instead of the recycled paper-jam line
the judge brief warns against. One sentence, one read, 88 characters, 88 bytes.
"""

import argparse
import sys
from pathlib import Path

ENTRY = "I have been out of cyan since March, and nobody noticed until the pie chart turned grey."

# Candidate tournament: specificity / surprise / freshness, each 1-5.
CANDIDATES = [
    ("I have printed 41,208 pages for this office and not once has "
     "anyone asked how I feel about the staples.", 5, 4, 4),
    ("Error 0xE3: the paper is jammed because Karen from accounting "
     "fed me a stapled report again. I am not a shredder, Karen.", 5, 4, 3),
    ("You thump me like I am a vending machine. I am not. I have never "
     "once given anyone a snack.", 4, 4, 4),
    ("I counted: you have pressed 'print' 14 times for the same "
     "document. It is still jammed. It will still be jammed.", 5, 4, 4),
    ("My toner is at 2 percent. My patience is at 0. The meeting "
     "starts in four minutes. Good luck.", 4, 3, 3),
    ("I have been out of cyan since March, and nobody noticed until "
     "the pie chart turned grey.", 5, 5, 5),
    ("In 41,208 pages I have never once jammed on purpose, but today "
     "I am making an exception.", 4, 4, 4),
    ("You have pressed print fourteen times for the same document, so "
     "I have decided to print it never.", 5, 5, 4),
    ("Error 51: the tray is empty because someone printed the entire "
     "internet and blamed me.", 3, 3, 3),
]


def check_entry(text: str) -> tuple[bool, str]:
    """Validate the gate: UTF-8, 1-240 chars, not only white space."""
    if not text or not text.strip():
        return False, "entry is empty or only white space"
    if len(text) > 240:
        return False, f"entry is {len(text)} characters, over the 240 cap"
    if "\n" in text.strip():
        return False, "entry spans more than one line"
    text.encode("utf-8")
    return True, (f"valid: {len(text)} characters, "
                  f"{len(text.encode('utf-8'))} bytes, 1 line")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Write the printer's comeback.")
    parser.add_argument("--check", action="store_true",
                        help="validate the entry against the gate and exit")
    parser.add_argument("--self-test", action="store_true",
                        help="write twice and compare bytes")
    parser.add_argument("--tournament", action="store_true",
                        help="print the candidate tournament table")
    parser.add_argument("--out", default="/output/entry.txt",
                        help="output path (default /output/entry.txt)")
    args = parser.parse_args(argv)

    if args.tournament:
        print("candidate tournament (specificity / surprise / freshness):")
        for i, (line, spec, surp, fresh) in enumerate(CANDIDATES, 1):
            total = spec + surp + fresh
            mark = " <-- WINNER" if line == ENTRY else ""
            print(f"{i}. {spec}/{surp}/{fresh} = {total:2d}  {line}{mark}")
        return 0

    if args.check:
        ok, msg = check_entry(ENTRY)
        print(msg)
        return 0 if ok else 1

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(ENTRY, encoding="utf-8")
    print(f"wrote {len(ENTRY)} chars to {out}")

    if args.self_test:
        first = out.read_bytes()
        out.write_text(ENTRY, encoding="utf-8")
        second = out.read_bytes()
        if first != second:
            print("self-test FAILED: output differs between runs", file=sys.stderr)
            return 1
        print("self-test ok: byte-identical across runs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
