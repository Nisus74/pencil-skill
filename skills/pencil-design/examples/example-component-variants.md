# Example: build a complete Button component family with all variants and states

A worked walkthrough of authoring a reusable component family in `.lib.pen`. The user says:

> *"Build the Button component for our design system. Cover the variants we need (primary, secondary, destructive, ghost, icon-only) and all the states."*

This example exercises the explicit-variants pattern, the `state` theme axis, slot anatomy for label and icons, and the loading-state choreography that won't shift layout. Cross-references: [`references/composition-patterns.md`](../references/composition-patterns.md) for the explicit-variants rule and `.lib.pen` extraction rules; [`references/states.md`](../references/states.md) for the state matrix and the two authoring conventions; [`design-system/components.md`](../design-system/components.md) for the project's component conventions.

---

## Step 1: read context

Before touching the canvas, read the project's design system. The Button has to honour what's already there.

- `design-system/visual-style.md` for the button shape language (rounded radius, no inner shadow, etc.).
- `design-system/tokens.md` for palette tokens (`$accent`, `$surface`, `$textPrimary`, `$danger`, `$focusRing`, `$surfaceMuted`) and type tokens (`$textBase`, `$fontMedium`).
- `design-system/components.md` for the project's component conventions, including whether the project uses variant siblings or a `state` theme axis.
- `design-system/accessibility.md` for the focus ring spec (2px outline, 2px offset, `$focusRing` colour).

Then load the references that govern this kind of work:

- `references/composition-patterns.md` for explicit variants over boolean prop sprawl, status workflow, and slot design.
- `references/states.md` for the state matrix, two authoring conventions, plus loading and focus-with-error edge cases.
- `references/iconography.md` for the rule that icon-only buttons need both `aria-label` and a tooltip.

## Step 2: decide the composition pattern

Per `references/composition-patterns.md` § Explicit variants: shipping a single `<Button variant="primary"/>` with a switch inside leaks into a sprawling boolean prop matrix as the component grows. Build `Button_Primary`, `Button_Secondary`, `Button_Destructive`, `Button_Ghost`, and `Button_IconOnly` as five named siblings. Consumers `ref` the one they need; there's no `variant` prop to keep in sync.

## Step 3: decide where it lives

Per `references/composition-patterns.md` § When to extract to `.lib.pen`: extract when the component hits 2+ uses, the composition's non-trivial, and cross-document reuse is expected. Buttons hit all three on day one. They live in `design-system.lib.pen`.

## Step 4: component status

Per `references/composition-patterns.md` § Component status workflow: ship the initial commit as `status: ready` (functional, may evolve). It'll move to `stable` after one release cycle without breaking changes.

## Step 5: build the base Button frame

Open the library, then create the parent frame that anchors the family. The parent isn't instantiated directly; it's the conceptual root that the variants hang off.

```
open_document({ path: "./design-system.lib.pen" })
U("doc", { themes: { state: ["default", "hover", "focus", "pressed", "disabled", "loading"] } })

button=I("doc", {
  type: "frame",
  name: "Button",
  reusable: true,
  context: "Button component family. Variants: Primary, Secondary, Destructive, Ghost, IconOnly. status: ready. Each variant ships all states (default, hover, focus, pressed, disabled, loading). Uses $accent, $surface, $textPrimary, $danger tokens. Focus ring 2px offset, $focusRing colour. State axis on the doc; bind state-conditional fills on each variant."
})
```

## Step 6: build the five variants as siblings

Each variant is its own reusable frame inside `Button`. Two are shown in full (Primary and Ghost); the other three follow the same shape.

**`Button_Primary`** is the workhorse variant. Filled `$accent`, label uses `$onAccent` (the token that contrasts against accent fills, defined in `tokens.md`).

```
btnPrimary=I(button, {
  type: "frame",
  name: "Button_Primary",
  reusable: true,
  layout: "horizontal",
  alignItems: "center",
  justifyContent: "center",
  gap: "$space-2",
  padding: "$space-3 $space-5",
  cornerRadius: "$radiusMd",
  fill: [
    { value: [{ type: "solid_color", color: "$accent" }],      theme: { state: "default"  } },
    { value: [{ type: "solid_color", color: "$accentHover" }], theme: { state: "hover"    } },
    { value: [{ type: "solid_color", color: "$accent" }],      theme: { state: "focus"    } },
    { value: [{ type: "solid_color", color: "$accentDark" }],  theme: { state: "pressed"  } },
    { value: [{ type: "solid_color", color: "$accent" }],      theme: { state: "disabled" } },
    { value: [{ type: "solid_color", color: "$accent" }],      theme: { state: "loading"  } }
  ],
  opacity: [
    { value: 1.0, theme: { state: "default" } },
    { value: 0.5, theme: { state: "disabled" } }
  ],
  context: "Primary action button. status: ready. One per view. aria-label inherited from label slot."
})

iconLeading=I(btnPrimary, { type: "frame", name: "Slot_IconLeading", slot: true, width: "fit_content", context: "Optional leading icon. Pass an icon node via descendants. Hidden when empty." })
label=I(btnPrimary, { type: "text", name: "Slot_Label", slot: true, content: "Button", fontSize: "$textBase", fontWeight: "$fontMedium", fill: [{ type: "solid_color", color: "$onAccent" }], context: "Required text slot. Override via descendants.Slot_Label.content." })
iconTrailing=I(btnPrimary, { type: "frame", name: "Slot_IconTrailing", slot: true, width: "fit_content", context: "Optional trailing icon. Pass an icon node via descendants. Hidden when empty." })
```

**`Button_Ghost`** uses a transparent fill, label in `$textPrimary`, hover surface in `$surfaceMuted`.

```
btnGhost=I(button, {
  type: "frame",
  name: "Button_Ghost",
  reusable: true,
  layout: "horizontal",
  alignItems: "center",
  justifyContent: "center",
  gap: "$space-2",
  padding: "$space-3 $space-5",
  cornerRadius: "$radiusMd",
  fill: [
    { value: [{ type: "solid_color", color: "transparent" }],     theme: { state: "default"  } },
    { value: [{ type: "solid_color", color: "$surfaceMuted" }],   theme: { state: "hover"    } },
    { value: [{ type: "solid_color", color: "transparent" }],     theme: { state: "focus"    } },
    { value: [{ type: "solid_color", color: "$surfaceSubtle" }],  theme: { state: "pressed"  } },
    { value: [{ type: "solid_color", color: "transparent" }],     theme: { state: "disabled" } }
  ],
  context: "Tertiary action button. status: ready. Use for low-emphasis actions inside dense UI. Same slots as Button_Primary."
})

ghostLabel=I(btnGhost, { type: "text", name: "Slot_Label", slot: true, content: "Button", fontSize: "$textBase", fontWeight: "$fontMedium", fill: [{ type: "solid_color", color: "$textPrimary" }] })
```

`Button_Secondary` (outline `$border`, transparent fill, label `$textPrimary`), `Button_Destructive` (fill `$danger`, label `$onDanger`), and `Button_IconOnly` (square aspect, single icon slot, no label slot) follow the same shape. Each gets its own `fill` array conditioned on `theme.state`, the same padding ramp, and a `context` that records the variant's purpose.

## Step 7: focus ring across all variants

Per `references/states.md` and `design-system/accessibility.md`, focus is the one state you can't skip. Every variant binds a stroke that's transparent by default and visible on `focus`. Apply to each variant frame:

```
U("btnPrimary", {
  stroke: [
    { value: { thickness: 0, fill: "transparent" },              theme: { state: "default" } },
    { value: { thickness: 2, fill: "$focusRing", offset: 2 },    theme: { state: "focus"   } }
  ]
})
```

The ring colour is the same across variants so consumers learn it once.

## Step 8: loading-state choreography

Per `design-system/forms.md` § Submit-state choreography and `references/states.md` § Component states matrix: the loading state replaces the label with a spinner-plus-label lockup. Width has to stay constant so the surrounding layout doesn't jump.

The cleanest way is a `loading` sibling inside each variant that holds the spinner-and-label group, gated to render only when `theme.state == "loading"`:

```
loadingGroup=I(btnPrimary, {
  type: "frame",
  name: "Slot_Loading",
  layout: "horizontal",
  gap: "$space-2",
  alignItems: "center",
  visible: [
    { value: false, theme: { state: "default" } },
    { value: true,  theme: { state: "loading" } }
  ]
})
spinner=I(loadingGroup, { type: "icon_font", iconName: "loader-2", iconLibrary: "lucide", fontSize: 16, fill: [{ type: "solid_color", color: "$onAccent" }], animate: "spin" })
loadingLabel=I(loadingGroup, { type: "text", content: "Saving...", fontSize: "$textBase", fontWeight: "$fontMedium", fill: [{ type: "solid_color", color: "$onAccent" }] })
```

The original label-and-icons row binds `visible: false` on `loading` so the two never stack. Width's preserved because the loading group's content width is sized to roughly match the label.

## Step 9: icon-only button accessibility

Per `references/iconography.md` § Icon-only versus paired with text: an icon-only button needs both an `aria-label` (for screen readers) and a tooltip (for sighted users who hover). Both, every time.

```
btnIconOnly=I(button, {
  type: "frame",
  name: "Button_IconOnly",
  reusable: true,
  width: 40,
  height: 40,
  cornerRadius: "$radiusMd",
  alignItems: "center",
  justifyContent: "center",
  context: "Icon-only button. status: ready. Square 40x40. aria-label is the action verb (e.g. 'Edit', 'Delete', 'Send'). Tooltip uses the same label on hover. Never ship without both."
})

iconSlot=I(btnIconOnly, { type: "frame", name: "Slot_Icon", slot: true, width: "fit_content", context: "Required icon. Pass an icon node from the project's icon library." })
```

The variant's `context` documents the `aria-label` shape so the engineer reading the design knows what to wire up.

## Step 10: slot summary

For Primary, Secondary, Destructive, and Ghost:

- `Slot_Label`: required, text content overridable.
- `Slot_IconLeading`: optional, hidden when empty.
- `Slot_IconTrailing`: optional, hidden when empty.

For IconOnly:

- `Slot_Icon`: required, icon node only.

Per `references/composition-patterns.md` § Slot design: each slot's purpose is documented in its `context` so consumers know what's overridable.

## Step 11: verify

Snapshot the layout, then screenshot the family in both modes.

```
snapshot_layout({ parentId: "button", maxDepth: 3 })
get_screenshot({ nodeId: "button", theme: { mode: "light" } })
get_screenshot({ nodeId: "button", theme: { mode: "dark"  } })
```

Per `references/states.md` § Verification, screenshot the worst-state cases too. Loop the state axis:

```
get_screenshot({ nodeId: "btnPrimary", theme: { state: "focus"    } })
get_screenshot({ nodeId: "btnPrimary", theme: { state: "disabled" } })
get_screenshot({ nodeId: "btnPrimary", theme: { state: "loading"  } })
```

Confirm:

- Five variants render correctly in light and dark modes.
- Six states visible per variant via the theme axis.
- Focus ring's consistent across variants (2px, 2px offset, `$focusRing`).
- Loading state preserves width; the label's still readable as `Saving...`.
- IconOnly variant's `context` documents the `aria-label` shape.

## Final report to user

> *"Done. Button family lives in `design-system.lib.pen` with five variants (Primary, Secondary, Destructive, Ghost, IconOnly), each marked `reusable: true` and `status: ready`. States are bound to a `state` theme axis on the document, so consumers activate hover/focus/pressed/disabled/loading via `theme: { state: ... }` on the ref. Focus ring's consistent across all variants (2px, 2px offset, `$focusRing`). Loading state replaces the label with a spinner-plus-`Saving...` lockup at preserved width. IconOnly variant's `context` records the required `aria-label`-plus-tooltip pattern. Verified with screenshots in light and dark modes plus the focus, disabled, and loading states for Primary."*

## What this example demonstrates

- **Explicit named variants** for a component family instead of a single component with a `variant` prop matrix.
- **`state` theme axis on the document** with state-conditional `fill`, `opacity`, `stroke`, and `visible` arrays on the variants.
- **Slot anatomy** for label and optional leading/trailing icons; required icon slot for IconOnly.
- **Loading-state choreography** that preserves width via a sibling slot gated on `theme.state`.
- **Icon-only accessibility documented in `context`** so the engineer wires up `aria-label` and tooltip from the design.
- **Status workflow surfaced in `context`** so consumers know the family's `ready` (safe to use) rather than `draft` or `deprecated`.

See also: [`references/composition-patterns.md`](../references/composition-patterns.md) for explicit variants and slot design rules; [`references/states.md`](../references/states.md) for the state matrix and authoring conventions; [`design-system/components.md`](../design-system/components.md) for the project's required state coverage.
