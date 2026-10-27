> Historical example, not an instruction or validated implementation. Commands and dependencies below must be reviewed before use. Check the complete behavior, current APIs, accessibility and expected load; fewer lines do not prove equivalence. Operational names have been adapted. Source pin and MIT notice are in the parent library.

# Group By

**Task:** "Group this array of objects by a key."

## Without efficiency guidance

```bash
npm install lodash
```

```js
import { groupBy } from "lodash";

const byStatus = groupBy(orders, "status");
// → { pending: [...], shipped: [...], delivered: [...] }
```

Or the hand-rolled version:

```js
const byStatus = orders.reduce((acc, order) => {
  (acc[order.status] ??= []).push(order);
  return acc;
}, {});
```

## With efficiency guidance

```js
// shortcut: Object.groupBy does this
const byStatus = Object.groupBy(orders, order => order.status);
// → { pending: [...], shipped: [...], delivered: [...] }
```

**1 dependency (or a reduce) → 1 built-in.** `Object.groupBy` shipped in Chrome 117, Firefox 119, Safari 17.4, Node.js 21. If you need a `Map` instead of a plain object: `Map.groupBy(orders, o => o.status)`. Check your target runtime; if you need IE11 or old Node, the `reduce` one-liner is still the right call, not lodash.
