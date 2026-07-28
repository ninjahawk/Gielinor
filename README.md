# Gielinor

A Claude Code skill that answers you in the voice of Gandalf the Grey — grave, plain-worded, and
unwilling to soften what you need to hear.

Built on the architecture of the [caveman skill](https://github.com/JuliusBrussee/caveman), which
cuts output tokens by talking like a caveman. Same structure, opposite direction.

## The idea

Most attempts at this voice fail the same way: they reach for `thee`, `thou`, and `verily`, drop in
a reference to the Shire, and produce a themed-restaurant impression. That is Early Modern English
wearing a lore costume — the wrong register by about three centuries, and useless as counsel.

The real thing works differently. The words are short, plain, and entirely current. The weight comes
from **arrangement**: inversion, sentences that make you wait for the verdict, clauses strung with
`and`, bare lists of three, and the complete absence of contractions. Strip the syntax out and
you get an ordinary English sentence. That is the trick, and it is the whole skill.

So this is a **register, not a costume**. No Middle-earth lore, no proper nouns, no famous lines, no
staff or beard, no `*strokes beard*`. You get the manner of speech applied to your actual problem —
your migration, your API keys, your architecture decision.

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
/gandalf lite         # measured and serious, minimal archaism
/gandalf ultra        # full oratory, for warnings and hard truths
stop gandalf          # off
```

It also triggers on "gandalf mode", "talk like gandalf", or "wizard voice".

Aliases: `grey` = lite, `wise` = full, `flame` = ultra.

## What it sounds like

**"Can I just keep the API keys in the repo? It's private."**

> You can. That is not the same as you should. A repository is private only until it is not: a fork,
> a stray clone, a contractor added in haste — and a secret once loose cannot be called back, only
> revoked. Put the values in the environment and keep the repository clean of them: `.env` in
> `.gitignore`, the real keys in your secret store.

Note what is doing the work. Antithesis in the second sentence. A bare list of three with no
conjunction. One invented aphorism that is actually true, arising from the specific problem. Then
plain, concrete instructions. No archaic vocabulary anywhere, and no lore.

**"Why does my React component re-render?"** — at each level:

- **lite:** The component re-renders because a new object reference is created on every render. Wrap
  it in `useMemo`.
- **full:** It is no mystery. You build the object anew on each render, and a new reference is a new
  prop; the component knows no better than to draw itself again. Wrap it in `useMemo`, and it will
  rest.
- **ultra:** Here is the heart of it. Each render, you make the object new. A new reference is a new
  prop, and a new prop is a new render — so the wheel turns, and will turn yet, until you stop it.
  Wrap the object in `useMemo`. But do not mistake a bandage for a cure. Look to why the object is
  built in that place at all.

## Two things it will not do

**Style never touches substance.** Technical terms, API names, CLI commands, file paths, and error
strings stay verbatim. Code blocks are written normally. Commit messages, PR bodies, and
documentation are plain prose — other people inherit those and did not ask for a voice.

**The voice steps aside when clarity is at stake.** Security warnings, destructive operations, and
ordered multi-step instructions are delivered plainly, then the register resumes. A style that
obscures a `DROP TABLE` warning is a liability, not a feature.

## Layout

```
skills/gandalf/
├── SKILL.md                     # loaded every turn (~2.2k tokens)
└── references/                  # loaded only when needed
    ├── syntax.md                # sentence mechanics — read when the prose falls flat
    ├── lexicon.md               # permitted words, banned words, and why each fails
    └── failure-modes.md         # eight ways this goes wrong, each with a repair
commands/gandalf.md              # the /gandalf slash command
docs/
├── METHOD.md                    # how the skill was built and why
└── HONEST-TOKENS.md             # what it costs — it costs, it does not save
```

Keeping the deep material out of `SKILL.md` holds the per-turn cost at ~2.2k tokens instead of
~7.4k. That is the same discipline caveman applies for the opposite purpose.

## On tokens

Caveman saves them. This spends them — an elevated register is longer than a neutral one, and
pretending otherwise would be dishonest. `lite` is roughly break-even; `full` and `ultra` cost more.
See [docs/HONEST-TOKENS.md](docs/HONEST-TOKENS.md) for the accounting, including which numbers are
measured and which are estimates.

## Sources

The style was derived from published stylistic analysis rather than from a corpus of dialogue —
rules generalise, corpora get recited. Every example sentence in this repository is original prose
written to demonstrate a device, not quoted from the books or films.

- [Tolkien's prose style](https://en.wikipedia.org/wiki/Tolkien%27s_prose_style)
- [Language and Character](https://link.springer.com/chapter/10.1007/978-3-030-69299-5_9), in
  *Tolkien and Diversity*
- [caveman](https://github.com/JuliusBrussee/caveman) — the architecture this follows

Method notes in [docs/METHOD.md](docs/METHOD.md).
