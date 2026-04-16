# Contributing to kalve

Thanks for looking. kalve is deliberately small — it does one thing (render
brand-consistent carousels from JSON) and tries to do it well. Contributions
are welcome, but please read below first so we stay on the same page.

---

## What kalve is (and isn't)

kalve **is** a deterministic rendering engine: JSON in, PNG out. Runs offline,
locally, fast. One dependency (Pillow). ~1400 lines of code.

kalve **is not**: a SaaS, a content generator, a publisher, an AI wrapper, a
Canva replacement with UI. Those are different products with different
trade-offs — by not being them, kalve stays small and composable.

---

## Extension points

There are three places where extension lives, each with its own rules.

### 1. New brand kit — for your project's visual language

Colors, fonts, radii, tier colors. Pure data.

→ Full walkthrough: [docs/BRAND_KIT_GUIDE.md](docs/BRAND_KIT_GUIDE.md)

PRs with brand kits are welcome — we want a gallery of real-world examples.
Before submitting:
- Include a sample `examples/<yourbrand>_<topic>.json`
- Include one generated PNG in `examples/sample_output/<yourbrand>/` so people
  can see the result without running anything.

### 2. New template — for a new card format

Instagram Story (1080×1920), OG image (1200×630), Google Ads banner, Twitter/X
card, anything.

1. Create `kalve/templates/mytemplate.py`.
2. Expose `render(spec, brand, output_dir, fonts_dir=None) -> list[str]`.
3. Use engine primitives from `drawing.py` / `typography.py`. Do NOT hardcode
   colors — pull from `brand.foo`.
4. Return a list of generated file paths.
5. Register in `kalve/__init__.py` under `TEMPLATES`.
6. Add a module docstring describing the expected `spec` shape.

Look at `kalve/templates/three_tiers.py` as a reference. The patterns there
(auto-sized text, brand mark in corner, position counter, tier badge) are
meant to be reused or adapted.

### 3. New engine primitive — for new low-level drawing operations

Add a standalone function to `kalve/drawing.py` or `kalve/typography.py`. Must
be:
- Pure inputs → pure outputs (no brand/template awareness).
- Composable: one function, one responsibility.
- Documented in docstring with types.

---

## Code style

- **Small, readable functions.** kalve is grokable in one sitting; let's keep it that way.
- **Dataclasses for config.** Brand kits are data, not classes with methods.
- **Fail loudly.** `ValueError` with a clear message for invalid input. See
  how `three_tiers.render` handles the wrong card count as the reference pattern.
- **Docstrings on anything public.** The engine functions are libraries for
  template authors — they need a docstring.
- **Comments:** Russian is fine in code authored by the original maintainer;
  English preferred for new contributions for reach.

---

## PR checklist

Before opening a PR, make sure:

- [ ] `python -m kalve examples/saunuole_compliments.json --output /tmp/test/` still works
- [ ] If you added a template: there's an example JSON in `examples/` and a
      sample PNG in `examples/sample_output/`
- [ ] If you added a brand kit: it's registered in `kalve/brands/__init__.py`
      AND `kalve/__main__.py` (`BRAND_REGISTRY`)
- [ ] If you added a new dependency: it's in `requirements.txt` AND the PR
      description explains why
- [ ] README updated if user-visible behavior changed
- [ ] No `print()` debug statements left behind

---

## What you will NOT see merged

Keeping scope tight on purpose:

- **Bundled LLM calls.** kalve renders pixels. AI lives above it — see
  [docs/AI_INTEGRATION.md](docs/AI_INTEGRATION.md).
- **Web UI.** Separate project if someone wants it. kalve stays a library/CLI.
- **Video / GIF / animation output.** PNG/JPG only.
- **Analytics / telemetry.** Offline-first, user-owned.
- **Auto-posting to social networks.** Publishing is a separate concern
  (N8N, Zapier, your own script).

If you want any of those, fork and go wild — MIT license, no strings.

---

## Running a sanity check locally

```bash
# Install
pip install -r requirements.txt

# Reference run
python -m kalve examples/saunuole_compliments.json --output /tmp/kalve-test/

# You should see:
#   Сгенерировано 4 файлов:
#     /tmp/kalve-test/01_turistas.png
#     /tmp/kalve-test/02_vietinis.png
#     /tmp/kalve-test/03_lietuvis.png
#     /tmp/kalve-test/04_cta.png

# Compare visually with examples/sample_output/compliments/ — should look the same.
```

---

## Questions / discussion

Open an issue. The maintainer will respond.
