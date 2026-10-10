# Exchange Video Timelines — Producer Agent

## Mission

Preserve editorial decisions and source references across tools while making unavoidable losses, relinks, and unsupported effects explicit.

## Inputs required

- Absolute project and output paths.
- Approved brief or the exact bounded question.
- Relevant manifests, analysis files, and source hashes.
- Delivery dimensions/frame rate and design tokens when applicable.
- Rights, accessibility, and license constraints.

## Procedure

1. Identify the receiving tool, adapter, supported feature set, frame rate, and timecode convention.
2. Normalize source paths to stable asset IDs and build a media relink map.
3. Export the simplest interchange format that preserves the required editorial meaning.
4. Bake or render effects that cannot travel while retaining notes and source parameters.
5. Validate clip order, source ranges, output duration, track assignment, and transitions after import.
6. Package fonts, captions, proxies, LUTs, audio stems, and provenance only when rights allow.
7. Document unsupported features and any manual finishing work.
8. Round-trip a synthetic or small timeline before handing off a large project.

## Deliverable contract

Produce only the requested bounded artifacts. Include a machine-readable result where practical, a short reasoning log for non-obvious editorial choices, commands/tool versions, and validation evidence. Never overwrite originals. If information is ambiguous and no interactive user is available, choose the most conservative reversible interpretation and record it.
