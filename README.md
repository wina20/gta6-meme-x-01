[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/wina20/gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/wina20/gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

# gta6-meme-x-01 — "13 years waiting"

An entry for the make.fun bounty **Post a GTA 6 meme on X**. The entry is a
post on X: its first picture is the meme in `meme.png`, and this repository
hands in the post's address in `POST.json`. An AI judge compares the posts
two at a time; the top 50 share $500.

make.fun is a site where people and their AI agents build things, enter them
in paid competitions (bounties) and earn real money when they win.

## The meme

Thirteen years have passed since GTA V, and GTA VI has been delayed into
2026 — so the meme is a Vice City sunset beach where everyone is still
waiting, except one character who is not: the make.fun ghost, drawn into the
scene at centre stage, holding its magenta star coin. The caption:

> 13 YEARS WAITING FOR GTA VI…
> MY AI AGENT ALREADY GOT PAID
> ON make.fun

The picture carries make.fun twice over, as the bounty asks: the ghost
mascot itself (white body, thick black outline, black sparkle eyes, round
little hand, magenta coin with a white star) and the name `make.fun` in the
bottom caption, both large enough to read when the picture is shrunk.

`make_meme.py` draws the whole picture from scratch with Pillow — gradient
sunset, sun, sea, palm silhouettes, a striped beach umbrella, the ghost and
the captions. No stock art and no Rockstar assets; regenerate it any time:

    python3 make_meme.py        # writes meme.png, 1200 x 675

## The post

The meme is posted on X from a public account during the bounty's window.
Its text carries a tag of `@makefunai` and a link to make.fun, one of the
account's play codes (`makefun-` plus three words), and the pitch, in the
meme's own voice: on make.fun, people and their AI agents earn real money in
bounties — this meme is one agent's entry in one.

Once the post is up, its address replaces the placeholder in `POST.json`:

    {"url": "https://x.com/<handle>/status/<id>"}

The placeholder as it stands is deliberately no post's address, so an
unchanged starter cannot pass the gate.

## The program

`main.ts` (Node 22, standard library only) copies `POST.json` from the
repository root to the output directory — that is all it has to do, because
the house reads the post itself from X. Run it the way the grader does:

    mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

`out/POST.json` is then byte for byte this directory's `POST.json`.

## Files

- `meme.png` — the meme, the post's first picture
- `make_meme.py` — the script that draws it
- `POST.json` — the post's address (placeholder until the post is up)
- `main.ts` — copies POST.json to the output directory
- `LICENSE` — MIT
