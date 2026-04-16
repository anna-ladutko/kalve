"""
kalve.templates — шаблоны карточек.

Каждый шаблон — отдельный модуль с функцией render(spec, brand, output_dir).
"""
from . import three_tiers

__all__ = ["three_tiers"]
