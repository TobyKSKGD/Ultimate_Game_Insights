from pathlib import Path

import pandas as pd
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "steam_march2025_features.parquet"
OUTPUT_PATH = ROOT / "figures" / "10_free_vs_paid_market_share.png"
FONT_DIR = ROOT / ".venv" / "lib" / "python3.13" / "site-packages" / "matplotlib" / "mpl-data" / "fonts" / "ttf"


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    path = FONT_DIR / name
    if path.exists():
        return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def text_size(draw: ImageDraw.ImageDraw, text: str, face: ImageFont.ImageFont) -> tuple[int, int]:
    left, top, right, bottom = draw.textbbox((0, 0), text, font=face)
    return right - left, bottom - top


def draw_centered_text(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    text: str,
    face: ImageFont.ImageFont,
    fill: str,
) -> None:
    x1, y1, x2, y2 = box
    width, height = text_size(draw, text, face)
    draw.text((x1 + (x2 - x1 - width) / 2, y1 + (y2 - y1 - height) / 2 - 2), text, font=face, fill=fill)


def main() -> None:
    free_flags = pd.read_parquet(DATA_PATH, columns=["is_free"])["is_free"].fillna(False)
    free_count = int(free_flags.sum())
    paid_count = int((~free_flags).sum())
    total = free_count + paid_count

    paid_share = paid_count / total
    free_share = free_count / total

    width, height = 1600, 720
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    ink = "#202124"
    muted = "#5F6368"
    bg = "#FAFBFC"
    border = "#DFE3E8"
    track = "#E7EAEE"
    paid = "#D85C5C"
    free = "#3E8F5D"

    title_font = font("DejaVuSans-Bold.ttf", 48)
    subtitle_font = font("DejaVuSans.ttf", 27)
    label_font = font("DejaVuSans-Bold.ttf", 31)
    small_label_font = font("DejaVuSans-Bold.ttf", 28)
    number_font = font("DejaVuSans-Bold.ttf", 54)
    body_font = font("DejaVuSans.ttf", 26)
    note_font = font("DejaVuSans.ttf", 23)

    draw.text((80, 58), "Free vs Paid Games Share", font=title_font, fill=ink)
    draw.text((80, 125), f"Steam games in dataset: {total:,}", font=subtitle_font, fill=muted)

    bar_x, bar_y, bar_w, bar_h = 80, 235, 1440, 78
    radius = bar_h // 2
    draw.rounded_rectangle((bar_x, bar_y, bar_x + bar_w, bar_y + bar_h), radius=radius, fill=track)

    paid_w = round(bar_w * paid_share)
    free_w = bar_w - paid_w
    paid_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    paid_draw = ImageDraw.Draw(paid_layer)
    paid_draw.rectangle((bar_x, bar_y, bar_x + paid_w, bar_y + bar_h), fill=paid)
    free_draw = ImageDraw.Draw(paid_layer)
    free_draw.rectangle((bar_x + paid_w, bar_y, bar_x + bar_w, bar_y + bar_h), fill=free)

    mask = Image.new("L", (width, height), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle((bar_x, bar_y, bar_x + bar_w, bar_y + bar_h), radius=radius, fill=255)
    img.paste(paid_layer.convert("RGB"), (0, 0), mask)

    split_x = bar_x + paid_w
    draw.line((split_x, bar_y - 8, split_x, bar_y + bar_h + 8), fill="white", width=7)

    draw_centered_text(draw, (bar_x, bar_y, split_x, bar_y + bar_h), f"Paid {paid_share:.1%}", label_font, "white")
    draw_centered_text(draw, (split_x, bar_y, bar_x + bar_w, bar_y + bar_h), f"Free {free_share:.1%}", small_label_font, "white")

    card_y, card_h = 380, 192
    card_w, gap = 690, 60
    cards = [
        (80, "Paid games", paid_count, paid_share, paid),
        (80 + card_w + gap, "Free games", free_count, free_share, free),
    ]

    for x, label, count, share, color in cards:
        draw.rounded_rectangle((x, card_y, x + card_w, card_y + card_h), radius=18, fill=bg, outline=border, width=3)
        draw.rectangle((x + 38, card_y + 37, x + 63, card_y + 62), fill=color)
        draw.text((x + 82, card_y + 30), label, font=label_font, fill=ink)
        draw.text((x + 38, card_y + 86), f"{count:,}", font=number_font, fill=color)
        draw.text((x + 38, card_y + 154), f"{share:.1%} of all games", font=body_font, fill=muted)

    note = "Paid games remain the dominant supply model; free games form a smaller but visible segment."
    draw.text((80, 625), note, font=note_font, fill=muted)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUTPUT_PATH, optimize=True)
    print(f"Saved {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
