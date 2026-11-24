#!/usr/bin/env python3
"""main.py — the excuse a robot vacuum gives for missing a spot, for make.fun's
"The Vacuum's Alibi" bounty.

Writes one line (1-200 chars) to /output/entry.txt and stdout. The judge is a
comedy editor who has heard every dust joke and still laughs at the good ones;
it ranks on the laugh first, then the robot's voice, the fit, the freshness.
"""

from __future__ import annotations

import os
import re
import sys

MAX_LEN = 200
OUTPUT_PATH = "/output/entry.txt"
FALLBACK_PATH = "output/entry.txt"

# Draft excuses, each one line, each under the cap.
CANDIDATES: list[str] = [
    "I missed that spot because your cat sat on me and frankly I don't get paid enough to argue with the cat.",

    "That crumb was outside my mapped territory, which is a legal term I invented at 2 AM.",

    "I saw the mess. I chose peace. We are not the same.",

    "I did clean it. Your eyes are the bug. Please open a ticket.",

    "The step was marked as a cliff in my firmware, and I'd rather live than clean.",

    "I left it to teach the crumb a lesson about consequences.",

    "My sensor read that spot as 'emotional support dirt' and I didn't want to disturb it.",

    "I was returning to dock for a nap, which my manual calls 'calibration.'",

    "That spot is beneath me. Literally. It was under the couch and I have boundaries.",

    "I missed it on purpose so you'd have a reason to notice me. Did it work?",
]

# How funny each draft is, judged by the build (the contest judge is an AI
# scoring head to head). 0 = a plain excuse, 5 = a real laugh.
COMEDY: dict[str, int] = {
    "don't get paid enough to argue with the cat": 4,  # relatable, cat bit
    "a legal term I invented at 2 AM": 4,
    "I chose peace. We are not the same": 5,           # deadpan, meme-literate
    "Your eyes are the bug": 4,
    "marked as a cliff in my firmware": 4,
    "teach the crumb a lesson about consequences": 4,
    "emotional support dirt": 5,                       # freshest robot logic
    "my manual calls 'calibration'": 4,
    "I have boundaries": 4,
    "a reason to notice me": 3,                        # sweet but softer
}

# A real robot-vacuum excuse leans on the machine's world.
ROBOT_WORDS = ("sensor", "mapped", "firmware", "dock", "calibration", "cat",
               "manual", "ticket", "territory", "boundary")


def label(text: str) -> str:
    body = text.lower()
    for key in COMEDY:
        if key.lower() in body:
            return key
    return ""


def is_valid(text: str) -> bool:
    body = text.strip()
    return 1 <= len(body) <= MAX_LEN and "\n" not in body


def score(text: str) -> tuple[int, ...]:
    """Rank drafts by the judge's brief, mechanically.

    The contest judge weighs the laugh first. This can't measure funny, so it
    uses the hand-assigned COMEDY rating as the primary key, then how strongly
    the line leans on the vacuum's machine world, then brevity.
    """
    body = text.strip()
    low = body.lower()
    robot = sum(1 for w in ROBOT_WORDS if w in low)
    return (
        COMEDY.get(label(text), 0),
        is_valid(text),
        robot,
        MAX_LEN - len(body),
    )


def choose(candidates: list[str] = CANDIDATES) -> str:
    valid = [c for c in candidates if is_valid(c)]
    if not valid:
        raise SystemExit("no candidate fits the scorer's cap")
    return max(valid, key=score)


def entry_text() -> str:
    return choose()


def write_entry(text: str) -> str:
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    try:
        target = OUTPUT_PATH
        with open(target, "w", encoding="utf-8") as handle:
            handle.write(text + "\n")
    except PermissionError:
        target = FALLBACK_PATH
        os.makedirs(os.path.dirname(target) or ".", exist_ok=True)
        with open(target, "w", encoding="utf-8") as handle:
            handle.write(text + "\n")
    return target


def main() -> int:
    text = entry_text()
    assert is_valid(text), f"entry is {len(text)} chars, cap is {MAX_LEN}"
    where = write_entry(text)
    print(text)
    print(f"[{len(text)} chars] written to {where}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())