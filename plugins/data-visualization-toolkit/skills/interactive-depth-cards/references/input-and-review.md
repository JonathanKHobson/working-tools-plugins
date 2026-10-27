# Input and review

This is an independent local implementation. It accepts the earlier layer brief and adds collectible-card motion, finish, flip, and exploded-layer controls. It is not a byte-preserved copy of the source package. The comparison record for the staged reference is held outside this plugin's distributable tree.

## Brief

Paths resolve relative to the JSON brief. Supply one to five PNG, JPEG or WebP files. Image files are decoded, oriented and re-encoded to strip EXIF and text metadata before embedding; an embedded color profile is retained for color fidelity. Limits: 12 MiB per file, 24 megapixels per image, 30 MiB combined embedded images, 256 KiB brief. Alpha is retained for PNG/WebP layers. Remote URLs, SVG and animated inputs are rejected.

```json
{
  "title": "A layered view of the habitat",
  "subtitle": "Illustrative scene",
  "body": "Move the pointer or use the arrow keys to inspect the layers.",
  "layers": [
    {"path": "background.png", "alt": "Distant hills", "depth": 8, "role": "background"},
    {"path": "foreground.png", "alt": "A tree in the foreground", "depth": 45, "role": "foreground"}
  ],
  "card_depth": 70,
  "finish": "holographic",
  "foil": true,
  "auto_rotate": false,
  "exploded": false,
  "back": {"title": "Reverse title", "body": "Reverse description"},
  "card_text": ["Edition one", "Ability: supplied wording"],
  "sparkles": 12,
  "facts": [{"label": "Scene type", "value": "Illustration", "source": "Supplied artwork"}]
}
```

`title` is required (1–100 characters); subtitle up to 180, body up to 700. Alt text is required for every image (up to 240 characters; empty only for decorative layers). Per-layer `depth` is a finite number from 0 to 48 CSS pixels; optional `role` is `background`, `foreground`, or `particles`. Omitted roles keep old briefs working: first layer is background, later layers foreground. `card_depth` is a finite 0–100 strength applied once to input motion, default 70. Zero neutralizes input-driven rotation, XY displacement, lift and light movement; the fixed layer Z order remains as part of the card's static composition. `finish` is `holographic`, `gold`, or `silver`; default holographic. `foil`, `auto_rotate`, and `exploded` are booleans. `back` is optional live reverse-face text; if omitted, no flip control appears. `card_text` adds up to four supplied live lines to the moving print plane. `sparkles` adds 0–24 decorative local CSS particles; it defaults to zero and stops twinkling under reduced motion. Optional facts: up to four label/value/source records, each required and nonempty. No measurements, statements, offer details or sources are invented by the helper.

## Execution

```sh
python3 scripts/build_depth_card.py --brief /absolute/brief.json --output /absolute/card.html
```

The Python script reads only the supplied brief, referenced images and its adjacent template. It writes only the specified output. No background process, environment credential, remote provider or telemetry is involved. Keep the source brief and assets in the owning project; the generated HTML carries embedded copies and can be moved independently.

## Review contract

| Anchor | Expected observation | Check |
| --- | --- | --- |
| Message | Title and body are readable without interaction | Script-disabled preview and 360px width |
| Scene | Background, subject and print move distinctly | Neutral, maximum tilt, reset and exploded view |
| Subject edge | No accidental frame gap or clipped critical subject | All four tilt extremes |
| Controls | Arrow keys tilt; Home/Escape/0 reset; Enter/Space flips when a back exists | Actual keys, focus indicator, announced pressed states |
| Motion preference | Reduced motion stops tilt and orbit; flip and layer changes remain immediate | Start reduced and change preference during use |
| Depth and light | 0 neutralizes input rotation, displacement, lift and light position; 50 is half of 100 | Pointer extremes at 0/50/100; foil and finish changes |
| Touch | Vertical scrolling works; drag does not flip; tap can flip | Touch drag, tap, cancellation and pointer capture |
| Lifecycle | Motion settles and stops when hidden | Observe frames after reset and visibility change |
| Static output | Facts remain flat/readable and print remains static | Print media and script-disabled preview |

The print inside the card moves modestly as live text; the explanation and sourced facts below remain flat. The card uses pointer touch with vertical scrolling preserved; it never requests motion-sensor permission. Controls affect this page only and do not save state. Browser support and screen-reader usability need actual target-host testing; automated DOM checks alone do not prove them.
