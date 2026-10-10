# Conditional Three.js product motion

Use this when an existing web product uses Three.js or React Three Fiber for an interactive scene, animated model, product preview or spatial control. First inspect the project's installed Three.js and renderer version, framework, model source and current scene owner. The product's state, focus, reduced-motion and performance requirements still come from the motion-and-performance skill. This method fills the scene lifecycle gap; it does not choose Three.js for a flat UI transition.

## Establish the interaction contract

Record the user action, the visual response, its semantic equivalent and the required settled state. Treat a model preview as content with loading, ready, paused, error and unavailable states. Keep product facts, controls and any call to action in accessible DOM where possible. A canvas-only hotspot needs an equivalent keyboard and assistive path. Decide whether rotation is decorative, user-driven or required to understand an object; show a meaningful still image or text when the renderer or model fails.

For any autoplay motion, check `prefers-reduced-motion` when mounting and on preference changes. Under reduced motion, show the same meaningful state without continuous camera travel, spin or parallax. If automatic motion runs more than five seconds beside other content, provide pause/stop/hide as required by [WCAG 2.2 SC 2.2.2](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html). A pause control must be usable by keyboard and report its state in text. Do not make focus follow an animated 3D target without an explicit interaction design.

## Own one clock and render loop

In vanilla Three.js, use the renderer's [`setAnimationLoop`](https://threejs.org/docs/pages/WebGLRenderer.html#setAnimationLoop) for the scene's loop. Advance each active [`AnimationMixer`](https://threejs.org/docs/pages/AnimationMixer.html#update) once per frame using a single elapsed delta, then render. Avoid mixing an independent `requestAnimationFrame` loop, a GSAP ticker and a framework-owned loop for the same scene. Pause the loop or mixer when the scene is hidden or the user pauses; on resume, reset timing so hidden-tab elapsed time does not jump the model forward. If rendering only changes on user input, use an on-demand render path instead of continuous work.

In React Three Fiber, join its shared loop with `useFrame`; do not start a second Three.js loop inside a component. Check the installed R3F version because hook timing and scheduler options change. Use the framework's `frameloop="demand"` and invalidation where it fits an otherwise still scene. A continuously playing mixer still needs frames, so choose the loop mode around actual motion. Follow [current R3F hook documentation](https://r3f.docs.pmnd.rs/api/hooks) rather than copying an older hook signature.

Keep authored model clips and interface state distinct. Map explicit app states to `AnimationAction` play, pause, crossfade or stop decisions. If a user reverses or repeats an action mid-transition, cancel or redirect the owned action without leaving the model in an impossible pose. A glTF may have no clips or a different clip name; inspect the loaded asset before binding controls. When a clip ends, place the model at the intended resting pose and leave its DOM status/control synchronized.

## Load, suspend and release

Reserve the canvas region and show loading and error alternatives. Associate every load with the scene instance that requested it. If the route/component unmounts before the load resolves, ignore the stale result and release newly created resources instead of attaching it to a dead scene. Limit new model sources to those authorized for the project; model loading can make network requests for external textures or decoders.

On teardown, stop the owned loop with `renderer.setAnimationLoop(null)` in vanilla Three.js, remove only owned event listeners/observers, stop actions, then use `mixer.uncacheRoot(root)` after stopping actions when the root is retired. Dispose only resources the scene owns: geometries, materials, textures, render targets, skeletons, controls and the renderer as applicable. A material's disposal does not dispose its textures; shared assets require reference ownership so one component cannot dispose another's resource. [Three.js disposal guidance](https://threejs.org/manual/pages/how-to-dispose-of-objects.html) lists the relevant resource types and caveats. R3F owns its Canvas loop and common declarative object cleanup; inspect explicit shared or imperative resources separately rather than disposing the framework renderer from a child.

## Verify the actual product

Inspect these states at the same viewport: loading/poster, first settled frame, mid-animation, paused/reduced-motion state, repeated/interrupted action, error/unavailable state and unmount/remount. Exercise mouse, touch, keyboard, screen reader labels and browser visibility changes. Check the chosen device class under normal and constrained GPU/CPU conditions before claiming a performance gain. Inspect frame time and `renderer.info` across repeated route changes for growth, remembering that some internal caches remain intentionally allocated. Confirm the final still conveys the same product information as the animation.

## Source and scope

This original UX lifecycle method was prompted by the Three.js animation/loading/interaction coverage in [cloudai-x/threejs-skills at `b1c6230`](https://github.com/cloudai-x/threejs-skills/tree/b1c623076c661fc9b03dac19292e825a5d106823) and the Three.js/R3F coverage in [freshtechbro/claudedesignskills at `1da73fe`](https://github.com/freshtechbro/claudedesignskills/tree/1da73febff0c3e1dfefc07f8a5ef8f7d1dfdb6cd). No upstream text, code, scripts or assets are copied. Cloudai-x lacks a root license file in the reviewed revision despite a README MIT claim, so its text is not admitted. Freshtechbro's root MIT notice covers its source, but its starter code and scripts were not needed. Current Three.js, R3F, MDN and W3C documents are the implementation authorities linked above.
