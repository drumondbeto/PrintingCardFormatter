#!/usr/bin/env python3
"""Generate an A4 PDF from PNG images in `src/`.

- Reads PNG files from `src/` (alphabetical)
- Places images into an A4 PDF in a grid
- Each image is fitted into 63.5mm x 88mm (preserving aspect ratio) and centered
- Spacing and margins default to 10 mm
- Output saved to project root as <unix_milliseconds>.pdf

Dependencies: Pillow, reportlab
"""
import os
import time
import math
from io import BytesIO
from PIL import Image, ImageOps
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

# Config (mm / DPI)
CARD_W_MM = 63.5
CARD_H_MM = 88.0
MARGIN_MM = 4.0
SPACING_MM = 5.0
DPI = 300  # target print DPI (use high-res source and downscale)

SRC_DIR = os.path.join(os.path.dirname(__file__), "src")
OUT_DIR = os.path.dirname(__file__)  # save PDF in project root

# Conversions
MM_TO_PT = 72.0 / 25.4
MM_TO_PX = DPI / 25.4

CARD_W_PT = CARD_W_MM * MM_TO_PT
CARD_H_PT = CARD_H_MM * MM_TO_PT
MARGIN_PT = MARGIN_MM * MM_TO_PT
SPACING_PT = SPACING_MM * MM_TO_PT

CARD_W_PX = int(round(CARD_W_MM * MM_TO_PX))
CARD_H_PX = int(round(CARD_H_MM * MM_TO_PX))

PAGE_W_PT, PAGE_H_PT = A4
PAGE_W_MM = 210.0
PAGE_H_MM = 297.0

def list_pngs(folder):
    if not os.path.isdir(folder):
        return []
    files = [f for f in os.listdir(folder) if f.lower().endswith(".png")]
    files.sort()
    return [os.path.join(folder, f) for f in files]

def prepare_image(path):
    img = Image.open(path)
    # If has alpha, composite onto white
    if "A" in img.getbands():
        bg = Image.new("RGBA", img.size, (255,255,255,255))
        bg.paste(img, mask=img.split()[-1])
        img = bg.convert("RGB")
    else:
        img = img.convert("RGB")

    # Only downscale (no upscaling)
    target = (CARD_W_PX, CARD_H_PX)
    if img.width > CARD_W_PX or img.height > CARD_H_PX:
        img_small = ImageOps.contain(img, target, Image.Resampling.LANCZOS)
    else:
        img_small = img

    # Place centered on white canvas exactly target pixels
    canvas_img = Image.new("RGB", target, "white")
    x = (target[0] - img_small.width) // 2
    y = (target[1] - img_small.height) // 2
    canvas_img.paste(img_small, (x, y))

    bio = BytesIO()
    canvas_img.save(bio, format="PNG")
    bio.seek(0)
    return bio

def compute_grid():
    usable_w_mm = PAGE_W_MM - 2 * MARGIN_MM
    usable_h_mm = PAGE_H_MM - 2 * MARGIN_MM
    cols = int(math.floor((usable_w_mm + SPACING_MM) / (CARD_W_MM + SPACING_MM)))
    rows = int(math.floor((usable_h_mm + SPACING_MM) / (CARD_H_MM + SPACING_MM)))
    cols = max(1, cols)
    rows = max(1, rows)
    return cols, rows

def main():
    imgs = list_pngs(SRC_DIR)
    if not imgs:
        print("No PNG files found in src/")
        return

    cols, rows = compute_grid()
    per_page = cols * rows

    ts = str(int(time.time() * 1000))
    out_path = os.path.join(OUT_DIR, f"{ts}.pdf")
    c = canvas.Canvas(out_path, pagesize=A4)

    start_x = MARGIN_PT
    start_y = PAGE_H_PT - MARGIN_PT - CARD_H_PT  # top-left card y (reportlab origin bottom-left)

    idx = 0
    for i, img_path in enumerate(imgs):
        page_idx = idx // per_page
        pos_in_page = idx % per_page
        col = pos_in_page % cols
        row = pos_in_page // cols

        x = start_x + col * (CARD_W_PT + SPACING_PT)
        y = start_y - row * (CARD_H_PT + SPACING_PT)

        bio = prepare_image(img_path)
        img_reader = ImageReader(bio)
        c.drawImage(img_reader, x, y, width=CARD_W_PT, height=CARD_H_PT, preserveAspectRatio=True, mask='auto')

        idx += 1
        # new page if filled
        if idx % per_page == 0 and idx < len(imgs):
            c.showPage()

    c.save()
    print(out_path)

if __name__ == "__main__":
    main()
