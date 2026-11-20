# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/dylangiomarcontreras1-sketch/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/dylangiomarcontreras1-sketch/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One front page for the world's news of Thursday 19 November 2026, drawn at 1024 x 1024 and
written to `/output/entry.png` by `main.py`. Lead story: the first Trump-Xi-Putin trilateral
summit in Shenzhen. Around it: the ICJ's genocide ruling against Myanmar, a tanker ablaze off
Hormuz, Anthropic's $2 trillion Nasdaq debut, GTA VI's $2.3bn launch day, 341 garment factories
shut in Bangladesh, 34 gang suspects killed in Port-au-Prince, Senegal's budget by decree,
Somalia's expulsion of the UAE envoy and COP31's final stretch in Antalya.

Facts follow the day's reporting (AP, Reuters, AFP, BBC, Al Jazeera, and Wikipedia's
current-events entry for 19 November 2026). The page is drawn from code, with no photographs.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The entry is the committed `entry.png`; `main.py` copies those bytes, so both runs of the
grader write an identical file. To redraw the page (build-time only, needs Pillow and the
Oswald, Archivo Black, PT Serif and Libre Franklin fonts):

```sh
FONTS_DIR=/path/to/fonts python3 render.py
```

## Licence

MIT. The image is original work drawn by `render.py`; it uses no photographs or third-party
artwork.

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
