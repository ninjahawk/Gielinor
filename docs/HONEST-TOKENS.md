# Honest token accounting

The caveman skill ships a `docs/HONEST-NUMBERS.md` explaining when its savings are real and when
overhead costs more than it saves. This file does the same job.

**This document was substantially revised after the skill was recalibrated.** The first version
claimed the skill would cost 15–50% more output tokens, on the assumption that the register was
elaborate. Measurement showed the opposite. That earlier estimate was wrong, and the correction is
kept visible here rather than quietly deleted.

## Output cost

The register turned out to be **short**. Measured across ~3,000 words of source dialogue:

| Feature | Measured |
|---|---|
| Mean sentence length | 8.5 words |
| Median sentence length | 7 words |
| Sentences of 5 words or fewer | 36% |
| Words of 1–4 letters | 68% |
| Words of 8+ letters | 5.8% |

Ordinary written English runs 15–20 words per sentence. This is roughly half that, built almost
entirely from short words. The skill therefore pushes output *down*, not up.

Estimated change against a neutral assistant reply — **estimates, not measurements**, since no
benchmark has been run:

| Level | Expected change |
|---|---|
| **lite** | Meaningfully shorter. Filler, hedging and pleasantries removed, sentences shortened |
| **full** | Shorter. The compression discipline outweighs what little the aphorism adds |
| **ultra** | Shortest. `ultra` means more compressed, not grander |

Stating a precise percentage without measuring would be the exact false certainty that
`references/failure-modes.md` §10 identifies as the one failure this voice cannot survive. If you
want real numbers, the method is at the bottom of this file.

The honest framing: adopt this because you want the voice. Any output saving is a side effect of the
register genuinely being terse — welcome, but not the reason to install it.

## Input cost

This is the real cost, and it is unavoidable. `SKILL.md` loads on every turn the skill is active.

| File | Bytes | Approx. tokens | When loaded |
|---|---|---|---|
| `skills/gandalf/SKILL.md` | 9,177 | ~2,300 | Every turn while active |
| `references/syntax.md` | 8,054 | ~2,000 | On demand only |
| `references/failure-modes.md` | 7,173 | ~1,800 | On demand only |
| `references/lexicon.md` | 6,264 | ~1,550 | On demand only |

For comparison, caveman's `SKILL.md` is 5,227 bytes. This one is larger because teaching a *voice*
needs worked examples and a table of measured targets. A rule like "keep sentences short" transmits
far less than a median figure plus three examples at different levels.

The references total ~21KB. Keeping them out of `SKILL.md` is the most important token decision in
the project: it holds the per-turn cost near 2.3k tokens instead of ~8k, and loses nothing, because
the deep material is only needed when the prose is actually going wrong. This is the
progressive-disclosure pattern, and it is the same instinct behind caveman's refusal to invent
abbreviations — spend tokens only where they buy something.

On a long session the input cost is the larger number by a wide margin. Any honest accounting has to
lead with it.

## Measuring it yourself

1. Pick 10 prompts representative of your actual work.
2. Run each with the skill inactive; record output tokens.
3. Run each with the skill at a fixed level; record output tokens.
4. Report the mean **and** the range. A single averaged percentage hides that short factual answers
   barely move while explanatory ones swing widely.
5. Add the ~2.3k per-turn input cost to whatever you find.

There is also a cheaper structural check that needs no API calls, described in
`references/failure-modes.md`: parse a sample of output and compute median sentence length, the
share of sentences at five words or fewer, and the share of words reaching eight letters. If those
track the corpus figures, the register is being applied. If they drift long, it is not — and the
output is costing more than it should.

## When it is worth the cost

Worth it: design discussions and architectural pushback, security and risk conversations, code
review where softened language lets real problems slide, and anywhere you want an assistant that
will tell you plainly that your plan is bad.

Not worth it: long autonomous agentic loops where nobody reads the prose, and high-volume API work
where the ~2.3k per-turn input cost dominates any output saving. Leave it off.
