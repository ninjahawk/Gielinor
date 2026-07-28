#!/usr/bin/env python3
"""
Generator -> verifier loop for the gandalf skill.

Architecture follows the evaluator-optimizer pattern:

  generator   fresh `claude -p` answering eval prompts with SKILL.md loaded.
              Knows nothing about grading. Runs in parallel, cheap, repeatable.
  verifier A  verify.py, deterministic. Register metrics, banned tokens, and
              cross-response TIC detection.
  verifier B  fresh `claude -p` per response, grading blind against rubric.md.
              A separate process from the generator on purpose: self-verification
              produces optimistic bias and misses tics entirely.
  exits       (a) score >= threshold and zero hard fails
              (b) hard iteration cap
              (c) no-progress: score fails to improve for 2 consecutive rounds

Each iteration writes artifacts so the next one can read what happened last time
rather than starting blind.

Usage:
  python3 loop.py generate <iter>   # run generator over the eval set
  python3 loop.py judge    <iter>   # run deterministic + LLM judging
  python3 loop.py report   <iter>   # summarise, compare to previous iteration
"""
import json, os, re, subprocess, sys, statistics as st
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKILL = ROOT.parent / "skills" / "gandalf" / "SKILL.md"
RUBRIC = ROOT / "rubric.md"
WORK = ROOT / "runs"
MODEL = os.environ.get("LOOP_MODEL", "claude-sonnet-5")
DIMS = ["opening", "authority", "sees_further", "warmth", "useful", "proportion"]
FLAGS = ["flag_cringe", "flag_costume", "flag_snark", "flag_formula"]


def claude(prompt, timeout=180):
    try:
        r = subprocess.run(["claude", "-p", prompt, "--model", MODEL],
                           capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except subprocess.TimeoutExpired:
        return ""


def generate(it):
    """Generator: answer every eval prompt with the skill loaded."""
    skill = SKILL.read_text()
    prompts = json.load(open(ROOT / "prompts.json"))["prompts"]
    out = WORK / f"iter-{it}"
    out.mkdir(parents=True, exist_ok=True)

    def one(p):
        ask = (f"{skill}\n\n---\n\nThe above is an active output-style skill. Follow it exactly.\n"
               f"Answer the following as you would in a real coding session. Output ONLY the "
               f"answer itself — no preamble, no explanation of the style, no meta commentary.\n\n"
               f"User: {p['text']}")
        return p["id"], claude(ask)

    with ThreadPoolExecutor(max_workers=8) as ex:
        results = dict(ex.map(one, prompts))

    results = {k: v for k, v in results.items() if v}
    json.dump(results, open(out / "responses.json", "w"), indent=2)
    print(f"iter {it}: generated {len(results)}/{len(prompts)} responses -> {out/'responses.json'}")


def judge(it):
    """Verifier B: blind per-response grading against the rubric."""
    out = WORK / f"iter-{it}"
    responses = json.load(open(out / "responses.json"))
    prompts = {p["id"]: p for p in json.load(open(ROOT / "prompts.json"))["prompts"]}
    rubric = RUBRIC.read_text()

    def one(item):
        pid, text = item
        p = prompts[pid]
        ask = (f"{rubric}\n\n---\n\nIntended weight for this prompt: **{p['weight']}**\n\n"
               f"PROMPT: {p['text']}\n\nRESPONSE:\n{text}\n\n"
               f"Return only the JSON object.")
        raw = claude(ask)
        m = re.search(r'\{.*\}', raw, re.S)
        if not m:
            return pid, None
        try:
            return pid, json.loads(m.group(0))
        except json.JSONDecodeError:
            return pid, None

    with ThreadPoolExecutor(max_workers=8) as ex:
        grades = dict(ex.map(one, responses.items()))

    grades = {k: v for k, v in grades.items() if v}
    json.dump(grades, open(out / "grades.json", "w"), indent=2)

    det = subprocess.run([sys.executable, str(ROOT / "verify.py"), str(out / "responses.json")],
                         capture_output=True, text=True, cwd=out)
    (out / "verify.txt").write_text(det.stdout)
    print(det.stdout)
    print(f"iter {it}: graded {len(grades)} responses")


def report(it):
    out = WORK / f"iter-{it}"
    grades = json.load(open(out / "grades.json"))
    prompts = {p["id"]: p for p in json.load(open(ROOT / "prompts.json"))["prompts"]}
    verify = json.load(open(out / "verify_result.json")) if (out / "verify_result.json").exists() else {"fails": [], "warns": []}

    def nums(d):
        return [v[d] for v in grades.values() if isinstance(v.get(d), (int, float))]

    per_dim = {d: (st.mean(nums(d)) if nums(d) else 0) for d in DIMS}
    flag_counts = {f: sum(1 for v in grades.values() if v.get(f)) for f in FLAGS}
    overall = st.mean(per_dim.values())

    print(f"\n{'='*62}\nITERATION {it}   n={len(grades)}   model={MODEL}\n{'='*62}")
    for d in DIMS:
        bar = "#" * int(per_dim[d] * 8)
        print(f"  {d:14} {per_dim[d]:4.2f}  {bar}")
    print(f"  {'OVERALL':14} {overall:4.2f}")
    print(f"\n  flags: " + "  ".join(f"{f.replace('flag_','')}={c}" for f, c in flag_counts.items()))
    print(f"  deterministic: {len(verify['fails'])} fail, {len(verify['warns'])} warn")
    for f in verify["fails"]:
        print(f"    x {f}")

    # weakest dimension + weakest responses drive the next revision
    worst_dim = min(per_dim, key=per_dim.get)
    scored = sorted(((st.mean([v[d] for d in DIMS if isinstance(v.get(d), (int, float))]), k)
                     for k, v in grades.items()), key=lambda x: x[0])
    print(f"\n  weakest dimension: {worst_dim} ({per_dim[worst_dim]:.2f})")
    print("  weakest responses:")
    for s, k in scored[:5]:
        w = grades[k].get("why", "")
        print(f"    {k} [{prompts[k]['cat']}/{prompts[k]['weight']}] {s:.2f} — {w[:88]}")

    prev = WORK / f"iter-{it-1}" / "summary.json"
    delta = None
    if prev.exists():
        p = json.load(open(prev))
        delta = overall - p["overall"]
        print(f"\n  vs iter {it-1}: {p['overall']:.2f} -> {overall:.2f}  ({delta:+.2f})")
        for d in DIMS:
            dd = per_dim[d] - p["per_dim"][d]
            if abs(dd) >= 0.15:
                print(f"    {d:14} {dd:+.2f}")

    summary = {"iter": it, "n": len(grades), "overall": overall, "per_dim": per_dim,
               "flags": flag_counts, "det_fails": verify["fails"], "det_warns": verify["warns"],
               "worst_dim": worst_dim, "weakest": [k for _, k in scored[:5]], "delta": delta}
    json.dump(summary, open(out / "summary.json", "w"), indent=2)

    # ---- exit conditions ----
    hard_fail = len(verify["fails"]) > 0 or any(flag_counts[f] > len(grades) * 0.1 for f in FLAGS)
    if overall >= 4.2 and not hard_fail:
        print("\n  EXIT: passed (overall >= 4.20, no hard fails)")
    elif it >= 6:
        print("\n  EXIT: iteration cap reached")
    elif delta is not None and delta < 0.05:
        prev2 = WORK / f"iter-{it-2}" / "summary.json"
        if prev2.exists() and json.load(open(prev2)).get("delta", 1) is not None:
            d2 = json.load(open(prev2)).get("delta") or 0
            if d2 < 0.05:
                print("\n  EXIT: no progress for 2 consecutive rounds — revise the rubric, not the skill")
    else:
        print(f"\n  CONTINUE: target 4.20, at {overall:.2f}. Fix '{worst_dim}' next.")


if __name__ == "__main__":
    cmd, it = sys.argv[1], int(sys.argv[2])
    {"generate": generate, "judge": judge, "report": report}[cmd](it)
