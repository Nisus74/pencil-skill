# Composition patterns

How to design components that scale. The patterns that prevent the slow rot toward god-components, boolean prop explosion, and component libraries that ship 5 buttons that all do the same thing badly.

**What this file owns:** compound components, generic provider/state/actions interfaces, explicit variants vs boolean modes, slot anatomy, descendants override discipline, component status workflow (`draft`/`ready`/`stable`/`deprecated`), when to extract to `.lib.pen`, library-hygiene anti-patterns.

**What this file does NOT own:** how to *read* an existing component before using it (slots, descendants paths, state activation). That's covered in [`component-anatomy.md`](component-anatomy.md). The visual states a component should cover (default/hover/focus/disabled/loading/error/success) live in [`states.md`](states.md). The Pencil schema for `reusable` / `slot` / `ref` nodes lives in [`pen-schema.md`](pen-schema.md). When to load a `.lib.pen` library at all is covered in SKILL.md § Components first.

## When to load this file

- You're designing a new component that other parts of the design will consume.
- You're extending an existing component and noticing it's collected too many props / variants.
- The user names *compound component*, *slot*, *variant*, *boolean prop*, *god component*, *generic provider*, *component library*, *deprecated*, *status*.
- You're auditing a `.lib.pen` for components that should be split, deprecated, or reorganised.

## Compound components vs boolean prop explosion

The most common mistake in component design: a single component grows boolean props as it gains variants, until nobody can remember what's safe to combine.

**The bad pattern.** A button accumulates over a year:

```tsx
<Button
  variant="primary"
  size="medium"
  loading
  disabled
  destructive
  outline
  ghost
  iconLeft={<Icon />}
  iconRight={<Icon />}
  fullWidth
  pill
/>
```

By the time you have ten boolean props, the matrix of valid combinations is unknowable. With `loading + disabled`, does loading override disabled, or disabled override loading? With `destructive + outline + ghost`, what colour wins? The component's TypeScript signature lists every flag, but the *valid combinations* are nowhere. They live in the original author's head.

**The compound pattern.** Break the component into named pieces that compose:

```tsx
<Button.Primary size="md">Save</Button.Primary>
<Button.Secondary size="md">Cancel</Button.Secondary>
<Button.Destructive size="md">
  <Button.Icon><DeleteIcon/></Button.Icon>
  Delete
</Button.Destructive>
<Button.Ghost size="md" loading>Sign in</Button.Ghost>
```

Each variant is a distinct component, with the props it actually supports and no others. `Button.Primary` doesn't have a `destructive` prop because primary buttons can't *be* destructive. That's the contradiction the boolean pattern hides.

**When to use compound components:**

- The component has 3+ visually distinct variants (primary / secondary / ghost / destructive).
- Some props only make sense for some variants (`loading` on `Submit` but not on a `Cancel`).
- The component composes into larger structures (a `Composer` made of header, input, footer, submit).
- A boolean prop is *really* a "which sub-component to render" decision.

**Pencil expression.** A component family in `.lib.pen` looks like a parent `Button` component (containing the shared logic and shared variables) and child `reusable: true` components per variant: `Button_Primary`, `Button_Secondary`, `Button_Ghost`, `Button_Destructive`. Each variant's `context` documents what it's for: *"Primary action button. Used at most once per view."*

When the user asks for a button in their design, you instantiate `Button_Primary` (or whichever variant fits) via a `ref`. The parent isn't directly instantiable; it's the conceptual root.

## Compound components for complex composables

When a component has multiple slots and meaningful internal structure (a chat composer, a card, a modal, a settings panel), the compound pattern goes further: the consumer composes the pieces.

```tsx
<Composer.Provider state={state} actions={actions} meta={meta}>
  <Composer.Frame>
    <Composer.Header>
      <Composer.Title>Reply to thread</Composer.Title>
      <Composer.Close />
    </Composer.Header>
    <Composer.Input placeholder="Type a message…" />
    <Composer.Footer>
      <Composer.Formatting />
      <Composer.Attach />
      <Composer.Submit>Send</Composer.Submit>
    </Composer.Footer>
  </Composer.Frame>
</Composer.Provider>
```

Compare to the boolean alternative:

```tsx
<Composer
  variant="thread-reply"
  showHeader
  showClose
  showFormatting
  showAttach
  submitLabel="Send"
  onSubmit={...}
  onClose={...}
  // ... 30 more props
/>
```

The compound version has zero ambiguity about what renders. The boolean version invites every consumer to discover, by trial and error, which prop combinations work.

**Pencil expression.** Build the compound as a parent component with `slot` frames for each piece. The root `Composer` component has `reusable: true` with slots `Header`, `Input`, `Footer`, `Submit`. Consumers instantiate `Composer` via `ref` and override the slots via `descendants`:

```
{
  "type": "ref",
  "ref": "Composer",
  "descendants": {
    "Header/Title": { "text": "Reply to thread" },
    "Input": { "placeholder": "Type a message…" },
    "Submit": { "text": "Send" }
  }
}
```

See [`component-anatomy.md`](component-anatomy.md) for slot path syntax and the worked deep-dive in [`assets/examples/example-component-deep-dive.md`](../assets/examples/example-component-deep-dive.md).

## Generic provider / state / actions / meta

For components that wrap stateful logic (data fetching, form state, real-time sync), use a three-part interface: `state` (current values), `actions` (functions to update), `meta` (refs, instances, metadata).

```tsx
interface ComposerContextValue {
  state: { value: string; isSending: boolean; isOnline: boolean };
  actions: { setValue: (v: string) => void; submit: () => void };
  meta: { inputRef: React.RefObject<HTMLTextAreaElement>; instanceId: string };
}
```

Now the UI components inside `<Composer.Provider>` know only the *shape* of state/actions/meta, not the implementation. You can swap the provider:

- `Composer.ProviderForThreads` (with thread-specific state and submit logic).
- `Composer.ProviderForDMs` (with DM-specific state).
- `Composer.ProviderForDrafts` (with offline-draft state).

The same `<Composer.Frame>`, `<Composer.Input>`, `<Composer.Submit>` components work with all three, because they only reach for the generic interface.

**Why this matters in design.** Pencil components carry their own `context` describing the data they expect. When you design a `Composer` that should work for threads *and* DMs *and* drafts, document the generic interface in `context`, not the specific use case. Future designers (and engineers) understand they can plug different providers in.

```
"context": "Reusable composer. Expects: state (value/isSending/isOnline), actions (setValue/submit), meta (inputRef). Works for thread replies, DMs, and drafts."
```

## Explicit variants instead of boolean modes

Boolean props that toggle a visual mode (`<Card highlighted>`, `<Button outlined>`, `<Banner urgent>`) are a particular flavour of boolean rot. Replace with explicit variants.

**The boolean version:**

```tsx
<Card highlighted>...</Card>
<Card>...</Card>
```

**The explicit version:**

```tsx
<Card.Highlighted>...</Card.Highlighted>
<Card.Default>...</Card.Default>
```

Why the explicit version is better:

- The TypeScript signature of `Card.Highlighted` and `Card.Default` can differ. Maybe `Highlighted` requires a `recommended` ribbon prop while `Default` doesn't. Boolean modes can't express this.
- Default behaviour is named. Reading the code, you know which card style is in play without checking which props are passed.
- The component library author can deprecate `Card.Highlighted` independently from `Card.Default` if the highlighted style stops being used.
- Search-and-replace becomes possible: `Card.Highlighted` is unambiguously different from `Card.Default` in a grep, while `<Card highlighted>` looks the same as `<Card>` until you parse the props.

**When boolean is fine:** for binary state that's user-controlled and orthogonal to the component's identity. `disabled`, `readOnly`, `loading` are states. They describe what the component is *currently doing*. Keep them as booleans.

The rule: **variants are nouns, state is verbs.** A `Card.Highlighted` is a noun (a kind of card). `loading` is a verb (a state the component is in).

## Slot design

A slot is a hole in a component that the consumer fills. Get this right and the component reads naturally; get it wrong and consumers fight the component.

Rules:

- **Name slots by their content.** `Header`, `Body`, `Footer` is fine if the component genuinely has those regions; `TopSlot`, `MiddleSlot`, `BottomSlot` is meaningless.
- **Default content vs required slot.** Some slots have sensible defaults (a card title that defaults to no-title); some require the consumer to fill them (a modal that requires a body). Document which is which in the slot's `context`.
- **One slot does one thing.** A slot that's "header *or* hero image *or* video" depending on what the consumer passes is overloaded. Split into `Header`, `Hero`, `Video` slots; consumers pick the one they need.
- **Slots can be optional, but they shouldn't be invisible.** A slot with no content shouldn't reserve empty space (it'll look like a layout bug). Either render nothing when empty, or default to filler that matches the design.

In Pencil, a slot is a `frame` node with `slot: true` (or however the local schema expresses it; see [`pen-schema.md`](pen-schema.md)). Document the slot's purpose in its `context`:

```
{
  "type": "frame",
  "name": "ContentSlot",
  "slot": true,
  "context": "Slot for the modal body. Required. Receives any node tree; expected to be plain text, a form, or a media block. Padded by the modal frame; do not double-pad."
}
```

The `context` tells the consumer (or the next agent) what to put in, what's expected, and what's already handled by the wrapper.

## Descendants overrides

When you instantiate a component via `ref` and want to customise a child, you use `descendants`:

```
{
  "type": "ref",
  "ref": "PricingCard",
  "descendants": {
    "Title": { "text": "Pro" },
    "Price/Amount": { "text": "$29" },
    "Price/Period": { "text": "/month" },
    "CTA/Label": { "text": "Start trial" }
  }
}
```

Discipline:

- **Override at instance, edit the component for shared change.** A one-off price for one card → `descendants`. A change to every pricing card's CTA colour → edit the `PricingCard` component itself.
- **Don't `descendants`-override the component's identity.** Overriding the CTA's `fill` colour on every instance to make it look different defeats the component. If you find yourself overriding the same property on every instance, the component has the wrong default; fix the component.
- **Document override expectations in the slot's `context`.** *"CTA label is overridable per instance. Colour and size are component-controlled; do not override."*
- **Path syntax matches the component's child names.** A child at path `Header → Title` is addressable as `"Header/Title"` in `descendants`. Slashes are forbidden in `id` but used as path separators in descendants. See [`component-anatomy.md`](component-anatomy.md) § Building descendants paths.

## Component status workflow

Every reusable component carries a status that tells consumers whether it's safe to use. Surface the status in the component's `context`.

| Status | Meaning |
|--------|---------|
| `draft` | Work in progress. Not stable. May change shape without notice. Use only in exploration. |
| `ready` | Functional and visually finished, but new (limited consumer adoption). Safe to use; report bugs aggressively. |
| `stable` | Battle-tested. Many consumers. Changes go through deprecation. Default choice. |
| `needs-review` | Has accumulated tech-debt or ambiguity. Will be rewritten or split soon. Avoid new uses; existing uses fine. |
| `deprecated` | Replaced by another component. Do not use in new designs. Migrate existing uses to the replacement. |

In a component's `context`:

```
"context": "Primary action button. status: stable (since v1.4.0). Used at most once per view. See states.md for default/hover/focus/disabled/loading/success."
```

For deprecated components, point at the replacement:

```
"context": "status: deprecated (since v1.6.0). Replaced by Button_Primary. Migrate all uses; this component will be removed in v2.0."
```

When you `ref`-instantiate a component, surface the status to the user if it's not `stable` or `ready`:

> *"I'm using `OldButton` here, but it's marked deprecated. It's been replaced by `Button_Primary`. Want me to use the new one instead?"*

The status workflow is what keeps a `.lib.pen` from rotting into a graveyard of half-finished experiments.

## When to extract to `.lib.pen`

A component belongs in a `.lib.pen` when:

- It's used in 2+ places already, or you can name 2+ future uses.
- The composition is non-trivial (more than 3–4 child nodes, or carries state, or has multiple variants).
- Cross-document reuse is expected (the design system, the marketing site, and the product app all use the same `Button`).

A component does NOT belong in a `.lib.pen` when:

- It's a one-off piece of a specific page (a hero composition that won't appear elsewhere).
- It's a sketch in exploration (extract once it stabilises).
- It's premature abstraction. The second use will reveal differences from the first that the abstraction can't bridge.

When in doubt, **build inline first, extract on the second use.** Premature abstraction is harder to fix than late abstraction; the first instance teaches you what's actually variable vs fixed.

When extracting:

1. Build the component in the `.lib.pen`.
2. Mark it `reusable: true`.
3. Set `status: ready` initially (move to `stable` after 3+ consumer uses without changes).
4. Add it to `design-system/components.md` with a one-paragraph "when to use this".
5. Replace inline uses with `ref` instantiations, instance-overriding via `descendants` where they differ.

For the Pencil ops to do all of this, see [`assets/examples/example-import-library.md`](../assets/examples/example-import-library.md).

## Anti-patterns

- **God components.** A `<DataTable>` that handles sorting, filtering, pagination, row selection, inline editing, bulk actions, and export. Split into `DataTable.Toolbar`, `DataTable.Headers`, `DataTable.Row`, `DataTable.Pagination`, `DataTable.BulkActions` so consumers can use the pieces they need.
- **Boolean prop creep.** A component that's grown 12 boolean props over time. Audit it; most of those booleans are variants in disguise. Promote them to compound components.
- **Premature abstraction.** A `Wrapper` component used once to "be ready for future uses" that never come. Inline it; abstract on the third use.
- **Two components that do the same thing.** A `Button` and a `LegacyButton`, neither marked deprecated. Pick one, deprecate the other, migrate.
- **Slots with overloaded purpose.** A slot called `Content` that's expected to be either an icon, an image, or a text block depending on context. Split into named slots.
- **Descendants-overrides as a backdoor for component editing.** Every instance overrides the same property. The component's default is wrong; fix the component.
- **Unnamed variants.** Variants distinguished only by which props are passed (`<Card>` vs `<Card prominent>` vs `<Card prominent compact>`). Name them.
- **Status not surfaced.** A `.lib.pen` with 40 components and no way to know which are safe. Add status to every component's `context`.

## Pencil expression: the whole picture

A well-organised component family in `.lib.pen`:

```
Button (parent: conceptual root, not instantiated directly)
├── Button_Primary    (reusable: true, status: stable)
│   ├── Slot: Label   (text content overridable)
│   └── Slot: Icon    (optional)
├── Button_Secondary  (reusable: true, status: stable)
│   └── (same shape)
├── Button_Ghost      (reusable: true, status: ready, newer)
│   └── (same shape)
├── Button_Destructive (reusable: true, status: stable)
│   └── (same shape)
└── Button_Icon       (reusable: true, status: stable, icon-only variant)
    └── Slot: Icon    (required)
```

Each variant lives at the same hierarchy level (siblings of each other, not nested). Each carries its own `context` documenting what it's for and what state it's in. Consumers `ref` into a specific variant, not the parent.

## Verification checklist

Before declaring a component design done:

1. **Variants are explicit.** No boolean props doing variant work.
2. **Slots are named by content,** not position. Each does one thing.
3. **`status` is set** in every reusable component's `context` (`draft` / `ready` / `stable` / `needs-review` / `deprecated`).
4. **Default vs required slots** documented. Consumers know what they must fill in.
5. **Descendants override expectations** documented in slot `context`.
6. **States are covered** (default / hover / focus / disabled / loading / error / success per [`states.md`](states.md)).
7. **No god components.** If a component has > 6 slots or > 8 variants, split it.
8. **Extracted at the right moment.** Neither premature nor delayed past the third use.
9. **Library hygiene.** Deprecated components point at their replacement.

Fix what fails. Don't ship a component without status; don't ship boolean prop explosion as "v1, we'll clean it up."

## See also

- SKILL.md § Components first: the always-apply rule for reaching for existing components before building from primitives.
- [`component-anatomy.md`](component-anatomy.md): how to read an existing component's structure (slots, descendants paths, state activation).
- [`states.md`](states.md): required state coverage per component type.
- [`pen-schema.md`](pen-schema.md): `reusable`, `slot`, `ref`, `descendants` schema.
- [`forms.md`](forms.md): Form / Field / Input / Submit as a worked example of the compound pattern.
- [`assets/design-system/components.md`](../assets/design-system/components.md): project-level component catalogue.
- [`assets/examples/example-component-deep-dive.md`](../assets/examples/example-component-deep-dive.md): full read→understand→instantiate cycle.
- [`assets/examples/example-import-library.md`](../assets/examples/example-import-library.md): adding a `.lib.pen` to a document.
