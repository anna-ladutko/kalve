# CLAUDE.md — guide for AI assistants

You are helping a developer use or extend **kalve**, a small Python tool that
generates brand-consistent social-media carousels from JSON specs.

This file is a high-density mental model of the project. Read it once before
touching code. Then use `docs/ARCHITECTURE.md`, `docs/BRAND_KIT_GUIDE.md`, and
`docs/AI_INTEGRATION.md` for depth.

---

## Product identity

- **Tagline:** Carousels-as-code — no Canva, no Figma, just JSON.
- **Input:** a JSON spec (content) + a brand kit (visual language) + a template (layout).
- **Output:** a set of PNG files ready to post on Instagram/Threads.
- **Core philosophy:** one tool, one job. kalve renders pixels. It does NOT
  generate content, publish posts, or bundle an LLM.

The "universal" claim matters: kalve was born for Šaunuolė (a Lithuanian language
tutor product) but is designed so any indie maker can plug in their own brand
and get on-brand cards.

---

## Mental model — three independent layers

```
  ┌─────────────────┐
  │   BRAND KIT     │  Pure data: colors, fonts, radii, tier colors
  │   brand.py      │
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │   TEMPLATE      │  Layout logic: where things go on a card
  │   template.py   │  (reads brand + content, calls engine)
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │   ENGINE        │  Low-level primitives:
  │   drawing.py    │  gradients, rounded rects, pills, emoji,
  │   typography.py │  text wrapping, auto-sizing
  └─────────────────┘
```

Any two of the three change independently:
- **New brand, same template** → write `kalve/brands/mybrand.py`, reuse `three_tiers`.
- **New template, same brand** → write `kalve/templates/story.py`, pass `SAUNUOLE`.
- **New engine primitive** → add standalone function to `drawing.py` / `typography.py`,
  templates opt in.

Invariants to preserve:
- Brand kits stay pure data (dataclass fields, no methods, no logic).
- Templates never hardcode colors — always pull from `brand`.
- Engine primitives know nothing about brand or template — they take coordinates and colors.

---

## Where things live

```
kalve/
├── kalve/                     The package itself
│   ├── __init__.py            Public API: generate(spec, brand, template, output_dir)
│   ├── __main__.py            CLI entry: `python -m kalve <input.json>`
│   ├── brand.py               BrandKit base dataclass
│   ├── drawing.py             Engine: gradients, rects, pills, emoji paste
│   ├── typography.py          Engine: font loading, text wrapping, auto-sizing
│   ├── colors.py              Engine: color helpers (hex→rgb, etc)
│   ├── brands/                Brand kits (data)
│   │   └── saunuole.py        Šaunuolė brand (reference example)
│   └── templates/             Card layouts (logic)
│       └── three_tiers.py     Reference template: 3 skill-level cards + CTA
│
├── kalve/assets/fonts/        Inter font family (ships with the package)
├── examples/                  Sample JSON specs and rendered PNGs
├── docs/                      Human-facing documentation
├── CLAUDE.md                  ← You are here
└── CONTRIBUTING.md            Extension points, code style, PR checklist
```

---

## Key commands

```bash
# Install
pip install -r requirements.txt

# CLI (reads brand/template from JSON or flags)
python -m kalve examples/saunuole_compliments.json --output output/
python -m kalve my_spec.json --brand mybrand --template three_tiers -o out/

# Python API
from kalve import generate
from kalve.brands.saunuole import SAUNUOLE

generate(
    spec={...},              # dict matching the template's expected shape
    brand=SAUNUOLE,
    template="three_tiers",
    output_dir="output/",
)
```

The CLI accepts JSON in two shapes:
- Wrapped: `{"brand": "...", "template": "...", "spec": {...}}`
- Flat: the spec object directly (use `--brand` / `--template` flags).

---

## How to add a brand kit (for a new project)

See `docs/BRAND_KIT_GUIDE.md` for the full walkthrough. Short version:

1. Copy `kalve/brands/saunuole.py` → `kalve/brands/mybrand.py`.
2. Edit values: colors, `product_name`, `product_url`, `tiers` dict.
3. Register the import in `kalve/brands/__init__.py`.
4. For CLI access, add to `BRAND_REGISTRY` in `kalve/__main__.py`.

Constraints:
- `tiers` dict keys must match `spec["tiers"]` strings coming in from JSON.
- `pill_bg` should be light; `pill_text` dark — maintain contrast.
- All color tuples are RGB or RGBA as integer 0-255 (not 0-1 floats).

---

## How to add a template (for a new card format: Story, OG, Banner, etc.)

1. Create `kalve/templates/mytemplate.py`.
2. Expose `render(spec, brand, output_dir, fonts_dir=None) -> list[str]`.
   - Returns absolute/relative paths of generated files.
3. Use `CANVAS_SIZE = (w, h)` module-level constant for the card dimensions.
4. Compose with `drawing.linear_gradient`, `drawing.rounded_rect`, `drawing.pill`,
   `drawing.paste_emoji`, `typography.font`, `typography.wrap_text`,
   `typography.auto_size`.
5. Register in `kalve/__init__.py`:
   ```python
   TEMPLATES = {
       "three_tiers": _templates.three_tiers,
       "mytemplate": _templates.mytemplate,   # add this
   }
   ```
6. Document the spec shape in a module docstring.

Reference implementation: `kalve/templates/three_tiers.py`. Read it first — the
patterns there (tier-badge pill, auto-sized phrase, brand mark in corner,
position counter) are meant to be reused.

---

## Rules of engagement for AI assistants

**Do:**
- Keep brand kits as pure data (dataclass fields, no logic, no I/O).
- Keep templates as pure layout — always `brand.foo`, never hardcoded `(37, 99, 235)`.
- Fail loudly with `ValueError` for invalid specs (see existing pattern in `three_tiers.render`).
- Prefer direct, readable code. kalve is ~1400 lines total — contributors should
  grok it in 30 minutes.
- When adding a dependency, ask first. Current deps: Pillow only.

**Don't:**
- Don't add LLM calls into kalve core. AI usage lives above kalve — see `docs/AI_INTEGRATION.md`.
- Don't couple a brand kit to a specific template. A brand should work with ANY template.
- Don't make templates call the network — kalve is offline-first and deterministic.
- Don't add animations / video / GIF output — static PNG/JPG only.
- Don't invent abstractions without a second concrete use case. "Maybe later we'll need X" is not a reason; two real callers is.

---

## When a user asks you to extend kalve, ask these three questions first

1. **Which layer is this?** Engine primitive, template, or brand kit? Each lives
   in a different folder and has different rules.
2. **Does it respect the separation?** If your "brand kit" has a `render()`
   method or your "template" has `#FF0000` hardcoded, stop and restructure.
3. **Is it reusable or one-off?** If it's specific to one project, keep it in
   that project (extend kalve there as a consumer), not in kalve itself.

---

## Current limitations (honest list)

- Only one template (`three_tiers`). Adding more is the main v0.2 roadmap item.
- Font support is Inter-only. Brand kits can't yet specify their own font family.
- No spec validation layer — invalid JSON gives you a stack trace.
- No batch mode — one spec = one carousel. Loop in bash for now.
- No PyPI package yet — install via `git clone`.

These are known. PRs welcome.
