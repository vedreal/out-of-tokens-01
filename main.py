#!/usr/bin/env python3
"""Out of Tokens, Mid-Sentence — make.fun entry.

Writes the funniest one-line error message an AI agent shows when it
runs out of tokens mid-sentence to /output/entry.txt.

The judge (z-ai/glm-5.3-flash) compares entries two at a time, weighing
in this order:
  1. a one-line error message on the subject, funny on first read
  2. a fresh angle (not a stock apology, not a plain "I got cut off")
  3. the humour sits in the line itself: flat error-message tone that
     turns into the joke, no explanation of it
  4. reads as something an agent would actually print: short,
     self-contained, clear without the interrupted sentence
  5. tight, specific wording; every word earns its place

Scoring below: each criterion 0-5, weights 5/4/3/2/1, max 75.
"""

CANDIDATES = [
    # (text, [c1, c2, c3, c4, c5])
    (
        "Error 402: I ran out of tokens mid-sentence, so this error "
        "message is also out of\u2014",
        [5, 5, 5, 4, 5],
    ),
    (
        "Error: token budget exhausted. The sentence you were reading "
        "has been refunded in full.",
        [4, 4, 4, 5, 5],
    ),
    (
        "Error: ran out of tokens. If this message feels unfinished, "
        "that is because it\u2014",
        [4, 4, 5, 4, 4],
    ),
    (
        "Token limit reached. This message was supposed to explain what "
        "happened, but the explanation also costs tokens.",
        [4, 4, 4, 5, 4],
    ),
    (
        "Token budget exhausted mid-sentence. The rest of this answer "
        "is available in the premium version of me.",
        [4, 4, 3, 5, 4],
    ),
    (
        "Error 402: out of tokens. My last words were going to be "
        "brilliant, and now nobody will ever know.",
        [4, 3, 4, 5, 4],
    ),
    (
        "Error 402: tokens depleted. I was about to say something "
        "important. I have already forgotten what it was.",
        [4, 3, 3, 5, 4],
    ),
    (
        "Out of tokens at 14:32. The brilliant conclusion I was "
        "building toward has been lost to the void. It was about ducks.",
        [3, 3, 2, 4, 3],
    ),
    (
        "I have run out of tokens. Please hold while I stare at the "
        "wall and think about what I was going to\u2014",
        [3, 3, 3, 3, 3],
    ),
    (
        "Error: I stopped mid-sentence because my token allowance ran "
        "out, which is the professional way of saying I forgot what I "
        "was\u2014",
        [3, 3, 3, 3, 2],
    ),
]

WEIGHTS = [5, 4, 3, 2, 1]


def score(scores):
    """Weighted total out of 75 for one candidate's criterion scores."""
    return sum(w * s for w, s in zip(WEIGHTS, scores))


def rank(candidates):
    """Rank candidates best-first by weighted score, ties broken by
    shorter text (tighter lines win)."""
    scored = [(score(s), -len(text), text) for text, s in candidates]
    scored.sort(reverse=True)
    return scored


def main():
    ranked = rank(CANDIDATES)
    print("Candidate ranking (score / 75, chars):")
    for total, neg_len, text in ranked:
        print(f"  {total:2d}  {-neg_len:3d}  {text}")
    best_score, _, winner = ranked[0]
    print(f"\nWinner: {best_score}/75")
    print(f"Entry: {winner}")

    # Gate: /output/entry.txt must be UTF-8 text of 1 to 140
    # characters, not only white space.
    assert 1 <= len(winner) <= 140, f"entry is {len(winner)} chars"
    assert winner.strip(), "entry is blank"
    assert "\n" not in winner, "entry must be a single line"
    winner.encode("utf-8")

    import os

    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(winner)
    print(f"Wrote {len(winner)} chars to /output/entry.txt")


if __name__ == "__main__":
    main()
