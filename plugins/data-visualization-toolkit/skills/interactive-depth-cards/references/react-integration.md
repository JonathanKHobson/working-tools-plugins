# Project-local React integration

Copy `assets/react/DepthCard.jsx`, `useDepthMotion.js`, and `DepthCard.css` together into an existing React project. Import `DepthCard` and provide project-local asset paths. The component has no icon package, CDN, service, API key or connected-app dependency. Do not install a new app to use it. Adapt the CSS to the owning design system, keeping the structural perspective and back-face rules.

```jsx
<DepthCard
  title="Local card title"
  description="Live card text"
  layers={[
    { src: backgroundUrl, alt: 'Distant landscape', depth: 8, role: 'background' },
    { src: subjectUrl, alt: 'Subject silhouette', depth: 45, role: 'foreground' }
  ]}
  back={{ title: 'Reverse title', body: 'Reverse description' }}
  finish="holographic" depth={70} foil sparkles={12} autoRotate={false}
  instructionsId="card-instructions"
><span>Supplied edition or ability text</span></DepthCard>
<p id="card-instructions">Arrow keys tilt; Home resets; Enter or Space flips.</p>
```

Use `finish` values `holographic`, `gold`, or `silver` and `depth` 0–100. `foil` and `autoRotate` are booleans; `sparkles` is an optional 0–24 decorative count. Children are optional live card-print details; source any factual claims in the owning app. Optional `exploded`/`onExplodedChange` and `flipped`/`onFlippedChange` support controlled parent state; omit them for local state. If the parent supplies a controlled value, supply its change callback as well. The component automatically clears flip when separating layers and rejoins layers when flipping. A `back` object enables the flip control. Provide a unique `instructionsId` per card. `focusRef` may be supplied when the parent needs to focus the card.

Keep the hit region untransformed, with tilt, flipper and faces in separate descendants. The hook writes depth-scaled CSS variables to the tilt wrapper; CSS uses fixed distances. It stops frames when settled or hidden and releases pointer capture, listeners, and frames on unmount. Touch uses vertical pan and an 8px drag threshold before suppressing a flip. Reduced motion stops tilt and ambient orbit while leaving immediate flip and layer-state changes usable. Avoid adding clipping, opacity, filters, or blend modes to a shared 3D ancestor; keep any clipping on the art plane. Test the actual host build and rendered interactions after copying.

If the host app adds an expanded card dialog, give it real dialog semantics, move focus inside on open, handle Escape, restore focus to the opener on close, and release any body scroll lock on every close or unmount path. Keep the separate flip and exploded states coherent inside it. The bundled component does not add a dialog or claim that these host-level duties are already handled.
