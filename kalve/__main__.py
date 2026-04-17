"""
kalve.__main__ — CLI для запуска через `python -m kalve`.

Использование:
    python -m kalve <input.json> [--output OUTPUT_DIR] [--brand BRAND_NAME]

Пример:
    python -m kalve examples/saunuole_compliments.json --output output/

Формат input.json:
    {
        "brand": "saunuole",
        "template": "three_tiers",
        "spec": { ... }
    }
"""
import argparse
import json
import sys

from . import generate, TEMPLATES
from . import brands


BRAND_REGISTRY = {
    "saunuole": brands.SAUNUOLE,
    "default_dark": brands.DEFAULT_DARK,
    "default_light": brands.DEFAULT_LIGHT,
}


def main():
    parser = argparse.ArgumentParser(
        prog="kalve",
        description="Генератор брендированных визуалов для соцсетей",
    )
    parser.add_argument("input", help="Путь к JSON-файлу со спецификацией")
    parser.add_argument(
        "--output", "-o",
        default="output/",
        help="Папка для сгенерированных PNG (по умолчанию: output/)",
    )
    parser.add_argument(
        "--brand", "-b",
        default=None,
        help=f"Идентификатор бренда. Доступны: {list(BRAND_REGISTRY.keys())}. "
             "Если не указан — берётся из 'brand' в JSON.",
    )
    parser.add_argument(
        "--template", "-t",
        default=None,
        help=f"Шаблон. Доступны: {list(TEMPLATES.keys())}. "
             "Если не указан — берётся из 'template' в JSON.",
    )

    args = parser.parse_args()

    # Загружаем JSON
    try:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Ошибка: файл не найден: {args.input}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Ошибка: невалидный JSON в {args.input}: {e}", file=sys.stderr)
        sys.exit(1)

    # Определяем бренд
    brand_name = args.brand or data.get("brand")
    if not brand_name:
        print("Ошибка: не указан бренд (--brand или поле 'brand' в JSON)", file=sys.stderr)
        sys.exit(1)

    brand = BRAND_REGISTRY.get(brand_name.lower())
    if not brand:
        print(f"Ошибка: бренд '{brand_name}' не найден. "
              f"Доступны: {list(BRAND_REGISTRY.keys())}", file=sys.stderr)
        sys.exit(1)

    # Определяем шаблон
    template_name = args.template or data.get("template", "three_tiers")

    # Получаем spec
    spec = data.get("spec", data)  # позволяем как с обёрткой spec, так и без

    # Запускаем генерацию
    try:
        paths = generate(
            spec=spec,
            brand=brand,
            template=template_name,
            output_dir=args.output,
        )
    except (ValueError, KeyError) as e:
        print(f"Ошибка генерации: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Сгенерировано {len(paths)} файлов:")
    for p in paths:
        print(f"  {p}")


if __name__ == "__main__":
    main()
