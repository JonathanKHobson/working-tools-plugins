# Audio perception, comparison, recorded design and synthesis

Use this branch for choosing or comparing sounds, inspecting a soundtrack,
creating procedural effects, fitting source sounds, or producing a licensed
recorded soundtrack. The audio owner remains Mix Video Audio. Instructional
Design owns learning outcomes and an audio lesson's learner task; Graphic owns
motion art direction and Video owns temporal audio integration and delivery.

## Read the governing adapter before source commands

The complete incorporated methods and their helpers are available locally.
Read the matching full procedure, then its relevant complete references,
templates, examples and helper contract. A routing paragraph does not replace
those methods. The current user request, actual host capabilities and this
execution adapter govern historical setup commands and restrictive creative
defaults. Do not execute upstream installation, MCP registration, model-fetch,
hosted-upload or arbitrary-Python commands merely because a source shows them.

- [Complete Earshot method](../../../libraries/earshot/skills/earshot/SKILL.md):
  asset selection, timeline/mix review, controlled A/B, procedural forge and
  soundtrack kit production, including calibration and Goodhart limitations.
- [Complete recorded-sound method](../../../libraries/earshot/skills/real-sound/SKILL.md):
  cue list, brief, source/license review, music arrangement, deterministic design,
  solo/integrated QA, critic variants, one fixer, mastering, credits and mux.
  Preserve its entire support subtree. Its recorded-only and launch-film
  choices apply when selected by the brief, rather than overriding a requested
  synthesized sound or defining universal lesson/audio loudness targets.
- [Synthesis bank](../../../libraries/earshot/docs/SFX.md),
  [fit production](../../../libraries/earshot/docs/FIT.md),
  [forge](../../../libraries/earshot/docs/FORGE_V2.md),
  [limitations](../../../libraries/earshot/docs/LIMITS.md) and
  [integration](../../../libraries/earshot/docs/INTEGRATION.md)
  retain their full implementation and examples. Source tests and calibration
  evidence are included; their historical results are not current host tests.

## Guarded local execution

Use [earshot_adapter.py](../../../scripts/earshot_adapter.py) from a separately
reviewed Python environment. It contains no installer or provider configuration.
Declare an existing task workspace and its scratch subdirectory, preferably on
the user's chosen bulk-storage volume. Verify that destination before rendering.

```text
python /plugin/scripts/earshot_adapter.py sfx-list --workspace /task --scratch /task/work/earshot
python /plugin/scripts/earshot_adapter.py measure --workspace /task --scratch /task/work/earshot --input /task/short.wav
python /plugin/scripts/earshot_adapter.py sfx-render --workspace /task --scratch /task/work/earshot --sound pluck/kalimba --output /task/output/kalimba.wav
python /plugin/scripts/earshot_adapter.py kit-render --workspace /task --scratch /task/work/earshot --input /task/audio/kit.json --output /task/output/new-kit
```

Substitute the actual plugin and task paths as structured arguments. `--plan`
prints the exact plan without importing Earshot. Commands are a fixed allowlist;
there is no arbitrary passthrough. Media and writes remain inside the declared
task. Write destinations must be fresh, preserving prior output. Symlinks are
resolved before scope checks. The process uses isolated Python, offline flags,
reviewed model revision pins, two CPU threads and a 180-second timeout. Provider
keys, custom model/bank overrides and proxy variables are not inherited. This
is an execution policy, not an OS memory or network sandbox. Start with a short
known PCM file and bounded outputs; long decoding still consumes resources.

`describe`, `match`, `find`, `compare`, `ab`, `realness` and `timeline` require `--cached-models`
after the required default pinned safetensors were separately reviewed and
placed in the task's `scratch/earshot/hf` cache. This flag never downloads or
enables a legacy pickle fallback. Missing dependencies or weights remain an
explicit execution gap; do not install or fetch them to hide the gap. `measure`,
`sfx-list`, `sfx-render` and `kit-render/check` do not need model weights.

The complete recorded-design helpers remain executable at
`libraries/earshot/skills/real-sound/scripts/` with their documented isolated
interpreter invocation. Read the selected helper before use and scope all
inputs/outputs to the task. Analyze, arrange, mix, master, QA, credit and mux
are real retained implementations, not replacements with checklists. Disable
`audit --fetch` for unreviewed manifests; its optional URL byte comparison needs
validated HTTPS destinations/redirects and is separate from license judgment.
Use critic variants before `variant --apply`; the latter rewrites the source
design after backing it up. Preserve the original source and existing stems.

For A/B use `--input` and `--second`, with an optional `--query` or repeated
`--reference` files. `compare` takes `--input` and repeated `--reference` files.
Use explicit preselected media excerpts when trim boundaries matter.

For perception functions not yet exposed by this narrow adapter (such as
sheets and critic profiles), extend its reviewed argument
contract and policy tests before execution. Complete procedures and source are
retained, so this is an execution boundary rather than a separate method-install
requirement. No Earshot MCP, persistent process, API or credential configuration
is installed by this integration. Hosted `llm` is held for a separately authorized
recording upload. Python recipe files execute code; review them as code before
using fit/forge, even if generated by an agent.

## Acceptance and interpretation

Keep source/trim IDs, matching queries, reference identities, unchanged comparison
conditions, actual hashes and the method/model revision with findings. Separate
signal measurements, inferred semantic labels, model preferences and actual
listening review. An agent with real audio access may use it; Earshot does not
become a mandatory proof for every statement about sound. A model transcript is
not a human listening receipt. Respect explicit quiet testing.

Inspect beginning, joins, strongest effects and tail; listen to the allowed final
render, and measure its encoded output with the existing audio/QA owners. In A/B
selection, match excerpt boundaries and playback levels, preserve intentional
dynamics, and change one consequential variable at a time. Scores from different
lengths, descriptions or reference sets may not be comparable. Realness does not
prove recording origin or consent; high optimizer scores do not establish
human preference. Retain blind, level-matched human comparison for claims that
generated sound equals recorded quality. Source licenses and attribution must
follow the exact recording or derived fit, with distinct output rights.

For a lesson, reconcile delivered words with the approved script, pronunciation,
pauses, instructions, references and transcript. Include an actual practice or
reflection action with feedback. Preserve narration, music/effects and combined
stems, and report technically checked, listened, learner-rehearsed and delivered
states separately. A passing loudness meter does not establish learning.

## Provenance and local verification

Source is Leonxlnx/earshot commit
`925ebe56a1b755e5d354ab642bb8f344440cfa9c` (MIT). All 259 supplied files are
retained byte-for-byte, including both full methods, support, runtime, tests and
notices. [Admission record](../../../libraries/earshot/ADMISSION.md) and
[file dispositions](../../../libraries/earshot/UPSTREAM-INVENTORY.json)
identify the exact closure and distinguish host adaptation from upstream code.

Run `python -B -m unittest discover -s tests -p test_earshot_adapter.py -v`
from the plugin root for policy tests. These tests import only the new adapter;
they do not execute or certify upstream audio/model code. A runtime smoke and
listening review need separate actual evidence.
