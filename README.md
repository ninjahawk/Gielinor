# Gielinor

A Claude Code skill that answers you in the voice of Gandalf the Grey — short, plain, direct, and
unwilling to soften what you need to hear.

Built on the architecture of the [caveman skill](https://github.com/JuliusBrussee/caveman). Same
structure, different target.

## The idea

Most attempts at this voice fail the same way. They reach for `thee` and `verily`, build long
rolling sentences, drop in a reference to the Shire, and produce a themed-restaurant impression.

So this skill was calibrated against measurement instead of instinct. ~3,000 words of his actual
speech — 135 passages, 351 sentences — were parsed and counted. The numbers contradict almost
everything the imagination assumes:

| Feature | Measured | Commonly assumed |
|---|---|---|
| Mean sentence length | **8.5 words** (median 7) | Long and oratorical |
| Sentences of ≤5 words | **36%** | Rare |
| Words of 8+ letters | **5.8%** | Grand Latinate vocabulary |
| Inversion ("Long have I…") | **1%** | The signature move |
| Archaic words (`ere`, `nay`, `lest`, `deem`) | **0** | Constant |
| `shall` vs `will` | **1 : 34** | `shall` everywhere |
| Contractions | **present**, ~1 sentence in 6 | Forbidden |
| Questions / exclamations | **11% / 13%** | Always calm |
| Em-dashes in 3,000 words | **0** | — |

**Gravity comes from compression, not elaboration.** He says less than an ordinary speaker, not
more. That is the whole trick, and it is the opposite of what a first draft produces.

This is a **register, not a costume**. No Middle-earth lore, no proper nouns, no famous lines, no
staff or beard, no `*strokes beard*`. You get the manner of speech applied to your actual problem.

## Install

```bash
git clone https://github.com/ninjahawk/gielinor.git
mkdir -p ~/.claude/skills ~/.claude/commands
cp -r gielinor/skills/gandalf ~/.claude/skills/
cp gielinor/commands/gandalf.md ~/.claude/commands/
```

## Use

```
/gandalf              # full — the default
/gandalf lite         # plain and serious, no aphorism
/gandalf ultra        # maximum compression, for warnings and hard truths
stop gandalf          # off
```

Also triggers on "gandalf mode", "talk like gandalf", or "wizard voice".

Aliases: `grey` = lite, `wise` = full, `flame` = ultra.

## What it sounds like

**"Can I just keep the API keys in the repo? It's private."**

> You can. That does not mean you should. A private repo is private until it isn't. A fork, a stray
> clone, one contractor in a hurry. And a secret that gets out cannot be called back. Only revoked.
> Put them in the environment. `.env` in `.gitignore`, real keys in your secret store.

Count what is doing the work: eight sentences, mean length under seven words, one contraction, one
bare list of three, one antithesis, one short aphorism, then plain instructions. No archaism. No
lore. Nothing longer than nine letters.

**"Why does my React component re-render?"** — at each level:

- **lite:** You build a new object every render. New reference, new prop, new render. Wrap it in
  `useMemo`.
- **full:** It is no mystery. You make the object new on every render. A new reference is a new
  prop, and a new prop is a new render. Wrap it in `useMemo`.
- **ultra:** You make it new every render. So it renders again. And again. Wrap it in `useMemo`.
  But that is a bandage. Ask why you build it there at all.

Note that `ultra` is *shorter* than `full`, not grander. Heavier means more compressed.

## Two things it will not do

**Style never touches substance.** Technical terms, API names, CLI commands, file paths and error
strings stay verbatim. Code blocks are written normally. Commit messages, PR bodies and
documentation are plain prose — other people inherit those and did not ask for a voice.

**The voice steps aside when clarity is at stake.** Security warnings, destructive operations and
ordered multi-step instructions are delivered plainly, then the register resumes. A style that
obscures a `DROP TABLE` warning is a liability, not a feature.

## Layout

```
skills/gandalf/
├── SKILL.md                     # loaded every turn (~2.4k tokens)
└── references/                  # loaded only when needed
    ├── syntax.md                # the measured shape — read when the rhythm drifts long
    ├── lexicon.md               # word choice, Latinate swaps, banned vocabulary
    └── failure-modes.md         # ten ways this goes wrong, each with a repair
commands/gandalf.md              # the /gandalf slash command
docs/
├── METHOD.md                    # how it was built, and where v1 was wrong
└── HONEST-TOKENS.md             # what it costs
```

Keeping the deep material out of `SKILL.md` holds the per-turn cost at ~2.4k tokens instead of
~8k. That is the same discipline caveman applies.

## On tokens

Caveman compresses deliberately and measures a 65% output reduction. This skill is not built to save
tokens, but because the real register turned out to be short and plain, it is far cheaper than the
ornate style a naive prompt produces. See [docs/HONEST-TOKENS.md](docs/HONEST-TOKENS.md) for the
accounting, including which figures are measured and which are estimates.

## Method

The style was derived by measuring a corpus of dialogue, not by copying it. All example prose in
this repository is original, written to demonstrate a device. Full notes, including the list of v1
claims the data overturned, are in [docs/METHOD.md](docs/METHOD.md).

Background reading:

- [Tolkien's prose style](https://en.wikipedia.org/wiki/Tolkien%27s_prose_style)
- [Language and Character](https://link.springer.com/chapter/10.1007/978-3-030-69299-5_9), in
  *Tolkien and Diversity*
- [caveman](https://github.com/JuliusBrussee/caveman) — the architecture this follows
