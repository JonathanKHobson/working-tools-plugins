# Generated character acting from coherent sprite sequences

Use this branch when a character must blink, change expression, gesture, walk,
handle an object or move between states. Start from the existing storyboard and
[generated-assets contract](generated-assets-for-motion.md). Keep the editorial
manifest and selected visual identity. A small registered action is the first
acceptance test before a large batch.

## Director and asset maker

For the Claude/Codex production route, Claude is the animation director and
assembler; Codex makes raster assets with built-in imagegen. Use the requested
Claude model when live availability verifies it, and record the actual returned
model. Keep provider/version choices in the project, not a plugin dependency.
The director supplies a detailed storyboard, timed action breakdown and exact
sprite requests; the asset maker returns saved referenced sequences and measured
geometry. The director reviews them, requests bounded corrections and assembles
the accepted poses into the video. A text-only review cannot certify visual
motion; supply inspected frames and playable evidence to the reviewer.

For each shot, specify: purpose, duration, output rate, character/reference ID,
viewpoint, body proportions, shared scale, registration point, ground baseline,
contact anchors, entry pose, exit pose and transition to the next shot. Name every
needed action explicitly, including blinks, expression changes, limb movement,
pick-up, hold and release. A missing drawing is an asset gap, not permission to
simulate its acting by stretching legs, replacing limbs with procedural shapes,
warping a cutout or translating a static sprite across the screen.

## Request and account for the acting

Use a compact pose ledger within the existing shot manifest. Each entry needs a
stable pose ID, action phase, visible whole-body pose, expression/eyelids, limb
positions, prop/contact relationship, reference hashes, exact output-frame range
and reason for its timing. Ranges cover every output frame once, with no gaps or
overlaps. Distinguish generated unique poses, intentional holds and encoded frames.
A 24fps file alone says nothing about fluid acting. Choose the pose cadence for
the action, render it and add in-betweens where playback shows a snap. Do not
advertise a deliberately held pose study as continuous full-frame animation.

Account for anticipation, action, contact, follow-through, recovery and the next
entry pose. For a pick-up: establish the object's resting location, hand approach,
first contact, grip closure, lift, held weight and settling. For release: open the
grip, separate hand and object, preserve the object's trajectory, show destination
contact and hand recovery. Name occlusion order and anchors at each change. A prop
must not teleport, swap hands, change size or pass through the body. Request missing
contact drawings from imagegen rather than manufacturing new anatomy in the renderer.

Approve one canonical character image first. Ground every later state/action strip
in that canonical image and every identity-defining reference. Include a guide
when useful, but reject visible guide marks. Request one coherent state/action per
strip with an explicit pose count, ordered acting, generous separation, complete
silhouettes, crop-safe margins, stable lighting/material and removable background.
Never ask for an entire multi-state atlas in one generation. Approve idle/blink
and a directional or gesture action early to catch identity and proportion drift.

A reusable request follows this pattern:

> Using the attached canonical character and approved entry pose, produce one
> coherent strip of N complete poses in the ledger order. Preserve face, head/body
> ratio, limb length, material, palette, handedness, prop identity and camera.
> Follow the specified anticipation, action, contact and recovery poses. Keep the
> resting ground baseline and apparent scale consistent; preserve intentional
> airborne displacement. Separate complete pose groups on clean transparency or
> the selected contrasting chroma key. No labels, guides, scenery, detached effects,
> trails or shadows that would merge with another pose. Return the source strip.

## Extract and register generated pixels

Inspect actual connected pose groups and source alpha bounds before extraction.
Generated spacing is not a reliable grid. Do not blindly divide a strip into equal
slots. Record group bounds, attach detached but intentional parts by explicit
reviewed assignment, and reject missing, merged, clipped or extra poses. Preserve
left-to-right temporal order. A mirrored directional variant is valid only when
markings, lighting, handedness and props permit it; mirror each pose in place,
never the whole strip with reversed time.

Fit all approved poses with one shared scale and a stable body/ground reference.
Do not independently resize each silhouette to fill its cell. Register body and
contact landmarks rather than assuming alpha-bounds centers are joint anchors.
Preserve vertical jump displacement and arcs; grounding every airborne pose erases
the action. Preserve face/body ratios and short limbs through every extreme pose.
Keep extraction rectangles and transforms bound to the source hash.

Prefer native transparency. If chroma is needed, choose a key absent from the
character, remove it, then perform a single edge-local despill pass after assembly.
Preserve antialiased alpha and opaque interiors; clear hidden RGB under zero alpha.
Inspect edges and holes over light, dark and contrasting backgrounds. Do not invent
missing artwork while cleaning alpha. Correct extraction/registration deterministically
when the source is sound; regenerate the smallest coherent strip when acting or
identity is wrong. After two recurrences of one failure, change the anchors,
pose instructions, extraction strategy or prop complexity rather than repeating it.

## Preview and verify

Review the exact final registered pixels and encoded clip at intended display size:

- Labeled contact sheet and at least four timestamped output stills.
- Each state/action loop at its intended cadence, with frame ranges and holds.
- Dedicated entry-action-exit transition, including idle-to-jump-to-idle when relevant.
- Prop contact/release and the hardest occlusion at playback speed and frame stepping.
- Light/dark/contrasting alpha composites, checked for fringe, clipping and holes.

Record 3–8 visual anchors before signoff: ID, source/hash and output time/region,
observed fact, intended check/correction and post-correction verdict. Check identity,
body proportions, baseline, scale, limb continuity, gaze/expression meaning, direction,
contact/weight, anticipation/follow-through and transition continuity. Structural
validation cannot approve those semantics. Reject wrong directions, broken attachments,
teleportation, conspicuous pops and static acting presented as fluid motion. Recheck
changed anchors after each correction. Review final compressed video separately.

The portable `scripts/preview_sprite_sequence.py` entrypoint validates an explicit
pose/hold manifest and renders review evidence from already extracted, registered
RGBA poses. Run `--help` for its current interface. Its timing/hash/geometry checks
are mechanical evidence only; they do not approve extraction, acting or identity.
Use the existing renderer for the final edit and `validate-video-quality` for signoff.

## Provenance and boundaries

This is an original method adaptation informed by the installed Pets v0.1.6
`create-pet` procedure and its shared sprite-sheet contract, reviewed 2026-10-26.
The transferable ideas are canonical-reference identity, coherent state strips,
shared registration, connected-pose extraction, alpha cleanup, movement/transition
previews and semantic visual QA. No Pets code, art or text is vendored here; no
redistribution grant is inferred for that upstream package. First-party additions
use this plugin's existing file-scoped licensing. Keep generator, prompt, source
reference/hash, accepted/rejected status, source-strip hash, extraction map,
registration, timing ledger, output hashes and review evidence in the project.
Generated artwork does not establish rights to an input character or trademark.

This generic workflow does not require Pets to be installed. Pets' atlas sizes,
nine lifecycle states, sixteen look directions, Library artifacts, validators,
upload sessions, creation/update/select APIs and activation rules remain with
Pets. Do not import those lifecycle requirements into a film or alter the installed
plugin. No new catalog, provider, hook, permission, publication or scheduling is added.
