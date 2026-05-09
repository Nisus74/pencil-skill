# Component anatomy — reading and using existing components

Before you can use a component well, you need to read it. This reference covers how to inspect a component's internal structure from a `batch_get` response, identify its slots and configurable children, build valid `descendants` paths, and activate component states in instances.

Load this when: you've found a component during inventory but haven't used it before, a `batch_design` op with `descendants` is erroring on an unknown key, or you need to fill a slot and aren't sure of the syntax.

---

## Reading a component's structure

After inventory surfaces a component, inspect it deeply before instantiating:

```
batch_get({ nodeIds: ["ComponentId"], readDepth: 4 })
```

`readDepth: 4` is the right depth for most components — shallow enough to be cheap, deep enough to see nested children that become valid descendant paths.

**Fields to scan in the result:**

| Field | What it tells you |
|-------|------------------|
| `id` | The component's own id — used in `ref: "id"` when instantiating |
| `children` | Direct children whose `id` values are top-level `descendants` keys |
| `slot` | Present on frame nodes that are content holes (see § Slots below) |
| `reusable` | Confirms you're looking at a component definition, not an instance |
| `theme` | Key-value pairs showing which theme axes the component uses (its states — see § States below) |
| `type` | The kind of node (`text`, `frame`, `icon`, `ref`, etc.) — tells you what properties are valid to override |

**Mental scan order:**

1. Identify top-level children — their `id` values are your primary `descendants` keys.
2. For each child, check for `slot` (content hole) or nested `children` (deeper paths).
3. Note any `theme` values — those are the component's active state options.
4. Look at `content`, `iconName`, or other value fields on text/icon nodes — these are the properties you'll typically override per instance.

**Example component structure returned by `batch_get`:**

```jsonc
{
  "id": "ButtonPrimary",
  "type": "frame",
  "reusable": true,
  "theme": { "state": "default" },
  "children": [
    {
      "id": "iconWrap",
      "type": "frame",
      "children": [
        { "id": "icon", "type": "icon", "iconName": "arrow-right" }
      ]
    },
    { "id": "label", "type": "text", "content": "Button" }
  ]
}
```

From this read you know:
- `label` and `iconWrap` are top-level `descendants` keys
- `icon` is nested inside `iconWrap` → reachable as `"iconWrap/icon"`
- The component has a `state` theme axis with `"default"` active

---

## Identifying and filling slots

A slot is an empty `frame` inside a component, marked with the `slot` property:

```jsonc
{ "id": "mediaArea", "type": "frame", "slot": ["ImageBlock", "VideoBlock"] }
```

The array is a list of *suggested* component ids that fit the slot — it's advisory, not a constraint. The slot itself must be empty in the origin component (no children). You fill it at the point of instantiation via `descendants`.

**Filling a slot — put a ref inside it:**

```jsonc
{
  "type": "ref",
  "ref": "CardPrimary",
  "descendants": {
    "mediaArea": {
      "children": [
        { "type": "ref", "ref": "ImageBlock", "descendants": { "img": { "src": "$heroImage" } } }
      ]
    }
  }
}
```

**Filling a slot — put a primitive inside it:**

```jsonc
"descendants": {
  "mediaArea": {
    "children": [
      { "type": "rectangle", "id": "placeholder", "width": 320, "height": 200, "fill": "$surface2" }
    ]
  }
}
```

**Key rules:**
- Set `children: [...]` on the slot's id in `descendants` to inject content.
- The injected content replaces the slot entirely — you're not appending to children, you're setting them.
- You can also replace the slot node itself (not just its children) by passing `type` alongside other properties in the descendant entry.

---

## Mapping descendant keys

Every `id` in a component's tree is a potential `descendants` key. The rules for building paths:

**Direct child — use its id as-is:**

```jsonc
"descendants": {
  "label": { "content": "Sign in" }
}
```

**Nested child — join ids with `/`:**

```jsonc
"descendants": {
  "iconWrap/icon": { "iconName": "log-in" }
}
```

**Arbitrarily deep — keep joining:**

```jsonc
"descendants": {
  "header/avatar/badge": { "visible": false }
}
```

Build paths left-to-right by following the tree: parent id `/` child id `/` grandchild id.

**Three things a descendant entry can do:**

| Intent | How |
|--------|-----|
| Override properties | Pass only the properties to change: `{ "content": "New label" }` |
| Replace the node entirely | Include `type` in the entry: `{ "type": "icon", "iconName": "check" }` |
| Replace its children | Pass `children: [...]`: `{ "children": [{ "type": "text", "content": "Hi" }] }` |

**Worked trace — three paths from one tree:**

```
CardPrimary
├── thumbnail (frame, slot)
├── body (frame)
│   ├── title (text)
│   └── subtitle (text)
└── footer (frame)
    └── cta (text)
```

Valid `descendants` keys from this tree:

```
"thumbnail"           → the slot frame
"body"                → the body wrapper
"body/title"          → the title text node
"body/subtitle"       → the subtitle text node
"footer/cta"          → the call-to-action text
```

`"title"` alone is **not** a valid key here — `title` is nested under `body`, so the path must be `"body/title"`.

---

## Discoverable properties

When you override a descendant, the valid properties depend on the node's `type`. Read the node's current values from the `batch_get` response to know what type it is and what's safe to pass.

**Common overrides by node type:**

| Node type | Commonly overridable properties |
|-----------|--------------------------------|
| `text` | `content`, `color`, `fontSize`, `fontWeight`, `visible` |
| `icon` | `iconName`, `color`, `width`, `height`, `visible` |
| `frame` | `width`, `height`, `fill`, `cornerRadius`, `visible`, `children` |
| `image` | `src`, `width`, `height`, `visible` |
| `ref` | `ref` (swap to a different component), `descendants`, `theme` |

**At the top-level ref node**, the properties you can pass are those on the root frame itself (`width`, `height`, `x`, `y`, `theme`, `visible`, `context`) plus `descendants`. You cannot override internal children directly on the ref — use `descendants` for that.

**Reading current values as a type hint:** if the origin has `"content": "Button"` on a text node, you know `content` is a string. If it has `"iconName": "arrow-right"`, you know that field takes an icon name string. Match the type you see, not what you guess.

---

## Component states in instances

Components express their interactive states via theme axes. When a component has `"theme": { "state": "default" }` in its definition, it supports a `state` axis with at least one value — and likely others.

**Discovering available states:**

The `batch_get` result shows the *active* state, not all possible states. To see all values the axis supports, read the component's parent document themes or check `get_editor_state`. In practice, common state values are: `default`, `hover`, `focus`, `pressed`, `disabled`, `loading`, `error`, `success`, `skeleton`. Not every component implements all of them — verify against the tree rather than assuming.

**Setting a state in an instance:**

Pass `theme` on the `ref` node to activate a different state:

```jsonc
{
  "type": "ref",
  "ref": "ButtonPrimary",
  "theme": { "state": "disabled" },
  "descendants": {
    "label": { "content": "Please wait" }
  }
}
```

**Setting a state on a specific descendant** (when only part of the component should change state):

```jsonc
"descendants": {
  "iconWrap": { "theme": { "state": "loading" } }
}
```

**Caution:** Not all components have a `state` theme axis. A component without `theme` in its structure has no states to set — passing `theme` on the ref will create a new axis rather than toggling a designed state, which is usually wrong. Always verify from the `batch_get` output before setting theme values.
