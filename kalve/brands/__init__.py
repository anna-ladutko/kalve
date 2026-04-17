"""
kalve.brands — готовые брендкиты.

Подключаем как:
    from kalve.brands.saunuole import SAUNUOLE
    from kalve.brands.default_dark import DEFAULT_DARK
    from kalve.brands.default_light import DEFAULT_LIGHT
"""
from .saunuole import SAUNUOLE
from .default_dark import DEFAULT_DARK
from .default_light import DEFAULT_LIGHT

__all__ = ["SAUNUOLE", "DEFAULT_DARK", "DEFAULT_LIGHT"]
