# Platform Delivery Research Policy

Platform constraints, upload encoders, product UI, safe zones, and recommended practices change. Store them as versioned data with:

- platform and surface;
- official source URL;
- reviewed date;
- account/product context (organic, ad, feed, story, reel, short, presentation, etc.);
- min/max duration, dimensions, aspect, frame rate, container, codec, bitrate/size, audio, captions;
- UI overlay screenshot or safe-zone overlay at the current product version;
- confidence and exceptions.

## Stable-ish defaults, not guarantees

- Preserve native frame rate unless deliberate conversion is needed.
- Use square pixels and broadly compatible pixel formats for consumer platforms.
- H.264/AAC MP4 is a compatibility baseline, not an archival master.
- Use fast-start for web delivery.
- Recompose vertical/square content; do not only crop.
- Keep captions as sidecars where supported and a burn-in variant where useful.
- Retain a higher-quality master independent of upload variants.

Before delivery, re-open the official source and compare the current product UI. Never let a skill’s remembered number override current official documentation or actual upload validation.
