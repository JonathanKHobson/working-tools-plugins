# Components, variants, and variables

## Relationship first

A main component defines a reusable object; an instance is linked to that component. Updates and overrides depend on this relationship. Determine which is selected before changing appearance. A similarly named frame is not a component, and visually identical artwork is not evidence of a link. [S17](sources.md#s17)

Inspect the selected object’s type in the UI and the available instance/main-component controls. Prefer the user’s existing component and approved property overrides. Do not detach an instance, recreate it as loose shapes, or edit a shared main component as an unannounced workaround.

## Create one reusable component

**Preconditions:** the selected subtree is the intended new component and does not accidentally include adjacent objects.

Use Create component from the observed context/properties action; Command-Option-K on macOS or Control-Alt-K on Windows is the documented shortcut. A bulk “create multiple components” operation has a different scope. [S18](sources.md#s18)

**Verify:** component identity, meaningful name, expected child structure. Add an instance using the Assets route and check that it remains linked. Test content changes through supported properties where available; do not assume typing directly into arbitrary nested layers creates a reusable text property.

## Variants

Combine the intended components as variants, or use the observed Add variant action on the main component. Configure meaningful property names and distinct value combinations, such as State=Default and State=Disabled. A component set contains component variants, not unrelated loose objects. [S19](sources.md#s19)

Verification requires an instance: use the property control to switch values and inspect the expected result. A “Disabled” label alone does not prove disabled interaction behavior; inspect prototype behavior separately. Do not duplicate masters blindly and infer independent variant relationships from appearance.

When the UI exposes component-property controls, read the actual property name, type, and value. Modify only the authorized property. If the property is not exposed, report that limitation instead of detaching.

## Bind an existing variable

For colors, use the style/variable picker for the specific fill/stroke. Numeric fields can provide a variable picker, including the documented `=` route. Available values depend on type, scope, and enabled libraries. Replacing a resolved number or color with a literal removes the intended relationship. [S20](sources.md#s20)

**Verify:** token identity in the property control, correct collection, resolved value, and effect. A visual match alone is insufficient. If duplicate names exist, disambiguate by collection/library. Do not create another token just because search returned no result before checking type and scope.

## Create or modify variables deliberately

Open the current Variables view from the navigation bar when present; older UI may expose a modal. Select the intended collection, create the correct data type, and set name/value in the observed controls. Aliases refer to compatible variable types. Collections and scopes affect how variables are organized and offered. [S21](sources.md#s21) [S04](sources.md#s04)

A change to a shared variable can affect many objects; it is not equivalent to rebinding one layer. Get explicit scope for shared-token changes, library publication, deleting variables/collections, or mode restructuring. Routine local binding inside an authorized edit does not need repeated confirmation.

When working with modes, confirm the chosen collection and active/inherited mode at the intended container. Check resolved values on representative children. Do not claim light/dark support merely because two modes exist; actual bindings and rendered results need inspection.

## Component QA

Check at least the requested state and one alternate supported state. Verify long/short text on a disposable instance when allowed. Resize without breaking the main/instance link. Inspect bound spacing and colors afterward. Keep a record of the main component changed, instances tested, and properties modified; do not claim every downstream instance was audited unless it was.

## Unavailable library or access

Missing library, blocked edit access, unavailable feature, or a missing font is a real constraint. Report the exact visible condition and any read-only findings. Do not publish, upgrade, import a lookalike library, or fetch assets from outside the approved organization as a silent fix.
