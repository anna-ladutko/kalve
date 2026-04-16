"""
Брендкит Šaunuolė — тренажёр литовского языка.

Источник правды: design system проекта (фон, белые карточки, синий акцент).
"""
from ..brand import BrandKit


SAUNUOLE = BrandKit(
    name="saunuole",
    product_name="Šaunuolė",
    product_url="saunuolė.lt",
    hashtag="литовский",

    # Фон сайта: пастельный градиент с лёгким лиловым тоном
    background_gradient=("#9DC9FF", "#E5D6FF", 280),

    # Белая карточка без тени
    inner_card_fill=(255, 255, 255, 255),
    inner_card_radius=48,
    inner_card_margin=60,

    # Текст
    text_primary=(17, 24, 39),    # gray-900
    text_secondary=(55, 65, 81),  # gray-700
    text_muted=(107, 114, 128),   # gray-500
    text_caption=(156, 163, 175), # gray-400

    # Brand blue
    accent=(37, 99, 235),  # blue-600 - используется для wordmark и ссылок

    # Tier-цвета: бейджи трёх уровней
    tiers={
        "turistas": {
            "pill_bg":   (219, 234, 254),  # blue-100
            "pill_text": (29, 78, 216),    # blue-700
        },
        "vietinis": {
            "pill_bg":   (224, 231, 255),  # indigo-100
            "pill_text": (67, 56, 202),    # indigo-700
        },
        "lietuvis": {
            "pill_bg":   (254, 226, 226),  # red-100
            "pill_text": (185, 28, 28),    # red-700
        },
    },
)
