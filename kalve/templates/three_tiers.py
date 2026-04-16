"""
kalve.templates.three_tiers — шаблон карусели «три уровня владения».

Структура карусели:
  Карточка 1 — tier 1 (например, Turistas: простая фраза)
  Карточка 2 — tier 2 (например, Vietinis: фраза посложнее)
  Карточка 3 — tier 3 (например, Lietuvis: идиома носителя)
  Карточка 4 — CTA (приглашение на сайт)

Использование:
    from kalve.brands.saunuole import SAUNUOLE
    from kalve.templates import three_tiers

    three_tiers.render({
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
             "native": "Аж пальчики оближешь!"},
        ],
    }, brand=SAUNUOLE, output_dir="output/")
"""
from PIL import Image, ImageDraw
import os

from ..typography import font, wrap_text, auto_size
from ..drawing import (
    linear_gradient, rounded_rect, pill, paste_emoji
)


CANVAS_SIZE = (1080, 1350)


# ------------------------------------------------------------------
# Phrase card
# ------------------------------------------------------------------

def _render_phrase_card(brand, content, tier_idx, fonts_dir=None):
    """
    Отрендерить одну карточку с фразой.

    Args:
        brand: BrandKit
        content: dict с полями:
            tier_key: ключ tier'а в brand.tiers
            tier_label_lt: подпись на бейдже (например, "Turistas")
            tier_label_native: подпись под бейджем (например, "турист")
            phrase_lt: литовская фраза
            phrase_native: перевод на родной язык читателя
            position: например, "1 / 3"
            emoji: эмодзи для верхнего угла
    """
    tier = brand.tiers.get(content["tier_key"])
    if not tier:
        raise ValueError(f"Tier '{content['tier_key']}' не найден в brand.tiers. "
                         f"Доступны: {list(brand.tiers.keys())}")

    # 1. Фон с пастельным градиентом
    bg_from, bg_to, bg_angle = brand.background_gradient
    bg = linear_gradient(CANVAS_SIZE, bg_from, bg_to, bg_angle).convert("RGBA")

    # 2. Белая внутренняя карточка
    m = brand.inner_card_margin
    bg = rounded_rect(
        bg,
        (m, m, CANVAS_SIZE[0] - m, CANVAS_SIZE[1] - m),
        radius=brand.inner_card_radius,
        fill_rgba=brand.inner_card_fill,
    )

    # 3. Эмодзи в правом верхнем углу карточки
    if content.get("emoji"):
        emoji_size = 100
        bg = paste_emoji(
            bg,
            content["emoji"],
            x=CANVAS_SIZE[0] - m - 50 - emoji_size,
            y=m + 50,
            target_size=emoji_size,
        )

    # 4. Бейдж tier'а
    inner_pad_x = m + 70
    pill_y = m + 80
    f_pill = font("bold", 38, fonts_dir)
    bg, pill_w, pill_h = pill(
        bg, (inner_pad_x, pill_y),
        content["tier_label_lt"], f_pill,
        bg_rgb=tier["pill_bg"], text_rgb=tier["pill_text"],
        pad_x=32, pad_y=14, radius=44,
    )

    # 5. Подпись под бейджем (родное слово)
    d = ImageDraw.Draw(bg)
    f_sub = font("regular", 28, fonts_dir)
    d.text(
        (inner_pad_x + 4, pill_y + pill_h + 10),
        content["tier_label_native"],
        fill=brand.text_muted,
        font=f_sub,
    )

    # 6. Brand mark в правом нижнем углу (Šaunuolė + ссылка)
    f_brand = font("semibold", 26, fonts_dir)
    f_url = font("regular", 22, fonts_dir)
    brand_y = CANVAS_SIZE[1] - m - 110
    d.text((inner_pad_x, brand_y), brand.product_name,
           fill=brand.accent, font=f_brand)
    d.text((inner_pad_x, brand_y + 36), brand.product_url,
           fill=brand.text_muted, font=f_url)

    # 7. Номер карточки в правом нижнем углу
    f_pos = font("regular", 30, fonts_dir)
    pos_bbox = d.textbbox((0, 0), content["position"], font=f_pos)
    pos_w = pos_bbox[2] - pos_bbox[0]
    d.text(
        (CANVAS_SIZE[0] - m - 70 - pos_w, CANVAS_SIZE[1] - m - 90),
        content["position"],
        fill=brand.text_caption,
        font=f_pos,
    )

    # 8. Главный блок: фраза + перевод
    max_w = CANVAS_SIZE[0] - 2 * inner_pad_x

    f_phrase, phrase_lines, phrase_size = auto_size(
        content["phrase_lt"], max_w, d,
        weight="bold",
        size_options=[108, 92, 78, 66, 56, 48],
        max_lines=2,
        fonts_dir=fonts_dir,
    )
    plh = int(phrase_size * 1.06)
    phrase_h = len(phrase_lines) * plh

    f_native = font("regular", 48, fonts_dir)
    native_lines = wrap_text(content["phrase_native"], f_native, max_w, d)
    native_lh = int(48 * 1.2)
    native_h = len(native_lines) * native_lh

    gap = 36
    total = phrase_h + gap + native_h
    center_y = CANVAS_SIZE[1] // 2 + 40
    y = center_y - total // 2

    for line in phrase_lines:
        d.text((inner_pad_x, y), line, fill=brand.text_primary, font=f_phrase)
        y += plh
    y += gap
    for line in native_lines:
        d.text((inner_pad_x, y), line, fill=brand.text_secondary, font=f_native)
        y += native_lh

    return bg.convert("RGB")


# ------------------------------------------------------------------
# CTA card
# ------------------------------------------------------------------

def _render_cta_card(brand, content, fonts_dir=None):
    """Отрендерить финальную CTA-карточку."""
    bg_from, bg_to, bg_angle = brand.background_gradient
    bg = linear_gradient(CANVAS_SIZE, bg_from, bg_to, bg_angle).convert("RGBA")

    m = brand.inner_card_margin
    bg = rounded_rect(
        bg,
        (m, m, CANVAS_SIZE[0] - m, CANVAS_SIZE[1] - m),
        radius=brand.inner_card_radius,
        fill_rgba=brand.inner_card_fill,
    )

    # Большая эмодзи героем
    if content.get("emoji"):
        big = 240
        bg = paste_emoji(
            bg, content["emoji"],
            x=(CANVAS_SIZE[0] - big) // 2 + 5,
            y=300,
            target_size=big,
        )

    d = ImageDraw.Draw(bg)

    # Название продукта крупно
    f_word = font("bold_24", 92, fonts_dir)
    bbox = d.textbbox((0, 0), brand.product_name, font=f_word)
    tw = bbox[2] - bbox[0]
    d.text(
        ((CANVAS_SIZE[0] - tw) // 2, 600),
        brand.product_name,
        fill=brand.accent, font=f_word,
    )

    # Tagline (две строки)
    f_tag = font("regular", 44, fonts_dir)
    tagline_lines = content.get("tagline", "").split("\n")
    for i, line in enumerate(tagline_lines):
        bbox = d.textbbox((0, 0), line, font=f_tag)
        lw = bbox[2] - bbox[0]
        d.text(
            ((CANVAS_SIZE[0] - lw) // 2, 770 + i * 60),
            line,
            fill=brand.text_secondary, font=f_tag,
        )

    # CTA: "Переходи на" + ссылка
    cta_label = content.get("cta_label", "Переходи на")
    f_hint = font("regular", 32, fonts_dir)
    bbox = d.textbbox((0, 0), cta_label, font=f_hint)
    hw = bbox[2] - bbox[0]
    d.text(
        ((CANVAS_SIZE[0] - hw) // 2, 1010),
        cta_label,
        fill=brand.text_muted, font=f_hint,
    )

    # Ссылка крупно
    cta_url = content.get("cta_url", brand.product_url)
    f_link = font("bold", 80, fonts_dir)
    bbox = d.textbbox((0, 0), cta_url, font=f_link)
    lw = bbox[2] - bbox[0]
    d.text(
        ((CANVAS_SIZE[0] - lw) // 2, 1070),
        cta_url,
        fill=brand.accent, font=f_link,
    )

    return bg.convert("RGB")


# ------------------------------------------------------------------
# Public API
# ------------------------------------------------------------------

def render(spec, brand, output_dir, fonts_dir=None,
           shuffle_pattern_seed=None):
    """
    Сгенерировать карусель из 4 PNG: 3 фразы + CTA.

    Args:
        spec: dict с полями:
            topic: тема карусели (для метаданных)
            emoji: эмодзи (один на всю карусель)
            tier_labels_lt: ["Turistas", "Vietinis", "Lietuvis"]
            tier_labels_native: ["турист", "местный", "литовец"]
            tiers: ключи tier'ов в brand.tiers, например
                   ["turistas", "vietinis", "lietuvis"]
            cards: список из 3 объектов
                {"lt": "...", "native": "..."}
            cta_tagline: опционально, текст под названием на CTA
                         (по умолчанию: "Тренируй эти фразы\nбесплатно")
            cta_label: опционально, лейбл перед ссылкой на CTA
                       (по умолчанию: "Переходи на")
            cta_url: опционально, переопределить ссылку на CTA
                     (по умолчанию: brand.product_url + "/t")
        brand: BrandKit
        output_dir: куда складывать PNG
        fonts_dir: путь к папке шрифтов (опционально)

    Returns:
        список путей к сгенерированным файлам
    """
    os.makedirs(output_dir, exist_ok=True)

    n = len(spec["cards"])
    if n != 3:
        raise ValueError(f"Шаблон three_tiers ожидает ровно 3 карточки, получено {n}")

    paths = []

    # Phrase cards
    for i, card in enumerate(spec["cards"]):
        content = {
            "tier_key": spec["tiers"][i],
            "tier_label_lt": spec["tier_labels_lt"][i],
            "tier_label_native": spec["tier_labels_native"][i],
            "phrase_lt": card["lt"],
            "phrase_native": card["native"],
            "position": f"{i+1} / {n}",
            "emoji": spec.get("emoji", ""),
        }
        img = _render_phrase_card(brand, content, i, fonts_dir)
        fn = f"0{i+1}_{spec['tiers'][i]}.png"
        path = os.path.join(output_dir, fn)
        img.save(path, "PNG", optimize=True)
        paths.append(path)

    # CTA card
    cta_content = {
        "emoji": spec.get("emoji", ""),
        "tagline": spec.get("cta_tagline", "Тренируй эти фразы\nбесплатно"),
        "cta_label": spec.get("cta_label", "Переходи на"),
        "cta_url": spec.get("cta_url", brand.product_url + "/t"),
    }
    cta_img = _render_cta_card(brand, cta_content, fonts_dir)
    cta_path = os.path.join(output_dir, "04_cta.png")
    cta_img.save(cta_path, "PNG", optimize=True)
    paths.append(cta_path)

    return paths
