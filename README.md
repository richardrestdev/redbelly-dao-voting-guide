# Redbelly DAO voting guide

## Deliverables

1. **The guide (web page):** `index.html`. Open it in a browser, or host this whole folder as it is. It needs `assets/` and `diagrams/` next to it.
2. **The diagrams as images:** `diagrams/1-verification-to-vote.png` and `.svg`, `diagrams/2-eligibility-snapshot.png` and `.svg`. Both are placed in the guide (Fig 1 and Fig 2), and each figure links to its image files. Each diagram also has a portrait version for phones (`-mobile` in the file name), which the guide shows on screens up to 900px wide. The SVGs are animated and play when opened in a browser. The PNGs are still frames.
3. **Editable source of the diagrams:** `diagrams/source/*.svg`, plain SVG that opens in Figma, Inkscape, Illustrator or a text editor. Editors that ignore animation still show the complete diagram. The SVGs are written by `src/make_diagrams.py`, so positions, text and timing can also be changed there.

`assets/` holds the Redbelly DAO logos and the favicon from the Redbelly DAO brand kit.

## Fact check

`VERIFICATION.md` lists every rule in the guide with its source, and the commands to check it again.

## Rebuilding

    python3 src/make_diagrams.py
    python3 src/build.py

`src/index.src.html` is the page source. `build.py` places the diagrams into it and writes `index.html`.

Fonts: Be Vietnam Pro, with JetBrains Mono for machine values, both from Google Fonts.
