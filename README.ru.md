[English](README.md) · **Русский**

# kalve

> **Carousels-as-code — no Canva, no Figma, just JSON.**

Генератор брендированных визуалов для соцсетей из JSON-спецификации.

Пишешь что должно быть на карточке — получаешь готовый набор PNG в фирменном стиле. Никакого Canva, никакого Figma, никакой ручной вёрстки.

Создан для проекта [Šaunuolė](https://saunuolė.lt) — тренажёра литовского языка, — но спроектирован как универсальный инструмент: подключаешь свой брендкит и получаешь карточки в своём стиле.

---

## Для кого

Если ты инди-разработчик, solo-мейкер или маленькая команда, которая:

- строит свой продукт и ведёт к нему соцсети сама
- устала от ручной вёрстки в Canva/Figma каждый раз, когда нужно что-то запостить
- хочет бренд-консистентные карусельки без дизайнера в штате
- уже думает в JSON и любит всё-`as-code`

— kalve для тебя. Один раз настраиваешь `brand.py` под свой проект — дальше карусели делаются одной командой из JSON. Встраивается в любой пайплайн (N8N, скрипт, CI), композируется с твоим любимым AI-инструментом (Claude, ChatGPT, Cursor) — см. [docs/AI_INTEGRATION.md](docs/AI_INTEGRATION.md).

---

## Что умеет

- **Шаблоны как код.** Один раз описали структуру карточки — рендерим сколько угодно вариантов с разным контентом.
- **Брендкит отдельно от шаблона.** Цвета, шрифты, настройки — в одном файле. Меняешь брендкит — меняется весь вид.
- **CLI и Python API.** Запускается одной командой или встраивается в пайплайн (N8N, скрипт, что угодно).
- **Без AI внутри.** kalve делает только рендер. AI-генерация спек живёт ВЫШЕ — используй свой любимый LLM и готовый промпт из [docs/AI_INTEGRATION.md](docs/AI_INTEGRATION.md).
- **Карусели для Threads и Instagram.** Формат 1080×1350, PNG, готовы к публикации.

На v0.1 есть один шаблон — `three_tiers` (карусель из 4 карточек про три уровня владения). Дальше добавим Google Ads баннеры, OG-картинки, Stories и что ещё скажешь.

---

## Пример

Что на входе:

```json
{
  "brand": "saunuole",
  "template": "three_tiers",
  "spec": {
    "topic": "Комплименты еде в ресторане",
    "emoji": "🍽️",
    "tiers": ["turistas", "vietinis", "lietuvis"],
    "tier_labels_lt": ["Turistas", "Vietinis", "Lietuvis"],
    "tier_labels_native": ["турист", "местный", "литовец"],
    "cards": [
      {"lt": "Labai skanu!", "native": "Очень вкусно!"},
      {"lt": "Patiekalas buvo tiesiog nuostabus.",
       "native": "Блюдо было просто потрясающим."},
      {"lt": "Net pirštus galima aplaižyti!",
       "native": "Аж пальчики оближешь!"}
    ]
  }
}
```

Что на выходе: 4 PNG карточки размером 1080×1350, готовые к публикации каруселью в Threads или Instagram. Примеры лежат в [examples/sample_output/compliments/](examples/sample_output/compliments/).

---

## Установка

Нужен Python 3.9+.

```bash
pip install kalve
```

Или из исходников:

```bash
git clone https://github.com/anna-ladutko/kalve.git
cd kalve
pip install -r requirements.txt
```

Шрифты (Inter) уже лежат в пакете — скачивать отдельно не нужно.

---

## Использование

### Через командную строку

```bash
python -m kalve examples/saunuole_compliments.json --output output/
```

Результат: 4 PNG в папке `output/`.

### Через Python

```python
from kalve import generate
from kalve.brands.saunuole import SAUNUOLE

generate(
    spec={
        "topic": "Комплименты еде",
        "emoji": "🍽️",
        "tiers": ["turistas", "vietinis", "lietuvis"],
        "tier_labels_lt": ["Turistas", "Vietinis", "Lietuvis"],
        "tier_labels_native": ["турист", "местный", "литовец"],
        "cards": [
            {"lt": "Labai skanu!", "native": "Очень вкусно!"},
            {"lt": "Patiekalas buvo nuostabus.",
             "native": "Блюдо было потрясающим."},
            {"lt": "Net pirštus galima aplaižyti!",
             "native": "Аж пальчики оближешь!"},
        ],
    },
    brand=SAUNUOLE,
    template="three_tiers",
    output_dir="output/",
)
```

### Через AI (твой личный copywriter)

kalve отлично работает в паре с AI-ассистентом. Общаешься с Claude/ChatGPT/Cursor словами, получаешь готовый JSON, скармливаешь в kalve. Готовый системный промпт и примеры — в [docs/AI_INTEGRATION.md](docs/AI_INTEGRATION.md).

---

## Архитектура

Три слоя, каждый можно менять независимо:

1. **Движок** (`kalve/drawing.py`, `kalve/typography.py`) — низкоуровневое рисование. Градиенты, скруглённые прямоугольники, pill-бейджи, шрифты, эмодзи. Редко трогается.

2. **Шаблон** (`kalve/templates/three_tiers.py`) — что и где на карточке. Принимает брендкит и контент, расставляет элементы. Хочешь новый формат (Google Ads, Story, OG) — пишешь новый шаблон.

3. **Брендкит** (`kalve/brands/saunuole.py`) — как это выглядит. Цвета, шрифты, скругления, фон. Хочешь другой бренд — пишешь свой файл.

Подробнее — в [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

## Как сделать свой брендкит

Смотри [docs/BRAND_KIT_GUIDE.md](docs/BRAND_KIT_GUIDE.md) — пошаговая инструкция с примером.

---

## Как расширить kalve

Новый шаблон (Story / OG-картинка / Google Ads), новый брендкит, новый движковый примитив — всё описано в [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Структура репозитория

```
kalve/
├── kalve/                    Основной пакет
│   ├── __init__.py           Главный API
│   ├── __main__.py           CLI
│   ├── brand.py              Базовый класс BrandKit
│   ├── drawing.py            Примитивы рисования
│   ├── typography.py         Работа со шрифтами
│   ├── colors.py             Утилиты цвета
│   ├── brands/               Готовые брендкиты
│   │   └── saunuole.py       Брендкит Šaunuolė
│   └── templates/            Шаблоны карточек
│       └── three_tiers.py    Карусель "три уровня владения"
│
├── assets/fonts/             Шрифты Inter
│
├── examples/                 Примеры входа и выхода
│   ├── saunuole_compliments.json
│   ├── saunuole_apologies.json
│   └── sample_output/        Сгенерированные примеры (в git)
│
├── docs/                     Подробная документация
│   ├── ARCHITECTURE.md       Почему три слоя, как они разделены
│   ├── BRAND_KIT_GUIDE.md    Как описать свой бренд
│   └── AI_INTEGRATION.md     Как генерить JSON через Claude/ChatGPT/Cursor
│
├── CLAUDE.md                 Контекст для AI-ассистентов (их читалка про проект)
└── CONTRIBUTING.md           Как добавить брендкит, шаблон или примитив
```

---

## Планы

- [ ] Шаблон `google_ads` — 10 размеров из одной спецификации
- [ ] Шаблон `og_image` — Open Graph картинки для блога/сайта
- [ ] Шаблон `story` — вертикальные Stories 1080×1920
- [ ] Поддержка кастомных шрифтов из брендкита
- [ ] Режим пакетной обработки (N спек → N каруселей)

---

## Лицензия

MIT. Делайте с кодом что хотите. Единственное условие — шрифт Inter распространяется по SIL Open Font License 1.1.

---

## Происхождение

Название — литовское слово «kalvė», то есть кузница. Потому что в этой штуке сырьё (JSON-спецификация) превращается в готовое изделие (картинка) одним нажатием.
