"""
kalve.typography — работа со шрифтами
"""
from PIL import ImageFont
import os

# Маппинг семантических весов на файлы Inter
INTER_WEIGHTS = {
    "thin": "Inter_18pt-Thin.ttf",
    "regular": "Inter_18pt-Regular.ttf",
    "semibold": "Inter_18pt-SemiBold.ttf",
    "bold": "Inter_18pt-Bold.ttf",
    "extrabold": "Inter_18pt-ExtraBold.ttf",
    "black": "Inter_18pt-Black.ttf",
    "bold_24": "Inter_24pt-Bold.ttf",  # Оптический размер для крупных заголовков
}


def get_fonts_dir():
    """Вернуть путь к папке со шрифтами kalve."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "..", "assets", "fonts")


def font(weight, size, fonts_dir=None):
    """
    Загрузить шрифт Inter заданного веса и размера.

    Args:
        weight: "thin", "regular", "semibold", "bold", "extrabold", "black", "bold_24"
        size: размер в пикселях
        fonts_dir: опционально - путь к папке со шрифтами

    Returns:
        PIL.ImageFont
    """
    if weight not in INTER_WEIGHTS:
        raise ValueError(f"Неизвестный вес шрифта: {weight}. "
                         f"Доступны: {list(INTER_WEIGHTS.keys())}")

    fonts_dir = fonts_dir or get_fonts_dir()
    path = os.path.join(fonts_dir, INTER_WEIGHTS[weight])

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Шрифт не найден: {path}. "
            f"Убедись что файлы Inter лежат в assets/fonts/"
        )

    return ImageFont.truetype(path, size)


def wrap_text(text, font_obj, max_width, draw):
    """
    Разбить текст на строки чтобы каждая помещалась в max_width.
    Возвращает список строк.
    """
    words = text.split()
    lines = []
    current = []
    for word in words:
        test = " ".join(current + [word])
        bbox = draw.textbbox((0, 0), test, font=font_obj)
        if bbox[2] - bbox[0] <= max_width:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines


def auto_size(text, max_width, draw, weight="bold",
              size_options=None, max_lines=2, fonts_dir=None):
    """
    Подобрать самый крупный размер шрифта, при котором текст
    помещается в max_width не более чем за max_lines строк.

    Args:
        text: текст для размещения
        max_width: доступная ширина в пикселях
        draw: PIL.ImageDraw для измерения
        weight: вес шрифта
        size_options: список размеров для перебора (от большего к меньшему)
        max_lines: максимум строк
        fonts_dir: путь к шрифтам

    Returns:
        (font_obj, lines_list, chosen_size)
    """
    if size_options is None:
        size_options = [136, 118, 102, 88, 76, 66, 56, 48, 40]

    for size in size_options:
        f = font(weight, size, fonts_dir)
        lines = wrap_text(text, f, max_width, draw)
        if len(lines) <= max_lines:
            return f, lines, size

    # Если ничего не подошло, берём самый мелкий
    f = font(weight, size_options[-1], fonts_dir)
    return f, wrap_text(text, f, max_width, draw), size_options[-1]
