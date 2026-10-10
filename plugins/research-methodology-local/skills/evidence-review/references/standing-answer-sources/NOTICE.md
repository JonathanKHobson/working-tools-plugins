# Attribution and adaptation boundary

Informed by Vectorize AI, Inc., Hindsight, MIT licensed, revision `017b3f5d888d67341e70f43c102cb8155bb9f51e`.

- [Mental-model method](https://github.com/vectorize-io/hindsight/blob/017b3f5d888d67341e70f43c102cb8155bb9f51e/hindsight-docs/docs/developer/mental-models.mdx): curated question, scoped change detection, stale-answer fallback, version/evidence history (lines 10–64).
- [Retraction handling](https://github.com/vectorize-io/hindsight/blob/017b3f5d888d67341e70f43c102cb8155bb9f51e/hindsight-api-slim/hindsight_api/engine/reflect/retractions.py): typed grounding, all-ID loss as potentially broken mapping rather than evidence of retraction (lines 1–84).

`standing-answer-freshness.md` is an original manual adaptation: it uses the already owned project document/source register, claim-level dependencies and explicit review. It excludes upstream automatic consolidation, memory retention, paid/local inference, background refresh, cloud storage, model/runtime installers, MCP tooling and SDK code. The upstream “always current” language is not carried over as a local guarantee. No Glean or Repolyze material is copied into this adaptation. The only copied upstream file here is the unchanged MIT license, retained in LICENSE. Source hashes are recorded in source-map.json.
