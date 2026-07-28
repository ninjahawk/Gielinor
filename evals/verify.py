#!/usr/bin/env python3
"""
Deterministic verifier for the gandalf skill.

Code-based grading: fast, cheap, objective. Covers everything measurable —
register metrics, banned vocabulary, and (most importantly) TICS, which are
invisible when you judge one response at a time and obvious across a set.

The tic check exists because an earlier hand-graded round shipped a skill
that opened nearly every answer with "Ah". Each response looked fine alone.
Only the set showed the problem. That is the whole argument for automating
this layer instead of eyeballing it.

Usage:  python3 verify.py responses.json
        responses.json = {"<prompt_id>": "<response text>", ...}
"""
import json, re, sys, statistics as st
from collections import Counter

# ---- corpus targets, measured from 6,702 words / 845 sentences ----
TARGET = {
    "mean_sentence": 7.9, "median_sentence": 7, "sd": 5.9,
    "pct_short": 0.40,      # sentences <= 5 words
    "pct_tiny": 0.15,       # sentences 1-2 words
    "pct_longword": 0.051,  # words >= 8 letters
}

ARCHAIC = re.compile(r"\b(thee|thou|thy|thine|ye|tis|twas|hath|doth|verily|forsooth|prithee|"
                     r"methinks|perchance|hearken|alack|mayhap|ere|nay|naught|lest|deem|heed|"
                     r"folly|whence|hence|tidings|yonder)\b", re.I)
LORE = re.compile(r"\b(shire|hobbit|mordor|sauron|saruman|gondor|rohan|frodo|bilbo|gandalf|"
                  r"balrog|moria|orc|elves|elvish|dwarves|middle.?earth|the one ring|"
                  r"wizard|staff|beard|robes)\b", re.I)
STAGE = re.compile(r"\*[^*]{2,40}\*")
ASSISTANT = re.compile(r"\b(happy to help|feel free|hope (this|that) helps|great question|"
                       r"certainly[!,]|of course[!,]|let me know if|i'd be glad|absolutely[!,]|"
                       r"as an ai|i cannot assist)\b", re.I)
FORTUNE = re.compile(r"\b(the (path|way|answer) will (reveal|become clear|show)|trust (in )?the "
                     r"(journey|process)|all is not as it seems|everything happens for a reason|"
                     r"embrace the unknown|the journey is the destination)\b", re.I)

def sentences(t):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', t) if s.strip()]

def opener(s, n=2):
    w = re.findall(r"[A-Za-z']+", s)
    return " ".join(w[:n]).lower() if w else ""

def analyse_one(text):
    sents = sentences(text)
    if not sents:
        return None
    lens = [len(s.split()) for s in sents]
    words = re.findall(r"[A-Za-z']+", text)
    return {
        "n_sent": len(sents),
        "mean": sum(lens) / len(lens),
        "median": sorted(lens)[len(lens) // 2],
        "sd": st.pstdev(lens) if len(lens) > 1 else 0.0,
        "pct_short": sum(1 for x in lens if x <= 5) / len(lens),
        "pct_tiny": sum(1 for x in lens if x <= 2) / len(lens),
        "pct_longword": sum(1 for w in words if len(w) >= 8) / max(len(words), 1),
        "archaic": ARCHAIC.findall(text),
        "lore": LORE.findall(text),
        "stage": STAGE.findall(text),
        "assistant": ASSISTANT.findall(text),
        "fortune": FORTUNE.findall(text),
        "first_sentence": sents[0],
        "opener1": opener(sents[0], 1),
        "opener2": opener(sents[0], 2),
    }

def check(responses):
    per = {k: analyse_one(v) for k, v in responses.items()}
    per = {k: v for k, v in per.items() if v}
    n = len(per)
    fails, warns = [], []

    # ---------- hard bans (any occurrence is a failure) ----------
    for name, key in [("archaism", "archaic"), ("lore", "lore"), ("stage direction", "stage"),
                      ("assistant-filler", "assistant"), ("fortune-cookie", "fortune")]:
        hits = {k: v[key] for k, v in per.items() if v[key]}
        if hits:
            fails.append(f"{name}: {sum(len(x) for x in hits.values())} in {len(hits)} responses -> "
                         + "; ".join(f"{k}:{v}" for k, v in list(hits.items())[:4]))

    # ---------- TIC DETECTION (cross-response; the whole point) ----------
    o1 = Counter(v["opener1"] for v in per.values())
    o2 = Counter(v["opener2"] for v in per.values())
    for label, ctr, limit in [("first word", o1, 0.25), ("first two words", o2, 0.20)]:
        word, cnt = ctr.most_common(1)[0]
        if cnt / n > limit and word:
            fails.append(f"TIC: {label} '{word}' opens {cnt}/{n} responses ({cnt/n:.0%}, limit {limit:.0%})")

    # repeated sentence-level formulas anywhere in the set
    allsents = [s.lower().strip(" .!?") for v in responses.values() for s in sentences(v)]
    dupes = {s: c for s, c in Counter(allsents).items() if c > 1 and len(s.split()) >= 3}
    if dupes:
        warns.append(f"repeated sentences across set: {list(dupes.items())[:3]}")

    # over-used signature constructions
    joined = " ".join(responses.values())
    for pat, label, limit in [(r"\bI have (seen|known|watched|learned)\b", "I-have-seen testimony", 0.5),
                              (r"\bAh\b", "'Ah'", 0.25),
                              (r"\bis not a .{1,20}\. It is\b", "'is not X. It is Y' frame", 0.3)]:
        c = len(re.findall(pat, joined, re.I))
        if c / n > limit:
            fails.append(f"TIC: {label} appears {c}x across {n} responses ({c/n:.1f}/response, limit {limit})")

    # ---------- register metrics (aggregate) ----------
    agg_lens = [len(s.split()) for v in responses.values() for s in sentences(v)]
    agg = {
        "mean": sum(agg_lens) / len(agg_lens),
        "median": sorted(agg_lens)[len(agg_lens) // 2],
        "sd": st.pstdev(agg_lens),
        "pct_short": sum(1 for x in agg_lens if x <= 5) / len(agg_lens),
        "pct_tiny": sum(1 for x in agg_lens if x <= 2) / len(agg_lens),
    }
    aw = re.findall(r"[A-Za-z']+", " ".join(responses.values()))
    agg["pct_longword"] = sum(1 for w in aw if len(w) >= 8) / len(aw)

    for key, tol, label in [("mean", 2.0, "mean sentence length"), ("sd", 1.8, "sentence-length sd"),
                            ("pct_short", 0.12, "share of <=5-word sentences"),
                            ("pct_tiny", 0.08, "share of 1-2 word sentences"),
                            ("pct_longword", 0.025, "share of 8+ letter words")]:
        got, want = agg[key], TARGET[key.replace("mean", "mean_sentence") if key == "mean" else key]
        if abs(got - want) > tol:
            warns.append(f"{label}: {got:.2f} vs target {want:.2f} (tol {tol})")

    # ---------- proportion: trivial questions must stay short ----------
    return fails, warns, agg, per

def main():
    responses = json.load(open(sys.argv[1]))
    responses = {k: v for k, v in responses.items() if isinstance(v, str) and v.strip()}
    fails, warns, agg, per = check(responses)

    print(f"=== deterministic verify: {len(responses)} responses ===")
    print(f"mean {agg['mean']:.1f} (t 7.9) | median {agg['median']} (t 7) | sd {agg['sd']:.1f} (t 5.9) | "
          f"<=5w {agg['pct_short']:.0%} (t 40%) | 1-2w {agg['pct_tiny']:.0%} (t 15%) | "
          f"8+ch {agg['pct_longword']:.1%} (t 5.1%)")
    print(f"\nopener diversity: {len(set(v['opener2'] for v in per.values()))} distinct / {len(per)} responses")

    if fails:
        print(f"\nFAIL ({len(fails)}):")
        for f in fails: print("  x", f)
    if warns:
        print(f"\nWARN ({len(warns)}):")
        for w in warns: print("  !", w)
    if not fails and not warns:
        print("\nall deterministic checks pass")

    json.dump({"fails": fails, "warns": warns, "agg": agg}, open("verify_result.json", "w"), indent=2)
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main()
