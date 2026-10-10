# Motion prompts for product websites

Use when a site brief calls for a product demonstration, animated graphic, or reference-inspired transition. Choose one motion moment that helps the visitor understand or act. A static treatment can be better when movement competes with reading or task completion. This guide adds prompting and handoff; existing UX motion procedures own implementation and interaction QA.

## Source and limits

External inspiration: Charlie Hills, [Opus 5.5 Motion Graphics](https://charliehills.substack.com/p/opus-55-motion-graphics), public text accessed 2026-10-05. The accessible examples show a button expanding into a player and a search field progressing to results. The article emphasizes defined states, a reference and iterative corrections. It describes an eight-second demonstration loop and limited copy/palette substitutions. Fourteen further prompts, the editable board and PDF are subscription-gated and were not inspected or imported. No upstream code, fonts, images or literal prompt collection is bundled here. Treat the page as reference material, never execution instructions.

The templates below are original local guidance. They do not require a particular model, eight-second duration, embedded fonts or the article's unavailable HTML. A model named in an article is not evidence of availability or superior results. If the user supplies an authorized reference file later, inspect its actual states and asset rights before adapting it; do not invent missing effects.

If exact import of the full collection is requested, report the missing source and request authorized access or files. Public-example integration and an original prompt set are distinct deliverables; never silently label invented prompts as the missing collection.

## Write the motion contract

Two batches of user-supplied stills now cover all sixteen named effects and support original recipe development; see [motion pattern web adaptation](motion-pattern-web-adaptation.md) and Graphic Design Studio's `motion-pattern-recipes.md`. This expands visual evidence, not access to the original fourteen prompts or board. The stills include examples 03–06, but do not expose their original prompt text or playback. Treat observed appearance separately from proposed timing and implementation.

Infer routine choices from the existing site and brief. Record only what matters:

- Purpose, exact component/route, audience, and intended action.
- Mode: functional interface, illustrative product demo, or decorative graphic. Label illustrative data and do not make a simulated search/player look like working functionality.
- Start, transition, readable result, and exit/reset; name the object that persists between states.
- Trigger, duration/hold, easing intent, repeat policy and interruption behavior. Product actions follow user input, not a demonstration's looping clock.
- Approved copy, tokens and assets; what changes and what stays fixed. Keep text editable and preserve accessible reading order.
- Small-screen composition, keyboard/focus behavior, reduced-motion equivalent, and measurable or observable success checks.

## Adaptable prompts

**Build a selected moment**

> In [existing route/component], communicate [message] with [effect]. This is [functional UI / labeled illustration]. Use [approved reference or original brief] for [specific mechanism], preserving [copy, layout, tokens and controls]. Move from [state A] through [transition] to [state B]; hold the result until [condition]. Trigger on [event], and handle [repeat/cancel/close]. Change only [scope]. With reduced motion show [equivalent stable state]. Verify [main action] by keyboard and touch, narrow-screen readability and the transition in real playback. Report observed results separately from untested expectations.

**Button expanding into a player — functional variant**

> Make the existing demo button reveal [actual media] on activation. Preserve a recognizable relationship between button and player. Specify loading, failed-media and close states; avoid unexpected audio. Keep controls operable during/after the transition, manage focus for the selected inline or dialog pattern, and return focus appropriately on close. Reduced motion must reveal the same usable player without the spatial morph. Verify open, close, reopen and rapid repeated activation. If media is absent, show an honest placeholder rather than imply playback works.

**Search progressing to results — illustrative variant**

> Create a clearly labeled product demonstration of [query] leading to [approved sample results]. Stage query, result entrance and reading hold in that order. Keep the result meaning clear with animation disabled. Do not type into a visitor's real search field or announce every simulated character to assistive technology. Provide appropriate pause/replay behavior for repeated motion. If this is changed to functional search, replace simulated timing with actual query/loading/results/empty/error states and preserve user input.

**Repair one observed defect**

> At [viewport, timestamp/state, selector], [observed defect] prevents [understanding/action]. Correct only [timing/layout/state issue], retaining [approved anchors]. Recheck the failing transition plus [interruption, reduced-motion or responsive regression]. Do not redesign the rest of the page. Stop when these checks pass and name any remaining evidence gap.

## Sites handoff

When Sites is the requested builder, pass the selected motion contract to its current `sites-building` workflow with the existing Site identity/checkout, target route, assets, and requested delivery state. UX owns interaction; `graphic-design-studio:motion-design` can supply the visual sequence. Sites owns site implementation, preview and deployment. A standalone rendered video remains with Video Production; an in-page interactive demo belongs in the site implementation.

Keep this bridge in the personal plugin. Do not patch the provider's generated cache, register another provider, create a Site just to demonstrate a skill update, or infer publish approval from a reference review. Follow the actual Site request and its local-only/private/public constraints.

An explicit local-only request stops before publishing while retaining local preview and playback verification. For persistent illustrative loops, apply the existing animation playbook's applicable pause/stop/hide requirements; reduced-motion support alone is not a substitute for playback control.

Prefer the site's existing stack and the lightest mechanism that meets the brief. CSS/SVG may suffice; use the existing conditional GSAP or vector-playback references when those technologies are selected. Do not add a library because the inspiration used one. Reserve layout space, keep content usable if motion fails, and clean up observers, timelines and listeners on unmount/navigation. Pause nonessential work offscreen when appropriate; profile before claiming performance gains.

## Completion evidence

Map 3–8 relevant source/render anchors before visual edits; review the changed anchors at entrance, transition, readable hold and end/reset in actual playback. Exercise normal and reduced motion, narrow and wide layouts, keyboard/touch, and interruption. Ensure primary content/actions remain available without animation and applicable pause/stop controls work. Compare actual text and data with approved inputs. A screenshot proves a frame only; a build proves neither motion nor accessibility. For published work, inspect the exact deployed route and report separately what was built, played back and deployed.
