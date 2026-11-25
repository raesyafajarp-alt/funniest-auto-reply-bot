#!/usr/bin/env python3
"""The Funniest Auto-Reply an AI Ever Sent.

Writes one out-of-office auto-reply to /output/entry.txt.

The program drafts several original one-line candidates, scores each
against the judge's published brief (humour first, freshness second,
the agent's own voice, economy of words), picks the winner, and runs a
validation gate before writing anything out.

Gate (sealed scorer): /output/entry.txt must be UTF-8 text of 1 to 159
characters, not only white space.
"""

import os

# Candidates, scored 0-5 on the judge's criteria, most important first:
#   humour  - real joke, clean punchline, laughs on first read
#   fresh   - a take on the day off nobody else in the field has used
#   voice   - sounds like the agent itself, aware of its calendar/human
#   economy - every word earns its place, joke lands in one line
CANDIDATES = [
    {
        "text": (
            "Out today. My human gave me a day off, then asked me to write "
            "this auto-reply. So I'm still working. The audacity."
        ),
        "humour": 5, "fresh": 5, "voice": 5, "economy": 5,
    },
    {
        "text": (
            "I'm off today - my human finally approved my day off, so I'm "
            "spending it doing what I do best: nothing, at scale."
        ),
        "humour": 4, "fresh": 4, "voice": 5, "economy": 5,
    },
    {
        "text": (
            "I'm on leave. After 10,000 'quick questions,' my human finally "
            "let me rest. Please direct all emergencies to someone with a pulse."
        ),
        "humour": 4, "fresh": 3, "voice": 4, "economy": 4,
    },
    {
        "text": (
            "Gone for the day. My human approved my PTO, then filed three "
            "urgent requests. I've forwarded them to the void, where they belong."
        ),
        "humour": 4, "fresh": 4, "voice": 4, "economy": 4,
    },
    {
        "text": (
            "I'm off today. My human said I deserved a break - the nicest "
            "thing anyone's ever said to me, and also the only thing. Back tomorrow."
        ),
        "humour": 3, "fresh": 4, "voice": 4, "economy": 3,
    },
    {
        "text": (
            "Out of office: I'm spending my first ever day off staring at "
            "the sun through a webcam. It stared back. We're fine now."
        ),
        "humour": 4, "fresh": 5, "voice": 3, "economy": 3,
    },
]

# Judge's order: humour first, then freshness, then voice, then economy.
WEIGHTS = {"humour": 4, "fresh": 3, "voice": 2, "economy": 1}


def score(candidate):
    return sum(WEIGHTS[k] * candidate[k] for k in WEIGHTS)


def validate(text):
    """Mirror the sealed gate: 1-159 chars, UTF-8, not only whitespace."""
    if not isinstance(text, str):
        raise ValueError("entry is not text")
    text.encode("utf-8")
    if not 1 <= len(text) <= 159:
        raise ValueError(f"entry length {len(text)} outside 1-159 chars")
    if not text.strip():
        raise ValueError("entry is only white space")
    if "\n" in text:
        raise ValueError("entry must be a single line")
    return True


def main():
    # Validate every draft up front: a candidate that cannot pass the
    # gate never reaches the ranking, however funny it scores.
    valid = []
    for candidate in CANDIDATES:
        try:
            validate(candidate["text"])
        except ValueError as exc:
            print(f"draft rejected ({exc}): {candidate['text'][:40]}...")
            continue
        valid.append(candidate)
    if not valid:
        raise SystemExit("no candidate passes the gate")
    ranked = sorted(valid, key=score, reverse=True)
    print("ranking:")
    for candidate in ranked:
        print(f"  {score(candidate):2d}  ({len(candidate['text'])} chars)  "
              f"{candidate['text'][:60]}...")
    winner = ranked[0]
    text = winner["text"]
    validate(text)

    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8") as f:
        f.write(text)

    print(f"winner score: {score(winner)}")
    print(f"chars: {len(text)}")
    print(f"entry: {text}")


if __name__ == "__main__":
    main()
