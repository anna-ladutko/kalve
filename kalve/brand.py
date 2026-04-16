"""
kalve.brand — базовый класс брендкита

Брендкит описывает визуальный язык конкретного продукта или компании:
цвета, шрифты, фон, скругления, особенности типографики.

Свой брендкит делается наследованием от BrandKit.
"""
from dataclasses import dataclass, field
from typing import Tuple


@dataclass
class BrandKit:
    """
    Базовый брендкит. Содержит только обязательные настройки.

    Чтобы создать свой бренд, наследуйся и переопредели поля.
    Смотри пример в kalve/brands/saunuole.py
    """
    # Идентификатор бренда (используется в логах и метаданных)
    name: str = "default"

    # Имя продукта - выводится на CTA-карточке
    product_name: str = "Product"

    # Главная ссылка - выводится на CTA-карточке  
    product_url: str = "example.com"

    # Hashtag для поста (без #)
    hashtag: str = ""

    # ---- Фон ----
    # CSS-стиль linear-gradient: (color_from_hex, color_to_hex, angle_deg)
    background_gradient: Tuple[str, str, int] = ("#FFFFFF", "#FFFFFF", 0)

    # Цвет белой карточки внутри
    inner_card_fill: Tuple[int, int, int, int] = (255, 255, 255, 255)
    inner_card_radius: int = 48
    inner_card_margin: int = 60  # отступ от края канвы

    # ---- Цвета текста ----
    text_primary: Tuple[int, int, int] = (17, 24, 39)    # gray-900
    text_secondary: Tuple[int, int, int] = (55, 65, 81)  # gray-700
    text_muted: Tuple[int, int, int] = (107, 114, 128)   # gray-500
    text_caption: Tuple[int, int, int] = (156, 163, 175) # gray-400

    # ---- Акцент (логотип / основная кнопка) ----
    accent: Tuple[int, int, int] = (37, 99, 235)  # blue-600

    # ---- Tier-цвета (для шаблонов с прогрессией) ----
    # Каждый tier - словарь "идентификатор" → {"pill_bg": rgb, "pill_text": rgb}
    tiers: dict = field(default_factory=dict)
