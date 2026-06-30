# Example: reading and using a component from a .pen file

**Task:** "Build a product listing using our card component."

This example walks through the full cycle: discover → inspect → understand → instantiate in three ways → set a state. Reference `references/component-anatomy.md` for the rules behind each step.

---

## Step 1: Inventory — find what's available

```
batch_get({ filePath: "", patterns: [{ reusable: true }], readDepth: 2 })
```

**Response (excerpt):**

```jsonc
[
  { "id": "CardPrimary", "type": "frame", "reusable": true, "name": "Card / Primary" },
  { "id": "ImageBlock",  "type": "frame", "reusable": true, "name": "Image / Block" },
  { "id": "ButtonPrimary", "type": "frame", "reusable": true, "name": "Button / Primary" }
]
```

`CardPrimary` looks like a match. The user said "card component" and `CardPrimary` is the only card here. `ImageBlock` is also available — relevant because `CardPrimary` may have an image slot.

---

## Step 2: Deep read — understand the component before using it

`readDepth: 2` from inventory only shows top-level fields. Before instantiating, read deeply enough to see all the children that become valid `descendants` keys:

```
batch_get({ filePath: "", nodeIds: ["CardPrimary"], readDepth: 4 })
```

**Response:**

```jsonc
{
  "id": "CardPrimary",
  "type": "frame",
  "reusable": true,
  "theme": { "state": "default" },
  "width": 320,
  "children": [
    {
      "id": "thumbnail",
      "type": "frame",
      "slot": ["ImageBlock"],
      "width": 320,
      "height": 200
    },
    {
      "id": "body",
      "type": "frame",
      "children": [
        { "id": "title",    "type": "text", "content": "Card title" },
        { "id": "subtitle", "type": "text", "content": "Supporting text" }
      ]
    },
    {
      "id": "footer",
      "type": "frame",
      "children": [
        { "id": "cta", "type": "text", "content": "Learn more" }
      ]
    }
  ]
}
```

---

## Step 3: Read the output — build your mental map

From the response above:

| What you see | What it means |
|-------------|---------------|
| `thumbnail` has `slot: ["ImageBlock"]` | This is a content hole — fill it via `descendants` |
| `body/title` is a `text` node | Override `content` to change the label |
| `body/subtitle` is a `text` node | Same — override `content` |
| `footer/cta` is nested under `footer` | Path is `"footer/cta"`, not `"cta"` alone |
| `theme: { state: "default" }` | Component has a `state` axis — other states like `"loading"` may be available |

**Valid `descendants` paths for this component:**

```
"thumbnail"       → the slot frame (fill its children)
"body"            → the body container
"body/title"      → the title text
"body/subtitle"   → the subtitle text
"footer"          → the footer container
"footer/cta"      → the CTA text
```

---

## Step 4: Three instantiation patterns

### Pattern 1 — simple content overrides

The most common case: you only need to change text values.

```
batch_design({ filePath: "", input: `
listings = Insert(page, {
  type: "frame", layout: "horizontal", gap: 16,
  children: []
})

card1 = Insert(listings, {
  type: "ref", ref: "CardPrimary",
  descendants: {
    "body/title":    { content: "Espresso Maker" },
    "body/subtitle": { content: "$89.99" },
    "footer/cta":    { content: "Shop now" }
  }
})
` })
```

No image in this instance — the slot stays empty.

---

### Pattern 2 — filling a slot

Put `ImageBlock` into the `thumbnail` slot. Set `children` on the slot's id in `descendants`:

```
batch_design({ filePath: "", input: `
card2 = Insert(listings, {
  type: "ref", ref: "CardPrimary",
  descendants: {
    thumbnail: {
      children: [
        {
          type: "ref", ref: "ImageBlock",
          descendants: { img: { src: "$frenchPressImage" } }
        }
      ]
    },
    "body/title":    { content: "French Press" },
    "body/subtitle": { content: "$34.99" }
  }
})
` })
```

`children: [...]` on the slot's descendant entry injects content into the hole. The `ImageBlock` ref inside also uses `descendants` to set its own `img.src`.

---

### Pattern 3 — nested path override

Use the `/` path syntax to reach `footer/cta` — a node two levels deep:

```
batch_design({ filePath: "", input: `
card3 = Insert(listings, {
  type: "ref", ref: "CardPrimary",
  descendants: {
    thumbnail: {
      children: [
        { type: "ref", ref: "ImageBlock",
          descendants: { img: { src: "$coldBrewImage" } } }
      ]
    },
    "body/title":    { content: "Cold Brew Kit" },
    "body/subtitle": { content: "$52.00" },
    "footer/cta":    { content: "Add to cart" }
  }
})
` })
```

`"footer/cta"` works because `cta` is a child of `footer`. Using `"cta"` alone would fail — it's not a direct child of `CardPrimary`.

---

## Step 5: State variant — loading skeleton

When the product data is loading, show the card in `loading` state. The component has `theme: { state: "default" }` in its definition, which means it has a `state` axis. Pass `theme` on the ref node:

```
batch_design({ filePath: "", input: `
cardLoading = Insert(listings, {
  type: "ref", ref: "CardPrimary",
  theme: { state: "loading" }
})
` })
```

No `descendants` needed — the component's `loading` state is a designed variant that handles its own visual treatment. Don't mix state with content overrides unless you've verified the component handles it (check the design-system docs or the component structure for a `skeleton` child).

---

## What this example demonstrates

| Concept | Where shown |
|---------|-------------|
| Inventory with `readDepth: 2` | Step 1 |
| Deep read with `readDepth: 4` | Step 2 |
| Reading the tree to find slot, paths, states | Step 3 |
| Content-only override | Pattern 1 |
| Slot fill with `children: [...]` | Pattern 2 |
| Nested `/` path syntax | Pattern 3 |
| Activating a theme state on a ref | Step 5 |
