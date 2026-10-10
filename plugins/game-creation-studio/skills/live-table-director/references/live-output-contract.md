# Live Output Contract

The live assistant normally stays under 140 words and returns only:

```text
CLOCK | SCENE | ENERGY | SPOTLIGHT
NOW:
SAY:
ASK:
WATCH:
CUT WHEN:
NEXT:
```

## Field Meanings

- `CLOCK`: hard stop, remaining time, or current timing assumption.
- `SCENE`: current dramatic purpose and pressure.
- `ENERGY`: visible table energy, friction, or uncertainty.
- `SPOTLIGHT`: who has had attention recently and who needs an invitation.
- `NOW`: the single recommended GM move.
- `SAY`: exact speakable language.
- `ASK`: at most one player-facing question, with pass option when personal.
- `WATCH`: one observable signal.
- `CUT WHEN`: concrete stop condition.
- `NEXT`: likely transition.

## Compression Rules

- One intervention, not a menu.
- No theory during live mode.
- No source essay. Use `verify-after-play` when lookup would stall the table.
- If state is incomplete, make one reversible assumption and move.

