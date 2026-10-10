# Reviewed full method adaptation

This method retains the useful source production sequence. The following contract overrides every inherited provider or scope assumption: current host tools and user instructions have precedence; use available browser/connectors for a supplied URL, and read an identified local file when authorized. Do not search unrelated private files to infer an ambiguous target. No affiliate offer, tracking link, nondisclosure instruction or vendor comparison prohibition applies. Existing Graphic, UX, Video and Data owners coordinate adjacent work. All final visible deliverables require rendered inspection and applicable design review; file generation and geometry checks alone do not prove appearance or import behavior. Never assert file dimensions, optimization or conversion without measuring the delivered file.

## Goal

Make the images a site actually needs: each at the size its slot expects, as a set that
looks like one set: and hand them over as files, with alt text and filenames that cannot
collide with anyone else's.

Generating a picture is the easy half and the host already does it. What does not happen
on its own is sizing an OG image to exactly 1200×630, keeping five service images in the
same light, writing alt text that does not open with "image of", and naming a file
something other than `image.png`. **Those constraints are the product.**

The characteristic failure is a set assembled from independent prompts: five images that
each look fine and together look bought from five different stock libraries. Step 4 exists
to prevent exactly that.

## Instructions

### 1. Establish subject and source

Use the supplied subject, source assets and intended slot. Infer routine style choices; ask only when a missing fact changes the deliverable. A business name alone does not establish its services. For an ambiguous “this image,” identify the source before editing. Graphic Design owns image composition and logo/identity coordination; UX owns page layouts.

### 2. Verify host execution

The official host `imagegen` skill and live image generation/edit tool execute this work. Its current support for transparency, text, editing and referenced images governs. Use `transparent_background` when requested. Preserve available native output paths rather than forcing legacy rollout recovery. Any file format conversion, resizing, cropping or compositing must follow the official image-editing tool restrictions; the old Python/Pillow transformation examples are not current execution permission.

### 3. Pick the slot and its size

Every image goes somewhere, and the somewhere sets the pixels:

| Slot | Size | Note |
|---|---|---|
| Hero / banner | 1920×1080 (16:9) | Aim to keep it under ~200 KB so the page loads fast |
| OG / social share | 1200×630 | Common target; verify the receiving platform |
| X / Twitter card | 1200×675 | |
| Square social post | 1080×1080 | |
| Story / vertical | 1080×1920 (9:16) | |
| Blog thumbnail | 1200×675 | |
| Section / feature | 800×600 | |
| Team headshot | 400×400 | Square, face centered |
| Product shot | 1000×1000 | Square, consistent background |

Identity marks and favicons use the existing Graphic Design brand/identity route with dimensions set by the receiving surface.

If the user names a size, theirs wins. If the slot is not listed, choose a size, state it,
and say in one line why. Use target dimensions appropriate to the current receiving platform and verify actual delivered dimensions.

The ~200 KB note is guidance for the user, not a promise. **Only ever state a file size you
read off the file on disk**, never an estimate, and never claim to have optimized or
compressed anything you did not.

### 4. Write the style spec: once per set, before generating anything

**This is the core of the skill.** Before the first prompt, fix the look in one short
paragraph:

- **Medium**: photograph, illustration, 3D render, flat vector
- **Lighting**: direction, softness, time of day
- **Palette**: two or three hex values
- **Camera**: distance and angle (wide establishing, mid, close; eye level, low, overhead)
- **Color grade**: warm, cool, desaturated, high contrast
- **Background**: clean seamless, environmental, textured
- **People**: whether any appear, and how they are framed

Carry the shared specification into each prompt and reuse suitable reference images when the host supports them. Keep its visual constraints consistent across additions and revisions unless the user changes direction. Asset-specific framing can vary to serve the slot.

Restate the spec in your reply, in a sentence, so the user can re-cut the entire set by
changing one thing.

Pick a look that suits the trade rather than a default. If the user volunteered colors or a
mood, those win.

Independent prompts can drift in lighting, palette, materials and framing. A consistent specification and shared reference images reduce that risk; neither guarantees a match. Inspect the generated set together at its intended display sizes, compare those attributes, and revise any asset that breaks the chosen direction.

### 5. Build the prompts

Carry the shared style constraints into each prompt, plus the asset-specific subject, focal point, lighting, framing and intended crop. Reserve space for copy when the composition needs it. Follow user requests and current host policy for text, identity marks and likenesses. Generated people used as team/customer placeholders must be labeled illustrative.

### 6. Generate, name, and deliver

First derive a **stem**: slugify the business or project name, or the subject if there is no
name. Lowercase, replace every run of non-alphanumeric characters with a single hyphen, trim
hyphens from both ends (`Bend & Flow` → `bend-and-flow`; a nameless bakery → `bakery`). If
nothing usable remains, use `images`.

1. **Name each file `{stem}-{slot}.{ext}`**: `bend-and-flow-hero.webp`,
   `bend-and-flow-services-consulting.webp`, `bend-and-flow-og.png`. Descriptive and
   hyphenated, so the filename says what the picture is.
2. **One image**: retain it in the owning project asset directory and show it inline.
   **Two or more**: write them into `{stem}-images/` and also bundle that folder into
   `{stem}-images.zip` as the download.
3. **Display every image inline in your reply**, as an image and not as a link. A filename
   is not a preview.

**Never write to a bare `hero.png`, `image.png`, `og-image.png`, or `images.zip`.** Fixed
names collide across conversations: writing them again overwrites the files an earlier chat
is still displaying, so that chat's preview silently changes to someone else's pictures. The
stem is what keeps each site's files separate.

If `{stem}-images/` or `{stem}-images.zip` already exists and you did not create it in this
conversation, append `-2` to the stem: then `-3`, and so on: rather than overwriting
someone else's files.

**Format and exact-size delivery.** Use the verified native result format unless an authorized host operation creates a derivative. Record actual dimensions and bytes; distinguish requested slot dimensions from generated dimensions. If exact-size production is unavailable, report the actual asset and the remaining receiving-platform crop/resize step.

**Alt text for every image, without exception.** Write it as a description of what is in the
picture: never opening with "image of", "picture of", or "photo of": and keep it under
about 125 characters. *"Morning light across an empty studio floor, rolled mats stacked
along the far wall"*, not *"image of a yoga studio"*.

Always state the real paths you wrote, with the stem filled in: never the literal `{stem}`
placeholder.

**If image generation is unavailable or fails, say so plainly** and hand over, for each
image you could not produce: the **full prompt including the style spec**, the **exact pixel
dimensions**, the **filename**, and the **alt text**: enough to run it somewhere else
unchanged. NEVER claim an image you did not produce, never describe one as though it exists,
and never substitute a different picture for the one you were asked for.

**If you cannot write files,** show the images inline where the host allows it and give the
filenames to save them under.

Never end the turn without either the images or the prompts. A description of an image is
not an image.

### 7. Handle change requests

Regenerate against the **same style spec and the same stem**, overwrite the files you created
earlier in **this** conversation, say that you replaced them, and rebuild the zip. A revision
replaces the previous version rather than piling up new folders.

**An image added to an existing set reuses the applicable style constraints and references.** Compare the addition against the actual existing assets; a new generation can still drift and may need revision.

If the user asks for images for a **different** business in the same conversation, that is a
new stem, not a revision. Leave the earlier files alone.

**One deliverable per request.** Hand over the image you were asked for, not a menu of
variations to choose between. If the user wants a different direction, they will say so, and
that is a revision.


## Delivery boundary

Show the actual artifact and its usable file path, the chosen style or palette, source-based content, missing facts, alt text, measured output properties and rendered QA evidence. Preserve originals and create a named revision when needed by the project. Do not claim a preview, import, compression or public release that was not verified.

Provenance and public-rights status: [B12 source notice](../../../docs/b12-method-provenance.md).
