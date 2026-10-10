# Generated Asset Workflow

Use generated assets after placement intent is clear.

## Before Generation

Record:

- asset purpose
- target slot or anchor ID
- adjacent claim or UI job
- source status needed
- aspect ratio and crop behavior
- style, tone, palette, and avoid list
- whether people, identity, text, logos, or real-world evidence are involved

## Generation Rules

- Generate `environment`, `atmosphere`, `identity`, and `interface` assets when
  real sources are missing or a designed system is needed.
- Do not generate `evidence` for real events, people, user behavior, gameplay,
  product behavior, or outcomes.
- For people or real-session atmosphere, label generated outputs as
  illustrative if they are public.
- Save the final prompt, model/tool, source inputs, output path, and status in a
  manifest or asset note.
- Follow the current official `imagegen` skill's persistence and output rules.
  A chat preview is not a project asset. For project use, save the selected
  output to a stable path and verify the actual file before placing it.

## Persistence and source check

Use the file returned or saved by the active official image tool. The built-in
`image_gen` tool saves under `$CODEX_HOME/*` by default; for a
project-bound asset, copy or move the selected output into the project under a
stable name, keeping approved originals intact. Verify that the project file
exists, is non-empty, has the expected image dimensions, and opens visually
before editing, deriving, placing, or claiming delivery. Do not infer a usable
file from an inline preview or invent an output path.

If the built-in tool provides no recoverable output file, report the missing
artifact and follow the official skill's supported path. Do not substitute a
screen capture, copied chat preview, unrelated web image, vector placeholder,
or prompt-only claim for a requested raster asset.

## Cutout workflows

- Use cutouts for icons, portraits, props, badges, and UI assets when they need
  to sit on varied backgrounds.
- Generate one icon/cutout per image. Do not generate a sheet of multiple icons
  when the final assets need clean individual crops.
- Ask the built-in `image_gen` tool for a transparent background using its
  `transparent_background: true` option. Preserve and verify the alpha channel
  in the saved output and any derivative.
- Inspect edges at intended rendered size.
- Keep the selected source and any edited derivatives separate.

## Rejection Rules

Reject or rework generated assets when they:

- look fake in a proof slot
- imply a real session, user, product, or outcome that did not happen
- introduce wrong world, product, or brand details
- contain unreadable or incorrect text
- clash with the surrounding visual system
- require captions to explain why they are present
