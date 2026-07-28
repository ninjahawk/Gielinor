# Method: how this skill was built

Written down so the reasoning can be checked, argued with, and reused.

## 1. Study the reference implementation

The brief was to build a persona skill the way the [caveman skill](https://github.com/JuliusBrussee/caveman)
was built, rather than to write a one-line style prompt. So the first step was reading caveman's
actual `SKILL.md` and repository layout instead of guessing at them.

Ten structural elements were worth carrying over:

| Caveman element | Why it works | How it appears here |
|---|---|---|
| Frontmatter `description` listing literal trigger phrases | Triggering is driven by the description; vague ones under-fire | Lists "gandalf mode", "talk like gandalf", "wizard voice", `/gandalf` |
| Core directive written *in* the target style | Demonstrates before it explains | "Speak as one who has seen much, hurries little…" |
| Explicit persistence + off-switch | Styles decay back to default over long sessions | "Persistence" section; "stop gandalf" / "normal mode" |
| Drop-list and keep-list | Concrete beats abstract | "Rules" section |
| A named trap that looks right but is wrong | Caveman bans invented abbreviations (`cfg`, `impl`) — they save nothing under the tokenizer and cost clarity | "The wall": no lore, no Early Modern English |
| A sentence-shape formula | Gives a default to fall back on | `[verdict]. [why, gravely]. [what is to be done].` |
| Not/Yes contrast pair | Shows the boundary faster than description | Included |
| Intensity ladder | One style rarely fits every context | lite / full / ultra, with themed aliases |
| Same input worked at every level | The only way to convey a gradient | React re-render example at all three |
| Auto-clarity exceptions | A style that obscures a security warning is a liability | "When the voice steps aside" |
| Substance boundary | Code and errors must survive styling intact | Technical terms and code blocks verbatim |

Caveman's sharpest idea is the last one in the first column: it explicitly forbids things that *look*
like they serve the goal but do not. Abbreviating `configuration` to `cfg` feels like compression;
the tokenizer splits it the same and the reader has to decode it. Identifying that trap is what
separates a real skill from a costume.

The equivalent trap here is archaic vocabulary, and it is addressed in the same spirit.

## 2. Establish the style empirically

The brief also asked to pull dialogue from the source works. That was declined in favour of a
better approach, for two reasons.

**Copyright.** The novels and screenplays are protected. Bundling a scraped corpus of their
dialogue into a distributable repository is not something to ship.

**It would not have worked anyway.** Caveman does not ship a corpus of caveman speech; it ships
~5KB of transformation rules. A corpus in `SKILL.md` would inflate the file loaded on every single
turn — precisely the cost discipline the brief asked to preserve — and a model asked to imitate a
pile of quotations tends to produce pastiche and quotation rather than a generalisable register.

Rules generalise; corpora get recited. So the style was decomposed into mechanics instead, drawing
on published stylistic analysis:

- [Tolkien's prose style](https://en.wikipedia.org/wiki/Tolkien%27s_prose_style) — the concrete
  devices: inversion for shifts of mood, parataxis and biblical cadence, asyndeton and "loose
  semantic fit", alliteration and assonance, and register deliberately varied by people, with
  hobbits modern and colloquial while elder peoples speak archaically.
- [Language and Character in Tolkien's works](https://link.springer.com/chapter/10.1007/978-3-030-69299-5_9)
  (Sims, in *Tolkien and Diversity*) — the character in question has the widest register range of
  the Fellowship, shifting from relaxed conversation to exalted narration, deploying both warm
  humour and irony, and narrating, explaining, and arguing effectively.
- Scholarship on Tolkien's technical command of archaism — he could switch it on and off at will,
  which is why the register is a deliberate instrument rather than a constant setting.
- Character description from the wider literature: merry and kindly to the young and simple, yet
  quick to sharp speech and the rebuking of folly. That pairing became the "rebuke, then counsel"
  rule — and its violation became failure mode §6, scolding.

The single most useful finding: the gravity is **syntactic, not lexical**. The vocabulary is short,
plain, and current; what elevates it is arrangement. Nearly every failed imitation inverts this and
reaches for `thee` and `verily`, producing Early Modern English — Shakespeare's register, centuries
adrift from the target. That finding is the backbone of `references/syntax.md` and the reason the
banned list in `references/lexicon.md` is as blunt as it is.

Every example sentence in this repository is original prose composed to demonstrate a device. None
is quoted or adapted from the books or films — which is also what makes them safe to ship.

## 3. Add the constraint the brief actually cared about

The requirement was a voice, not a franchise: no lore, no Shire, no hobbits. This turned out to be
the load-bearing design constraint rather than a footnote, so it was given its own section at the
top of `SKILL.md` ("The wall") and reinforced in two references.

It is also the constraint most likely to fail under pressure, because thematically adjacent
questions — journeys, doors, fire, small brave things — invite pattern completion toward famous
lines. `SKILL.md` names those triggers explicitly so the pull is recognised as a trap rather than an
invitation.

## 4. Structure for progressive disclosure

`SKILL.md` holds what is needed on every turn (~2.2k tokens). The deep material — sentence
mechanics, full lexicon, failure catalogue — sits in `references/` and loads only when the prose is
actually going wrong, with `SKILL.md` naming the symptom that should send you to each file.

This keeps the per-turn cost at roughly 2.2k tokens rather than 7.4k, and it is the same instinct as
caveman's refusal to spend tokens on abbreviations that buy nothing.

## 5. Report the costs honestly

Caveman's repository includes a document explaining when its savings evaporate. The equivalent here
is `docs/HONEST-TOKENS.md`, and it opens by stating that this skill costs tokens rather than saving
them, because an elevated register is inherently longer than a neutral one.

The output-overhead figures in that file are labelled as estimates, since no benchmark has been run.
Publishing a precise percentage without measuring it would be the exact false certainty that
`references/failure-modes.md` §8 identifies as the one failure this voice cannot survive.
