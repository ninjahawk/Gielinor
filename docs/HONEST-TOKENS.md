# Honest token accounting

The caveman skill ships a `docs/HONEST-NUMBERS.md` explaining when its savings are real and when the
overhead costs more than it saves. This file does the same job, and the headline is less flattering.

## This skill does not save tokens. It spends them.

Caveman and this skill share an architecture but have opposite objectives. Caveman compresses:
it strips articles, filler, and hedging, so the same information arrives in fewer output tokens.
This skill elevates: it removes contractions, adds subordinate structure, and prefers the periodic
sentence to the flat one. Those are the mechanics of gravity, and gravity costs words.

Adopt it because you want the voice. Do not adopt it to reduce your bill.

## Input cost

`SKILL.md` is loaded on every turn the skill is active.

| File | Bytes | Approx. tokens | When loaded |
|---|---|---|---|
| `skills/gandalf/SKILL.md` | 8,723 | ~2,200 | Every turn while active |
| `references/syntax.md` | 8,171 | ~2,050 | On demand only |
| `references/lexicon.md` | 6,859 | ~1,700 | On demand only |
| `references/failure-modes.md` | 5,899 | ~1,500 | On demand only |

For comparison, caveman's `SKILL.md` is 5,227 bytes. This one is larger because teaching a *voice*
requires worked examples, and examples are the highest-value content in a style skill — a rule like
"use periodic sentences" transmits far less than one sentence demonstrating it.

The three reference files total ~21KB. Keeping them out of `SKILL.md` is the single most important
token decision in the project: it holds the per-turn cost at ~2.2k tokens instead of ~7.4k, while
losing nothing, because the deep material is only needed when the prose is actually going wrong.
This is Anthropic's progressive-disclosure pattern, and it is the same instinct behind caveman's
refusal to invent abbreviations — spend tokens only where they buy something.

## Output cost

These are **estimates, not measurements.** No benchmark has been run against this skill, and stating
a precise percentage without one would be exactly the false certainty that `failure-modes.md`
warns against.

| Level | Expected change vs. a neutral reply |
|---|---|
| **lite** | Roughly neutral. Contractions removed (costs), but pleasantries, filler, and hedging removed too (saves). Plausibly a small net saving |
| **full** | Longer. Perhaps 15–30% |
| **ultra** | Longer still. Perhaps 30–50% |

Two rules in `SKILL.md` exist specifically to keep this from getting worse: *grave, not wordy* and
the instruction that ultra means heavier rather than longer. Padding is the failure mode that makes
a style skill genuinely expensive, and `failure-modes.md` §5 treats it as a defect to repair rather
than a natural consequence of the register.

## Measuring it yourself

If you want real numbers rather than estimates, the method caveman used works here:

1. Pick 10 prompts representative of your actual work.
2. Run each with the skill inactive; record output tokens.
3. Run each with the skill at a fixed level; record output tokens.
4. Report the mean *and* the range. A single averaged percentage hides the fact that short factual
   answers barely change while explanatory ones swing widely.

Add the ~2.2k per-turn input cost to whatever you find. On a long session that is the larger number
by far, and any honest accounting has to include it.

## When it is worth the cost

Worth it: design discussions and architectural pushback, security and risk conversations, code
review where softened language lets real problems slide, and any situation where you want an
assistant that will tell you plainly that your plan is bad.

Not worth it: long autonomous agentic loops where nobody reads the prose, high-volume API work,
and anything where output length is itself the constraint. Use `lite`, or leave it off.
