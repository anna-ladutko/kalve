# AI Integration — как использовать kalve с AI-ассистентом

> **kalve doesn't ship AI — it ships the recipe for using yours.**

kalve — чистый движок без встроенного AI. Это осознанный выбор: у тебя уже есть
твой любимый LLM (Claude, ChatGPT, Cursor, Copilot, локальная модель), и kalve
не должен тебя ни в чём ограничивать.

Авторский workflow выглядит так:

1. Открываешь чат с AI (Claude.ai / ChatGPT / Cursor / whatever).
2. Говоришь словами: "карусель про прощания по-литовски".
3. AI отдаёт валидный kalve-spec в JSON.
4. Сохраняешь в файл, запускаешь `python -m kalve spec.json -o output/`.
5. Получаешь 4 PNG, постишь.

Этот документ даёт тебе готовый системный промпт и примеры, чтобы ты мог
повторить этот workflow с любым LLM.

---

## Step 1 — copy this system prompt into your AI

Вставь это в поле "system prompt" (OpenAI Playground, Claude Projects, Custom
GPT, Cursor `.cursorrules`, и т.д.):

````
You are a writing assistant for `kalve`, a Python tool that renders
brand-consistent social-media carousel cards from JSON specs.

When the user describes a carousel idea, produce a valid kalve JSON spec for
the `three_tiers` template. Output ONLY the JSON (no prose, no markdown fences
unless the user asks for them).

Spec schema:

```json
{
  "brand": "saunuole",
  "template": "three_tiers",
  "spec": {
    "topic": "Short human-readable description of the carousel theme",
    "emoji": "Single emoji character fitting the theme",
    "tiers": ["tier1_key", "tier2_key", "tier3_key"],
    "tier_labels_lt": ["Label1", "Label2", "Label3"],
    "tier_labels_native": ["sublabel1", "sublabel2", "sublabel3"],
    "cards": [
      {"lt": "Phrase in target language", "native": "Translation"},
      {"lt": "Phrase in target language", "native": "Translation"},
      {"lt": "Phrase in target language", "native": "Translation"}
    ],
    "cta_tagline": "Optional CTA tagline, use \\n for line breaks",
    "cta_label": "Optional lead-in phrase before URL",
    "cta_url": "Optional URL override"
  }
}
```

Hard rules:
- Exactly 3 cards. Not 2, not 4.
- `tiers` keys must match keys in the brand kit's tiers dict.
  For the default `saunuole` brand: use "turistas", "vietinis", "lietuvis".
- `tier_labels_lt` is what appears on the badge (3 strings).
- `tier_labels_native` is the subtle caption below the badge (3 strings).
- Keep phrases ≤60 chars in the `lt` field so they render at full size.
- For `three_tiers`, the cards should show a progression: tier 1 simplest
  phrase, tier 3 most native/idiomatic.
- If the user uses a non-saunuole brand, adapt the tier keys to whatever they
  tell you their brand supports.

Return ONLY the JSON, starting with `{`.
````

Сохрани этот промпт один раз — в Claude Project, OpenAI Custom GPT, Cursor
rules file или любом другом reusable-месте. Дальше каждая новая карусель — одно
сообщение в чат.

---

## Step 2 — chat with AI

**You:** Сделай карусель про прощания по-литовски.

**AI:**
```json
{
  "brand": "saunuole",
  "template": "three_tiers",
  "spec": {
    "topic": "Прощания по-литовски",
    "emoji": "👋",
    "tiers": ["turistas", "vietinis", "lietuvis"],
    "tier_labels_lt": ["Turistas", "Vietinis", "Lietuvis"],
    "tier_labels_native": ["турист", "местный", "литовец"],
    "cards": [
      {"lt": "Viso!", "native": "Пока!"},
      {"lt": "Iki pasimatymo.", "native": "До встречи."},
      {"lt": "Iki, susitiksime!", "native": "Увидимся!"}
    ]
  }
}
```

---

## Step 3 — render with kalve

Сохрани AI-ответ в файл:

```bash
# Скопируй JSON в редактор, сохрани как farewells.json
python -m kalve farewells.json --output output/farewells/
```

Готово — 4 PNG в `output/farewells/`.

---

## Итеративный workflow (где рождается качество)

Магия не в одном запросе, а в диалоге. Примеры полезных follow-up:

- *"Третья карточка слишком длинная, укороти её"*
- *"Сделай тональность более весёлой"*
- *"Замени второй вариант на более бытовой, как местный сказал бы другу"*
- *"Добавь восклицательный знак на первой карточке"*

AI поправит JSON, ты перезапустишь kalve, получишь новую версию. Такая
итерация — именно та причина, почему "AI + kalve" лучше, чем одноразовый
генератор.

---

## Если используешь свой брендкит (не `saunuole`)

1. Замени `"brand": "saunuole"` в JSON на ключ твоего бренда.
2. Поменяй `tiers` и `tier_labels_*` под твои категории. Примеры:
   - `"beginner"` / `"intermediate"` / `"advanced"`
   - `"free"` / `"pro"` / `"enterprise"`
   - `"easy"` / `"medium"` / `"hard"`
3. Если в твоём проекте не нужен билингвальный контент (`lt` + `native`),
   опиши своему AI, какие поля использовать вместо. Или сделай кастомный
   шаблон — см. [CONTRIBUTING.md](../CONTRIBUTING.md).

---

## Почему AI не встроен в kalve сам

- У тебя уже есть любимый LLM. Зачем нам его выбирать за тебя.
- Встроенный AI = обязательный API-ключ = барьер входа.
- Недетерминизм: для брендинга важно получать одинаковый результат на одинаковом входе.
- Композиция сильнее интеграции. Unix philosophy: one tool, one job, pipes between.

kalve = deterministic renderer. AI = content generator. Пайп между ними — твой
любимый LLM.

---

## Примеры готовых промптов для разных кейсов

**Для разработчика продукта (не про языки):**
> "You are generating carousel specs for [my product]. Tier keys are 'basic',
> 'pro', 'enterprise'. Each card shows a feature at that tier level. Use my
> brand 'myproduct'."

**Для контент-криэйтора (советы / лайфхаки):**
> "You are generating three-step tutorials as carousels. Tier keys are 'step1',
> 'step2', 'step3'. `lt` field holds the step action, `native` holds the
> detailed explanation."

**Для образовательного проекта:**
> "You are generating flashcard carousels. Tier keys are 'beginner',
> 'intermediate', 'advanced'. `lt` holds the term, `native` holds the
> definition."

Адаптируй под свой проект — схема гибкая.
