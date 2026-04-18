**English** · [Русский](README.ru.md)

# kalve

> **Carousels-as-code — no Canva, no Figma, just JSON.**

Generate brand-consistent Instagram and Threads carousels from a JSON spec. Python, offline, MIT-licensed. Composable with any AI assistant (Claude, ChatGPT, Cursor). Think of it as a self-hosted, `pip install`-able Bannerbear — but for devs who'd rather edit a config file than click through a dashboard.

Built for [Šaunuolė](https://saunuolė.lt) (a Lithuanian language tutor) but designed as a universal tool: plug in your own brand kit, get cards in your own style.

---

## See it in action

Same JSON spec, three different brand kits — that's the point:

**`default_dark`** — developer-native dark theme:
<p align="center">
  <img src="https://raw.githubusercontent.com/anna-ladutko/kalve/main/examples/sample_output/demo_dark/01_tier1.png" width="22%" alt="Dark tier 1" />
  <img src="https://raw.githubusercontent.com/anna-ladutko/kalve/main/examples/sample_output/demo_dark/02_tier2.png" width="22%" alt="Dark tier 2" />
  <img src="https://raw.githubusercontent.com/anna-ladutko/kalve/main/examples/sample_output/demo_dark/03_tier3.png" width="22%" alt="Dark tier 3" />
  <img src="https://raw.githubusercontent.com/anna-ladutko/kalve/main/examples/sample_output/demo_dark/04_cta.png" width="22%" alt="Dark CTA" />
</p>

**`default_light`** — clean minimal light theme:
<p align="center">
  <img src="https://raw.githubusercontent.com/anna-ladutko/kalve/main/examples/sample_output/demo_light/01_tier1.png" width="22%" alt="Light tier 1" />
  <img src="https://raw.githubusercontent.com/anna-ladutko/kalve/main/examples/sample_output/demo_light/02_tier2.png" width="22%" alt="Light tier 2" />
  <img src="https://raw.githubusercontent.com/anna-ladutko/kalve/main/examples/sample_output/demo_light/03_tier3.png" width="22%" alt="Light tier 3" />
  <img src="https://raw.githubusercontent.com/anna-ladutko/kalve/main/examples/sample_output/demo_light/04_cta.png" width="22%" alt="Light CTA" />
</p>

**`saunuole`** — a real brand (Lithuanian language tutor):
<p align="center">
  <img src="https://raw.githubusercontent.com/anna-ladutko/kalve/main/examples/sample_output/compliments/01_turistas.png" width="22%" alt="Saunuole tier 1" />
  <img src="https://raw.githubusercontent.com/anna-ladutko/kalve/main/examples/sample_output/compliments/02_vietinis.png" width="22%" alt="Saunuole tier 2" />
  <img src="https://raw.githubusercontent.com/anna-ladutko/kalve/main/examples/sample_output/compliments/03_lietuvis.png" width="22%" alt="Saunuole tier 3" />
  <img src="https://raw.githubusercontent.com/anna-ladutko/kalve/main/examples/sample_output/compliments/04_cta.png" width="22%" alt="Saunuole CTA" />
</p>

---

## Who's this for

You, if you're an indie hacker, solo founder, or a small team that:

- ships your own product and runs your own social media
- is tired of hand-crafting posts in Canva or Figma every time you need to publish
- wants brand-consistent carousels without hiring a designer
- already thinks in JSON and loves `-as-code` workflows (GitOps, Infrastructure-as-Code, and now Carousels-as-Code)

Configure a brand kit once — from that point every new carousel is one `python -m kalve spec.json` away. kalve pipes into any workflow (N8N, cron, GitHub Actions, a bash one-liner) and composes cleanly with any AI of choice — see [docs/AI_INTEGRATION.md](docs/AI_INTEGRATION.md) for a ready-to-paste system prompt.

---

## What it does

- **Templates as code.** Describe a card structure once — render unlimited variations by swapping content.
- **Brand kit separate from template.** Colors, fonts, radii in a single Python dataclass. Change the brand kit → entire visual language changes. Same JSON spec produces cards in any brand.
- **CLI and Python API.** One command from the terminal, or an import for your pipeline.
- **No AI inside.** kalve only renders pixels. AI-driven content generation lives *above* it — bring your own LLM, your own API keys, your own prompts. See [AI_INTEGRATION.md](docs/AI_INTEGRATION.md) for the ready-made recipe.
- **Ready-to-post output.** 1080×1350 PNG, sized for Instagram and Threads carousels.
- **Offline and deterministic.** No network calls, no telemetry, no surprises. Same input → same output, every time.

v0.1 ships with one template — `three_tiers` (a 4-card carousel showing "3 skill levels + CTA"). More templates are coming (see [roadmap](#roadmap)).

---

## Example

Input (`examples/saunuole_compliments.json`):

```json
{
  "brand": "saunuole",
  "template": "three_tiers",
  "spec": {
    "topic": "Compliments about food in a restaurant",
    "emoji": "🍽️",
    "tiers": ["turistas", "vietinis", "lietuvis"],
    "tier_labels_lt": ["Turistas", "Vietinis", "Lietuvis"],
    "tier_labels_native": ["tourist", "local", "Lithuanian"],
    "cards": [
      {"lt": "Labai skanu!", "native": "Very tasty!"},
      {"lt": "Patiekalas buvo tiesiog nuostabus.",
       "native": "The dish was simply wonderful."},
      {"lt": "Net pirštus galima aplaižyti!",
       "native": "You could lick your fingers!"}
    ]
  }
}
```

Output: four 1080×1350 PNG files, ready to post.

---

## Install

Requires Python 3.9+.

```bash
pip install kalve
```

Or from source:

```bash
git clone https://github.com/anna-ladutko/kalve.git
cd kalve
pip install -r requirements.txt
```

Fonts (Inter) ship with the package — no extra download needed.

---

## Usage

### CLI

```bash
python -m kalve examples/saunuole_compliments.json --output output/
```

Result: four PNG files in `output/`.

### Python API

```python
from kalve import generate
from kalve.brands.saunuole import SAUNUOLE

generate(
    spec={
        "topic": "Compliments about food",
        "emoji": "🍽️",
        "tiers": ["turistas", "vietinis", "lietuvis"],
        "tier_labels_lt": ["Turistas", "Vietinis", "Lietuvis"],
        "tier_labels_native": ["tourist", "local", "Lithuanian"],
        "cards": [
            {"lt": "Labai skanu!", "native": "Very tasty!"},
            {"lt": "Patiekalas buvo nuostabus.", "native": "The dish was wonderful."},
            {"lt": "Net pirštus galima aplaižyti!", "native": "Lick your fingers good!"},
        ],
    },
    brand=SAUNUOLE,
    template="three_tiers",
    output_dir="output/",
)
```

### With AI (your personal copywriter)

kalve is designed to pair with an AI assistant. Chat with Claude / ChatGPT / Cursor in natural language, get a valid JSON spec back, pipe it into kalve. A ready-to-paste system prompt and worked examples live in [docs/AI_INTEGRATION.md](docs/AI_INTEGRATION.md).

---

## Architecture

Three independent layers — any two can change without breaking the third:

1. **Engine** (`kalve/drawing.py`, `kalve/typography.py`) — low-level primitives: gradients, rounded rectangles, pill badges, fonts, emoji paste. Rarely touched.
2. **Template** (`kalve/templates/three_tiers.py`) — layout logic. What goes where on a card. Reads from the brand kit; never hardcodes colors.
3. **Brand kit** (`kalve/brands/saunuole.py`) — pure data. Colors, fonts, margins, tier palettes. No logic.

More detail in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

## Making your own brand kit

Copy `kalve/brands/saunuole.py`, change the values, register the import. Full step-by-step guide: [docs/BRAND_KIT_GUIDE.md](docs/BRAND_KIT_GUIDE.md).

---

## Extending kalve

Add a new template (Stories, OG images, ad banners), a new brand kit, or a new engine primitive — all covered in [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Repository structure

```
kalve/
├── kalve/                    Main package
│   ├── __init__.py           Public API: generate()
│   ├── __main__.py           CLI entry point
│   ├── brand.py              BrandKit dataclass
│   ├── drawing.py            Engine: gradients, rects, pills, emoji
│   ├── typography.py         Engine: fonts, text wrapping, auto-sizing
│   ├── colors.py             Engine: color helpers
│   ├── brands/               Brand kits (data)
│   │   └── saunuole.py       Reference brand
│   └── templates/            Card layouts (logic)
│       └── three_tiers.py    "3 skill levels + CTA" carousel
│
├── kalve/assets/fonts/       Inter font family (shipped with the package)
├── examples/                 Sample JSON specs and rendered PNGs
│
├── docs/
│   ├── ARCHITECTURE.md       Why three layers, how they compose
│   ├── BRAND_KIT_GUIDE.md    How to describe your own brand
│   └── AI_INTEGRATION.md     Using kalve with Claude/ChatGPT/Cursor
│
├── CLAUDE.md                 Context for AI assistants opening this repo
└── CONTRIBUTING.md           How to add brand kits, templates, primitives
```

---

## Roadmap

- [ ] `google_ads` template — 10 ad sizes from a single spec
- [ ] `og_image` template — Open Graph images for blogs and landing pages
- [ ] `story` template — vertical 1080×1920 stories for Instagram/Facebook
- [ ] Custom fonts in brand kits (not just Inter)
- [ ] Batch mode — many specs in, many carousels out
- [ ] Spec validation with human-readable error messages

---

## License

MIT. Do whatever you want with the code. The bundled Inter font is licensed separately under the [SIL Open Font License 1.1](https://github.com/rsms/inter/blob/master/LICENSE.txt).

---

## Why "kalve"

*Kalvė* is Lithuanian for "forge" — the place where raw material (a JSON spec) is hammered into a finished product (branded PNGs) with a single command.
