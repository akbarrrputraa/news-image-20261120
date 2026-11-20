# news-image-20261120 — The World in One Page

[![make.fun](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/akbarrrputraa/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/akbarrrputraa/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

One image summing up the world's news of **Friday 20 November 2026**,
built for the [make.fun bounty](https://make.fun/bounty/news-image-20261120).

## The image

A 1024×1024 broadsheet front page — *THE WORLD in one page* — with the
day's verified news:

- **Lead:** the International Court of Justice rules 9–6 that Myanmar
  committed genocide against the Rohingya — the first time the UN court
  has ever found a state guilty of genocide.
- **Markets:** Anthropic closes up 17% at $97.17 in the biggest IPO ever
  ($81.3bn raised) as US stocks fall 2%.
- **Diplomacy:** Trump, Xi and Putin hold the first three-way summit in
  Shenzhen and issue a four-point peace declaration.
- **The Gulf:** a tanker catches fire after hitting a mine near the
  Strait of Hormuz; a Houthi missile hits Riyadh.
- **War:** Ukraine hits the Crimean Bridge a third time in four days;
  four ballistic missiles strike Kyiv.
- **Europe:** allies meeting in Berlin say they are ready for talks
  with Russia.
- **Washington:** the Senate rejects an Iran war-powers vote 51–48;
  Trump pardons Pete Rose.
- **Also today:** Genoa airport halts flights after drones are spotted,
  India evacuates 80,000 as Storm Dana nears, Fiona the hippo dies,
  COP31 draft drops fossil-fuel wording — plus a markets strip
  (S&P −2.02%, Dow −2.19%, Nasdaq −2.25%, ANT +17%, NVDA −3%).

Every figure was verified on 20 November 2026 against WSJ, Barron's,
BBC, Reuters and AP. No story was invented.

## How it runs

Pure Python standard library — no network, nothing installed.
`main.py` draws the page with `render.py` (a small raster canvas, an
embedded 5×7 bitmap font and a zlib PNG encoder) and writes
`entry.png` to `$MAKEFUN_OUTPUT_DIR` (or `/output`):

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The output is deterministic: two runs write byte-identical PNGs
(1024×1024, ~23 KB, well under the 1 MiB gate).

## Files

- `main.py` — entrypoint: the broadsheet layout and the day's news.
- `render.py` — canvas, bitmap font, PNG encoder (stdlib only).
- `entry.png` — the rendered image, for reference.
- `.makefun/owner.json` — the payout wallet for this entry.

## License

MIT — see `LICENSE`.
