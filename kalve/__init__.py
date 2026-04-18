"""
kalve — генератор брендированных визуалов для соцсетей.

Простой пример использования:

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
                {"lt": "Patiekalas buvo nuostabus.", "native": "Блюдо было потрясающим."},
                {"lt": "Net pirštus galima aplaižyti!", "native": "Аж пальчики оближешь!"},
            ],
        },
        brand=SAUNUOLE,
        template="three_tiers",
        output_dir="output/",
    )
"""
from . import templates as _templates
from .brand import BrandKit

__version__ = "0.1.1"

# Реестр шаблонов
TEMPLATES = {
    "three_tiers": _templates.three_tiers,
}


def generate(spec, brand, template="three_tiers", output_dir="output/", fonts_dir=None):
    """
    Сгенерировать набор карточек по спецификации.

    Args:
        spec: dict с данными контента (структура зависит от шаблона)
        brand: BrandKit или строка-идентификатор готового бренда
        template: имя шаблона ("three_tiers" пока единственный)
        output_dir: куда складывать PNG
        fonts_dir: путь к папке со шрифтами (опционально)

    Returns:
        список путей к сгенерированным файлам
    """
    if template not in TEMPLATES:
        raise ValueError(f"Шаблон '{template}' не найден. Доступны: {list(TEMPLATES.keys())}")

    if isinstance(brand, str):
        # Поддержка строкового идентификатора в будущем
        from . import brands
        brand_obj = getattr(brands, brand.upper(), None)
        if not brand_obj:
            raise ValueError(f"Брендкит '{brand}' не найден")
        brand = brand_obj

    return TEMPLATES[template].render(spec, brand, output_dir, fonts_dir)


__all__ = ["generate", "BrandKit", "TEMPLATES"]
