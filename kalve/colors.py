"""
kalve.colors — работа с цветом
"""


def hex_to_rgb(hex_color):
    """Конвертировать HEX в RGB tuple. Принимает '#RRGGBB' или 'RRGGBB'."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_with_alpha(rgb, alpha=255):
    """Добавить альфа-канал к RGB."""
    return rgb + (alpha,)
