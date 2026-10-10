# Renderer Adapter Contract

A renderer adapter consumes either the full manifest or an isolated animation-slot manifest and writes normalized media plus evidence.

## Inputs

- absolute manifest/slot path;
- output path and work/cache directory;
- dimensions, frame rate, duration, color and alpha requirements;
- resolved asset map and hashes;
- quality level and deterministic seed when relevant.

## Outputs

- rendered media;
- probe JSON;
- render log with command, tool/runtime versions, input/cache hash, warnings, elapsed time;
- representative frames or contact sheet;
- explicit alpha/color metadata and any exceptions.

## Normalization

Final slot assets must declare dimensions, frame rate, time base, codec, pixel format, alpha mode, color space/transfer/primaries, duration, and audio presence. Editorial timing stays in the core manifest; an adapter must not silently shift duration or add handles.

## Failure behavior

Exit nonzero, preserve logs and partial evidence, never overwrite sources, and distinguish missing dependency, invalid manifest, renderer failure, timeout, and validation failure.
