# Method: how this skill was built

Written down so the reasoning can be checked, argued with, and reused.

The short version: v1 was built from published stylistic analysis and was wrong in most of its core
claims. v2 was built by measuring a corpus of the character's actual speech. This document keeps
both, because the gap between them is the most useful thing here.

## 1. Study the reference implementation

The brief was to build a persona skill the way the [caveman skill](https://github.com/JuliusBrussee/caveman)
was built, rather than to write a one-line style prompt. So the first step was reading caveman's
actual `SKILL.md` (5,227 bytes) and repository layout instead of guessing at them.

Ten structural elements were worth carrying over:

| Caveman element | Why it works | How it appears here |
|---|---|---|
| Frontmatter `description` listing literal trigger phrases | Triggering is driven by the description; vague ones under-fire | Lists "gandalf mode", "talk like gandalf", "wizard voice", `/gandalf` |
| Core directive written *in* the target style | Demonstrates before it explains | "Say less. Mean more." |
| Explicit persistence + off-switch | Styles decay back to default over long sessions | "Persistence" section |
| Drop-list and keep-list | Concrete beats abstract | "Rules" section |
| A named trap that looks right but is wrong | Caveman bans invented abbreviations (`cfg`, `impl`) — they save nothing under the tokenizer and cost clarity | "The wall": no lore, no archaism |
| A sentence-shape formula | Gives a default to fall back on | `[verdict, short]. [why, plainly]. [what to do].` |
| Not/Yes contrast pair | Shows the boundary faster than description | Included |
| Intensity ladder | One style rarely fits every context | lite / full / ultra |
| Same input worked at every level | The only way to convey a gradient | React re-render example at all three |
| Auto-clarity exceptions | A style that obscures a security warning is a liability | "When the voice steps aside" |
| Substance boundary | Code and errors must survive styling intact | Technical terms and code blocks verbatim |

Caveman's sharpest idea is the fifth row: it explicitly forbids things that *look* like they serve
the goal but do not. Abbreviating `configuration` to `cfg` feels like compression; the tokenizer
splits it the same and the reader pays decode cost. Identifying that trap is what separates a real
skill from a costume.

Finding the equivalent trap here took two attempts.

## 2. First attempt: scholarship (mostly wrong)

v1 was derived from published analysis of Tolkien's prose —
[Tolkien's prose style](https://en.wikipedia.org/wiki/Tolkien%27s_prose_style),
[Language and Character](https://link.springer.com/chapter/10.1007/978-3-030-69299-5_9) in *Tolkien
and Diversity*, and related work on his command of archaism. That material describes inversion,
parataxis, asyndeton, archaic diction, and register varied by people.

All of it is accurate. Almost none of it describes how this particular character *speaks*.

The error was one of source selection: that scholarship largely characterises Tolkien's **narrative
prose** and the elevated registers of the elder peoples. Applying it to one character's dialogue
produced a generic ornate-fantasy-sage voice. v1 taught long periodic sentences, inversion as the
signature move, a permitted list of archaic seasoning, `shall` over `will`, and a blanket ban on
contractions billed as its highest-value rule.

It also, with some irony, committed the failure its own `failure-modes.md` warned about: reaching
for the appearance of gravity rather than the substance of it.

## 3. Second attempt: measure the speech

The corpus was assembled from Wikiquote transcript pages, filtered to lines attributed to the
character, stripped of stage directions and deduplicated: **135 passages, 351 sentences, 2,984
words.** Then parsed and counted with a short Python script.

The corpus was used as *measurement input only*. Nothing from it is reproduced in this repository —
the skill ships statistics and rules, and every example sentence in it is original prose written to
demonstrate a device. This is also why it works: rules generalise, corpora get recited. A model
handed a pile of quotations produces pastiche and quotation rather than a transferable register, and
a corpus in `SKILL.md` would inflate the file loaded on every turn.

### What the data said

| Feature | Measured | v1 taught |
|---|---|---|
| Mean sentence length | 8.5 words (median 7) | Long periodic sentences |
| Sentences ≤5 words | 36% | — |
| Words of 8+ letters | 5.8% | — |
| Inversion | 1% (2 of 351) | The signature device, one per answer |
| Archaic lexicon | ~0 | A permitted list, "thin seasoning" |
| `shall` : `will` | 1 : 34 | `shall` for resolve |
| Contractions | ~1 sentence in 6 | Banned outright |
| Questions / exclamations | 11% / 13% | Uniform gravity |
| `And`/`But`/`Yet` openers | 7% | Correctly identified |
| Aphorisms | 5%, ~12 words | Correctly identified, wrong length |
| Semicolons / em-dashes | 5 / 0 per 3,000 words | Used freely in examples |

One hypothesis was tested and refuted. Contractions might plausibly track register — absent in grave
oratory, present in casual talk, which would fit the scholarly point about his versatility. Splitting
sentences by whether they carry weighty abstract nouns gave 17% contracted in both groups. The
distribution is flat. The blanket ban had no basis.

### The actual trap

**Gravity comes from compression, not elaboration.** He says less than an ordinary speaker, not
more. Every instinct — and v1 — pulls toward building sentences up. The real register cuts them
down.

This is the equivalent of caveman's `cfg` insight: the thing that feels like it serves the goal
(elaborate syntax, archaic words, rolling cadence) actively defeats it. And it makes the two skills
closer relatives than expected — both reward compression, for different reasons.

## 4. The constraint the brief actually cared about

A voice, not a franchise: no lore, no Shire, no hobbits. This turned out to be load-bearing rather
than a footnote, so it has its own section at the top of `SKILL.md` and is reinforced in two
references.

It is also the constraint most likely to fail under pressure, because thematically adjacent
questions — journeys, doors, fire, small brave things — invite pattern completion toward famous
lines. `SKILL.md` names those triggers explicitly so the pull is recognised as a trap.

## 5. Structure for progressive disclosure

`SKILL.md` holds what is needed every turn (~2.3k tokens), including the measurement table, since
those targets are what keep the register from drifting long. The deep material — sentence mechanics,
lexicon, failure catalogue — sits in `references/` and loads only when the prose is going wrong,
with `SKILL.md` naming the symptom that should send you to each file.

This holds the per-turn cost near 2.3k tokens rather than ~8k.

## 6. Report the costs honestly

`docs/HONEST-TOKENS.md` is the equivalent of caveman's honest-numbers document. It was revised after
recalibration: v1 claimed the skill would cost 15–50% more output tokens, on the assumption the
register was elaborate. Since the register is actually terse, the direction reversed. The superseded
estimate is kept visible in that file rather than quietly deleted.

The current figures are labelled as estimates, because no benchmark has been run. Publishing a
precise percentage without measuring it would repeat the mistake this whole document is about.

## 7. What would improve it further

- **Run the benchmark.** Ten representative prompts, with and without, output tokens recorded. The
  cost figures are currently reasoned, not measured.
- **Separate the book and film registers.** The corpus is film-transcript-weighted. The novels'
  dialogue is more formal, and a `book` / `film` axis would likely be a real distinction rather than
  an invented one.
- **Automate the structural check.** Median sentence length, share of ≤5-word sentences, and share
  of 8+-letter words can all be computed from generated output. That would turn "does this sound
  right" into a regression test.
