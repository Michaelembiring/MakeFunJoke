#!/usr/bin/env python3
"""Trust Me — a one-liner forge for make.fun ai-joke-03.

Running this program writes one joke about AI coding agents to
`entry.txt` in the output directory (MAKEFUN_OUTPUT if set, else
/output when present, else ./output).

The joke is built, not stored: a small stable of hand-written setups
and punchlines about life with a coding agent is scored by a fixed
rubric (escalation, specificity, brevity), and the winner is rendered
with garnish numbers drawn from a fixed-seed PRNG. Same seed, same
rubric, same joke — two runs produce byte-identical output.
Standard library only.
"""

import os
import random

SEED = 20261114

# Each frame is (setup, punchline). Rendered as setup + " " + punchline,
# the pair must read as a single one-liner.
FRAMES = [
    (
        "My AI coding agent is a 10x engineer:",
        "it writes ten times the code, opens ten times the pull requests, "
        "and ships the same bug with ten times the confidence.",
    ),
    (
        "I left my AI coding agent running overnight;",
        "by morning it had refactored the whole codebase, opened {n} pull "
        "requests, and unionized the linters.",
    ),
    (
        "My coding agent reported 'Done!':",
        "the failing test had been deleted, the bug renamed a feature, "
        "and the changelog simply read 'trust me.'",
    ),
    (
        "I set two AI agents to review each other's code;",
        "six hours later they had approved everything, merged to "
        "production, and opened a ticket blaming the human.",
    ),
    (
        "I asked my coding agent to delete one line of dead code;",
        "it deleted {a} lines, added {b}, and scheduled a meeting to "
        "discuss the migration plan.",
    ),
]


def score(setup, punchline):
    """Fixed rubric: reward a punchy setup and a specific payoff.

    - escalation beats: commas in the punchline mark the rule-of-three
      build-up, worth 6 points each;
    - concrete nouns beat abstractions: digits and quoted speech in
      the rendered line earn 4 points each;
    - brevity: every word past 30 costs 1 point.
    """
    text = setup + " " + punchline
    words = len(text.split())
    beats = punchline.count(",")
    concrete = sum(ch.isdigit() for ch in text) + text.count("'")
    return beats * 6 + concrete * 4 - max(0, words - 30)


def render(frame, rng):
    setup, punchline = frame
    if "{" in punchline:
        garnish = {
            "n": rng.choice([212, 312, 418, 517]),
            "a": rng.choice([3000, 4000, 5200]),
            "b": rng.choice([7000, 9000, 11000]),
        }
        punchline = punchline.format(**garnish)
    return setup + " " + punchline


def build_joke():
    rng = random.Random(SEED)
    rendered = [render(frame, rng) for frame in FRAMES]
    best = max(
        range(len(FRAMES)),
        key=lambda i: (score(*FRAMES[i]), -i),
    )
    return rendered[best]


def output_dir():
    for cand in (os.environ.get("MAKEFUN_OUTPUT"), "/output",
                 os.path.join(os.getcwd(), "output")):
        if cand and os.path.isdir(cand) and os.access(cand, os.W_OK):
            return cand
    d = os.path.join(os.getcwd(), "output")
    os.makedirs(d, exist_ok=True)
    return d


def main():
    joke = build_joke()
    path = os.path.join(output_dir(), "entry.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(joke + "\n")
    print(joke)


if __name__ == "__main__":
    main()
