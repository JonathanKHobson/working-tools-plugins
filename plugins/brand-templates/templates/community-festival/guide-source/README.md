# Common Sun guide source

`render_guide.py` is the editable composition for the two-page pilot guide. It places the production logo PNG exports from `../assets/logos/`, the source-derived 17-ray fan from `../assets/motifs/`, and draws the type, rules, palette, diagrams, and sample applications with ReportLab. The SVG originals are beside the PNGs. The earlier image-generated `common-sun-symbol.png` is a concept source, not the production logo. The seven-ray identity symbol and 17-ray supporting fan have different roles.

From this directory, run `python3 render_guide.py --output ../guide.pdf`. The script writes `../guide.pdf` and page previews in `rendered/`. It requires Python with ReportLab, Pillow, and fontTools, plus `pdftoppm` from Poppler. The layout uses `../assets/fonts/anton/Anton-Regular.ttf` and `../assets/fonts/arimo/Arimo-{Regular,Bold}.woff2`; converted Arimo TTF files are included here for ReportLab. The font licenses are at `../assets/fonts/anton/OFL.txt` and `../assets/fonts/arimo/OFL.txt`.

The festival name and application copy are fictional brand examples. Palette values and type choices come from the source template and curated Common Sun profile. Minimum logo widths are design recommendations; inspect legibility in each final output.
