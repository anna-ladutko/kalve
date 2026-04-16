"""
kalve.drawing — низкоуровневые примитивы рисования
"""
from PIL import Image, ImageDraw, ImageFont
import math
import os

from .colors import hex_to_rgb


# ------------------------------------------------------------------
# Градиенты
# ------------------------------------------------------------------

def linear_gradient(size, color_from_hex, color_to_hex, angle_deg=0):
    """
    Создать изображение с линейным градиентом.

    Args:
        size: (width, height)
        color_from_hex: начальный цвет, например "#9DC9FF"
        color_to_hex: конечный цвет, например "#E5D6FF"
        angle_deg: угол по CSS-конвенции (0 = снизу вверх, 90 = слева направо,
                   180 = сверху вниз, 270 = справа налево, 280 = почти-горизонтальный)

    Returns:
        PIL.Image RGB
    """
    w, h = size
    c1 = hex_to_rgb(color_from_hex)
    c2 = hex_to_rgb(color_to_hex)

    # Делаем горизонтальный градиент шире чем диагональ
    diag = int(math.sqrt(w*w + h*h)) + 100
    grad = Image.new("RGB", (diag, 1))
    px = grad.load()
    for x in range(diag):
        t = x / (diag - 1)
        r = round(c1[0] + (c2[0] - c1[0]) * t)
        g = round(c1[1] + (c2[1] - c1[1]) * t)
        b = round(c1[2] + (c2[2] - c1[2]) * t)
        px[x, 0] = (r, g, b)

    # Растягиваем до квадрата
    grad_full = grad.resize((diag, diag), Image.NEAREST)

    # CSS угол → PIL поворот
    pil_rotate = -(angle_deg - 90)
    rotated = grad_full.rotate(pil_rotate, resample=Image.BICUBIC, expand=False)

    # Вырезаем центр
    cx, cy = rotated.size[0] // 2, rotated.size[1] // 2
    left = cx - w // 2
    top = cy - h // 2
    return rotated.crop((left, top, left + w, top + h))


# ------------------------------------------------------------------
# Скруглённые прямоугольники
# ------------------------------------------------------------------

def rounded_rect(img, xy, radius, fill_rgba):
    """
    Нарисовать скруглённый прямоугольник на img.

    Args:
        img: PIL.Image
        xy: (x1, y1, x2, y2)
        radius: радиус скругления в пикселях
        fill_rgba: (r, g, b, a) - заливка с альфой
    """
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.rounded_rectangle(xy, radius=radius, fill=fill_rgba)
    return Image.alpha_composite(img.convert("RGBA"), overlay)


# ------------------------------------------------------------------
# Pill (бейдж)
# ------------------------------------------------------------------

def pill(img, xy, text, font_obj, bg_rgb, text_rgb,
         pad_x=36, pad_y=16, radius=44):
    """
    Нарисовать pill-бейдж: скруглённый прямоугольник с текстом внутри.

    Args:
        img: PIL.Image
        xy: (x, y) - левый верхний угол бейджа
        text: текст внутри
        font_obj: шрифт
        bg_rgb: (r, g, b) - цвет фона
        text_rgb: (r, g, b) - цвет текста
        pad_x, pad_y: внутренние отступы
        radius: радиус скругления

    Returns:
        (новый img, ширина бейджа, высота бейджа)
    """
    d = ImageDraw.Draw(img)
    bbox = d.textbbox((0, 0), text, font=font_obj)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x, y = xy
    pw = tw + pad_x * 2
    ph = th + pad_y * 2

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rounded_rectangle([(x, y), (x + pw, y + ph)],
                         radius=radius, fill=bg_rgb + (255,))
    out = Image.alpha_composite(img, overlay)

    rd = ImageDraw.Draw(out)
    rd.text((x + pad_x - bbox[0], y + pad_y - bbox[1]),
            text, fill=text_rgb, font=font_obj)
    return out, pw, ph


# ------------------------------------------------------------------
# Эмодзи
# ------------------------------------------------------------------

EMOJI_FONT_PATH = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"


def render_emoji(emoji_char, size=80, emoji_font_path=None):
    """
    Отрендерить эмодзи в transparent PNG заданного размера.

    Note: использует Noto Color Emoji. На системах без него может упасть.
    """
    font_path = emoji_font_path or EMOJI_FONT_PATH
    if not os.path.exists(font_path):
        # Возвращаем пустую картинку, чтобы не ронять весь рендер
        return Image.new("RGBA", (size, size), (0, 0, 0, 0))

    # Noto Color Emoji - bitmap, нативный размер 109px
    img = Image.new("RGBA", (140, 140), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(font_path, size=109)
    d.text((10, 10), emoji_char, font=f, embedded_color=True)

    if size != 109:
        scale = size / 109
        new_w = int(140 * scale)
        new_h = int(140 * scale)
        img = img.resize((new_w, new_h), Image.LANCZOS)
    return img


def paste_emoji(img, emoji_char, x, y, target_size=80, emoji_font_path=None):
    """Вставить эмодзи на img в точку (x, y)."""
    em = render_emoji(emoji_char, size=target_size, emoji_font_path=emoji_font_path)
    img.paste(em, (x, y), em)
    return img
