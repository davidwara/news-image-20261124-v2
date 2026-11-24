[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/davidwara/news-image-20261124-v2/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/davidwara/news-image-20261124-v2/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

# THE WORLD IN ONE DAY — Tuesday 24 November 2026

A newspaper front page that sums up Tuesday 24 November 2026 in a single
1024×1024 image: **36 stories, 5 regions, every one dated**.

## What the image holds

- **3 lead stories** with custom illustrations: Jensen Huang's return as
  Nvidia CEO, the COP31 climate talks collapsing in Antalya, and NATO's vow
  to defend against threats in space.
- **12 more stories** (4–15) in a grid, each with its own pictogram.
- **21 more stories** (16–36) in the "Also on Tuesday 24 November" list.
- **"Where it happened"** world map with 15 numbered pins and a pin key.
- **Region bar** with story counts (Americas 14, Europe 8, Asia-Pacific 6,
  Middle East 5, Africa 3).
- **"The day in UTC"** timeline of the day's key moments.
- **KPI strip**: Nvidia +31%, +$900bn market cap added in a day, 25 Russian
  airspace violations in 2026, 90+ nations rejecting the COP31 draft, the
  $43.9bn CrowdStrike–Zscaler deal, and 7.3 million people's aid at risk.
- **Date check** box explaining what was left out and why, plus a
  certainty legend (reported / claim / forecast).

## How to run

```sh
python3 main.py
```

`main.py` is pure Python standard library: it reads the pre-rendered
`entry.png` from its own directory, validates it (PNG magic, IEND trailer,
≤ 1 MiB, IHDR 1024×1024, bit depth 8, colour type 2 RGB) and copies it to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`). It writes nothing
into the repository directory and needs no network and no third-party
packages.

`render.py` is the build-time renderer (Pillow) that drew `entry.png`. It
is not run at grade time.

## Sources

Reuters, Le Monde, AP, BBC, Al Jazeera, The Guardian, WSJ, FT, Middle East
Eye, Grist, The Conversation. Stories first reported 22–24 Nov 2026; every
story is dated to Tuesday 24 November 2026, with Monday's announcements
(Huang's reinstatement, the CrowdStrike–Zscaler deal) included only for
their Tuesday developments, as explained in the Date Check box.
