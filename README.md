# Printing Card Formatter

Printing Card Formatter helps you quickly produce print-ready PDFs of your custom TCG cards.

The script automates arranging card images into a PDF using the standard TCG card dimensions (63.5 mm × 88 mm), removing the manual trial-and-error usually required when preparing many cards for print.

**Overview**

- **Purpose:** Place all card images you want to print into the `src` folder and run the script. The script generates a PDF laid out for printing, with each card sized to 63.5 mm × 88 mm.
- **Why:** Preparing many trading-card-style images for print is normally manual and error-prone. This tool streamlines that workflow.

**Features**

- Automatically sizes images to standard TCG card dimensions.
- Produces a single PDF ready for printing.
- Minimal setup: requires Python and the listed dependencies.

**Requirements**

- Python 3.8+ (or your system Python 3)
- See `requirements.txt` for required Python packages. Install with:

```bash
python3 -m pip install -r requirements.txt
```

**Quickstart**

1. Put all card images you want to print into the `src` directory. Supported formats: PNG, JPG, JPEG.
2. Run the generator:

```bash
python3 generate_pdf.py
```

3. The script will create an output PDF (usually `output.pdf` or as configured in the script). Open it in a PDF viewer and print on your preferred paper size.

**Image recommendations**

- Use high-resolution images (300 DPI recommended) to keep text and details sharp when printed.
- Ensure images are already cropped to the artwork you want on the card (the script will scale/crop to fit the target card size).
- Consistent aspect ratio close to TCG cards (63.5 mm × 88 mm) gives the best results.

**Card dimensions & bleed**

- The script targets the standard TCG dimension: 63.5 mm × 88 mm.
- If you need bleed or crop marks, edit `generate_pdf.py` to add margins or change page layout. See the script header for configurable constants.

**Customization**

- Page size, margins, and how many cards per page may be configured in `generate_pdf.py`.
- If you want a different paper size (e.g., US Letter) or a custom grid, edit the page settings in the script.

**Troubleshooting**

- If images appear blurry, use higher-resolution source images (300 DPI recommended).
- If cards are misaligned on the printed page, check your printer's scaling settings — set scaling to 100% or "Actual Size".

**License & Contribution**

- This project is provided as-is. Feel free to open an issue or submit a pull request with improvements (e.g., add bleed support or alternate layouts).

---

For quick help, run `python3 generate_pdf.py --help` (if the script supports arguments), or inspect the top of `generate_pdf.py` for configuration options.
