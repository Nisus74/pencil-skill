# Composer component — design plan

A Composer is a compound component (header + input + footer), so before laying down a single op I need to do the discipline-rule checks. References I consulted from the skill, and why:

- `SKILL.md` — the default workflow (steps 1 to 7), the Discipline rules (Naming, Context, Components-first, Themes, Responsive, Accessibility), and the verification ladder.
- `references/component-anatomy.md` — because the user wants a **compound component**. I need to know how to structure something with multiple regions (header, body, footer), how to expose them as named children for `descendants` overrides, and whether to fold any region into a `slot`.
- `references/batch-design-grammar.md` — for the op grammar, the `foo=I(...)` binding form, the sizing rules (`fill_container` requires a flex parent), the `padding: [t,r,b,l]` array, and the chunking rule.
- `references/states.md` — because a Composer is interactive and has at least: empty (placeholder visible), filled (text entered), focused, disabled (rate-limited or while sending), loading (mid-send), and over-limit (error). I want to know which states to author up-front.

I will **not** load `flows.md` (single component, no cross-screen flow) or `mcp-tools.md` (I'm only using the standard tools). I'll load `accessibility.md` only if the baseline 5 checks surface something I can't resolve from memory.

## Step 1 — Detect host

I'd call:

```
get_editor_state({ include_schema: false })
```

Expected response shape: an object with `activeDocument` (path or null), `selection` (array of node ids), `themes` (the document's declared theme axes), and `imports` (map of alias to library path). If this errors with `transport not connected to app: desktop`, I stop and tell the user to open the Pencil desktop app or IDE extension. No silent fallback.

What I'd check in the response:

- Is a `.pen` file open? If not, I ask whether to open one or create new.
- Is anything selected? If the user has the canvas pre-positioned on a "components" page or has an existing Composer-shaped frame selected, that changes where I insert.
- What's in `imports`? This drives the components-first inventory in step 3.
- What `themes` are declared? I expect at least `mode: ["light", "dark"]`. If absent, I'll bootstrap.

## Step 2 — Locate context

From step 1's response I know which `.pen` is open. Then I'd list the project root (using a normal directory listing, not the MCP) for `design-system/`. Three outcomes:

- Folder exists with the standard files → load `design-system/README.md`, then `design-system.md` (for the `.lib.pen` path and icon library) and `tokens.md` (for the spacing/type/color naming).
- Folder doesn't exist → offer to scaffold the 12 core templates once. If declined, proceed without and don't ask again this session.
- Folder exists but contains code (`.tsx`, `package.json`) → don't overwrite; ask where to put docs.

For this prompt I'll assume the common case: a `design-system/` folder exists, and `design-system.md` declares a `.lib.pen` path like `./design/system.lib.pen`.

## Step 3 — Load guidelines and inventory components

Two parallel actions:

```
get_guidelines()
```

This returns the categories the server can serve for this document. For a chat-product Composer the category I'd request next is **`Web App`** (or **`Mobile App`** if the project's `Build target` in `design-system.md` says mobile). I'd skip `Landing Page`, `Table`, and `Tailwind` — none of them are about chat input affordances.

Then components-first inventory, per the rule. **This is the most important step for a compound component** — the Composer is built largely from existing primitives:

```
batch_get({ patterns: [{ reusable: true }], readDepth: 2 })
batch_get({ filePath: "./design/system.lib.pen", patterns: [{ reusable: true }], readDepth: 2 })
```

What I'm hunting for, in order of likely reuse:

- An existing **`IconButton`** (for the attachment toggle and probably a mic/voice toggle if the project has one). The Composer header is mostly icon buttons.
- An existing **`ButtonPrimary`** with a `loading` and `disabled` state (for Send). If the project has a `ButtonIcon` variant, even better — Send is sometimes icon-only.
- A **`TextArea`** or **`Input`** component with auto-grow behaviour. If the only input component is single-line, I'll have to either extend it or build a frame-with-text (and offer to add a TextArea to the library).
- An **`Icon`** primitive (Lucide / Material Symbols / Phosphor, whichever `design-system.md` declares).
- A **`Tooltip`** or **`Badge`** if there are inline character-count warning patterns to follow.

If I find an existing `Composer`-shaped component, I stop and use it (the rule: don't fork the library because of a naming preference). If not, I'll build one and offer to promote it to the `.lib.pen` at the end.

I'd also note from inventory whether the library uses **variant siblings** (`Button_Default`, `Button_Hover`...) or a **`state` theme axis** for component states. I'll match the existing convention rather than introducing a third style.

## Step 4 — Plan, atmosphere, and shape

**Atmosphere:** *Balanced density, symmetric, static.* A composer needs to feel like a calm input surface, not a control panel. No motion until the user types.

**Anatomy I'm going to build** (this is the compound component shape — three regions, all named, header and footer minimally tall, body the flex grain):

```
Composer (frame, reusable: true)
├── Composer_Header (frame, layout: horizontal, justifyContent: space-between)
│   ├── HeaderLeft (frame, layout: horizontal, gap: $space-2)
│   │   └── AttachmentToggle (ref → IconButton, icon: paperclip)
│   └── HeaderRight (frame, layout: horizontal, gap: $space-2)
│       └── (slot: HeaderActions — empty, advisory list ["IconButton", "Badge"])
├── Composer_Body (frame, layout: vertical, padding: [12, 16, 12, 16])
│   └── MessageInput (text node OR ref to TextArea — depends on inventory)
└── Composer_Footer (frame, layout: horizontal, justifyContent: space-between, alignItems: center)
    ├── FooterLeft (frame, layout: horizontal, gap: $space-3)
    │   └── CharacterCount (text, content: "0 / 4000", fill: $textMuted)
    └── FooterRight (frame, layout: horizontal, gap: $space-2)
        └── SendButton (ref → ButtonPrimary, label: "Send", icon: arrow-up)
```

Why this shape:

- **Three named region frames** (`Composer_Header`, `Composer_Body`, `Composer_Footer`) so a consumer can target any one of them via `descendants: { Composer_Header: { ... } }`. This is the compound-component contract — the regions are the API surface.
- **Header has a `slot` on the right** (`HeaderActions`) so consumers can drop in a model picker, voice toggle, or mode switch without forking the component. Slot is empty in the origin per the slot rule (and per the `slot frame must be empty in origin` server error).
- **Body is the flex grain** (`width: fill_container`) so the Composer can sit inside any container width.
- **Footer's `CharacterCount` is exposed** as a named child so consumers can override `content` per-instance (`"123 / 4000"`) without reaching into internals. It's also a candidate for hiding via `visible: false` on instances that don't want a counter.
- The Send button on the right matches the universal chat-affordance (right side, primary). Attachment toggle on the left matches Slack / Discord / WhatsApp / Messenger conventions.

**States to author** (from `references/states.md`):

- `default` — placeholder visible, send disabled (no content)
- `filled` — text entered, send active
- `focus` — 2px `$focusRing` outline on the whole Composer card (per accessibility rule 5)
- `disabled` — whole Composer at `opacity: 0.5`, e.g. while user is rate-limited
- `loading` — Send button shows spinner, original width preserved (per the loading state rule), input becomes read-only
- `error` — character count over limit: count flips to `$danger`, paired with an `alert-circle` icon (color is never the only signal — accessibility rule 3), Send disabled

I'll match the project's existing state convention (variant siblings vs `state` theme axis). If the inventory shows variant siblings, I'll create `Composer_Default`, `Composer_Filled`, `Composer_Focus`, `Composer_Disabled`, `Composer_Loading`, `Composer_Error` as siblings inside the `reusable: true` Composer.

**Variables I expect to need, all of which should already exist** (I'll only set them if `get_variables()` shows them missing — never re-declare):

- `$surface` (composer card background)
- `$borderSubtle` (composer card border)
- `$cornerRadiusLg` (composer corner radius — soft, ~12-16px)
- `$textPrimary`, `$textMuted`, `$textPlaceholder`
- `$danger` (over-limit count)
- `$focusRing`
- `$space-2`, `$space-3`, `$space-4` (gaps and padding)
- An accent color for the Send button (already set in the existing `ButtonPrimary`)

If any of these are missing **and the project's tokens.md doesn't declare an alternative**, I'd add them via `set_variables({ replace: false, variables: { ... } })` with both `light` and `dark` values. If `tokens.md` names them differently, I follow `tokens.md`.

I would tell the user this plan in 2-3 sentences before executing — verbatim something like:

> *Plan: I'll build a `Composer` reusable component with three named regions (header, body, footer). Header has an attachment IconButton on the left and a slot for additional actions on the right. Body holds a multi-line text input that grows with content. Footer has a character count on the left and a Send button (instance of ButtonPrimary) on the right. I'll author default, focus, disabled, loading, and over-limit-error states matching the library's existing convention. Plus I'll instantiate one example on the canvas so you can see it. Sound right?*

## Step 5 — Execute

Two `batch_design` calls, both well under the 25-op cap.

**Call 1 — define the `Composer` component itself in the `.lib.pen`** (or in the open `.pen` if the project doesn't yet have a library):

```
composer=I(document, { type: "frame", name: "Composer", reusable: true, context: "Chat input surface for the messaging product. Three regions: header (attachment toggle + slot for additional actions), body (multi-line message input), footer (character count + Send button). States: default, focus, disabled, loading, error (over-limit). Width is fill_container — the consumer determines the surrounding width.", placeholder: true, layout: "vertical", width: 720, fill: "$surface", stroke: { fill: "$borderSubtle", width: 1 }, cornerRadius: "$cornerRadiusLg", padding: [0, 0, 0, 0] })

header=I(composer, { type: "frame", name: "Composer_Header", context: "Top bar of the composer. Holds the attachment toggle on the left and an advisory slot on the right for consumer-supplied actions (model picker, voice toggle, etc.).", layout: "horizontal", width: "fill_container", justifyContent: "space-between", alignItems: "center", padding: [10, 12, 10, 12], gap: "$space-2" })

headerLeft=I(header, { type: "frame", name: "HeaderLeft", layout: "horizontal", gap: "$space-2", alignItems: "center" })

attachmentToggle=I(headerLeft, { type: "ref", ref: "IconButton", name: "AttachmentToggle", context: "Toggles the attachment picker. Single-tap opens the file picker; long-press opens the source menu (camera, files, etc).", descendants: { icon: { iconName: "paperclip" } } })

headerRight=I(header, { type: "frame", name: "HeaderRight", layout: "horizontal", gap: "$space-2", alignItems: "center" })

headerActionsSlot=I(headerRight, { type: "frame", name: "HeaderActions", context: "Slot for consumer-supplied actions. Drop in IconButton or Badge instances per chat surface.", slot: ["IconButton", "Badge"], layout: "horizontal", gap: "$space-2", width: "fit_content", height: "fit_content" })

body=I(composer, { type: "frame", name: "Composer_Body", context: "Multi-line message input region. Min height ~96px (3 lines at default font size), grows with content up to a content cap that the consumer's container enforces via overflow.", layout: "vertical", width: "fill_container", padding: [12, 16, 12, 16], gap: 0 })

messageInput=I(body, { type: "ref", ref: "TextArea", name: "MessageInput", context: "Primary message input. Auto-grows with content. Placeholder reflects the conversation context.", descendants: { input: { placeholder: "Message…" } }, width: "fill_container" })

footer=I(composer, { type: "frame", name: "Composer_Footer", context: "Bottom bar. Character count on the left (muted by default, $danger when over limit), Send button on the right.", layout: "horizontal", width: "fill_container", justifyContent: "space-between", alignItems: "center", padding: [10, 12, 10, 12], gap: "$space-3" })

footerLeft=I(footer, { type: "frame", name: "FooterLeft", layout: "horizontal", gap: "$space-2", alignItems: "center" })

charCount=I(footerLeft, { type: "text", name: "CharacterCount", context: "Live character count. Format: '<count> / <max>'. Color $textMuted by default; $danger when count > max. Consumers override content per-instance.", content: "0 / 4000", fontSize: "$textXs", fill: "$textMuted", fontFeatureSettings: "tnum" })

footerRight=I(footer, { type: "frame", name: "FooterRight", layout: "horizontal", gap: "$space-2", alignItems: "center" })

sendButton=I(footerRight, { type: "ref", ref: "ButtonPrimary", name: "SendButton", context: "Submits the message. Shows spinner while the request is in flight (loading state preserves width). Disabled when the message is empty or over the character limit.", descendants: { label: { content: "Send" }, iconWrap: { children: [{ type: "icon", iconName: "arrow-up" }] } } })

U(composer, { placeholder: false })
```

That's 13 ops, within the chunking budget. Notes on what I'd watch for:

- The `TextArea` `ref` assumes the inventory turned one up. If it didn't, this op becomes either `type: "text"` with `content: ""` and a `placeholder` (if the schema supports it on text — `references/pen-schema.md` would need a check) or a new `MultilineInput` primitive frame I build inline — in which case I'd surface to the user: *"Your library doesn't have a TextArea — I'm building one inline; want me to promote it to your .lib.pen?"*
- The `IconButton` `ref` assumes one exists; same fallback applies.
- The `ButtonPrimary` `descendants` keys (`label`, `iconWrap/icon`) come from the canonical example in `component-anatomy.md`. If the actual library has different child ids, I'd read the component first via `batch_get({ nodeIds: ["ButtonPrimary"], readDepth: 4 })` and adjust. **I would not guess** — wrong descendant keys are silent failures.
- I'm using `fontFeatureSettings: "tnum"` on the char count to keep digits monospaced so the number doesn't jitter as it counts up. (If the schema rejects that property name, I'd drop to using the project's mono font for that single text node per the typography rule.)
- All variables are referenced as `"$name"` — never raw hex.
- Padding everywhere uses the array form `[t, r, b, l]` per the grammar reference (no `paddingTop`).

**Call 2 — author the states** (assuming the project uses variant siblings; I'd switch to a `state` theme axis if that's the convention).

I'd copy the Composer and override the bits that change. Sketch:

```
composerFilled=C(composer, document, { name: "Composer_Filled", context: "Filled state — text entered, character count partway, Send active.", descendants: { "Composer_Body/MessageInput/input": { content: "Hey team, quick update on the migration…", placeholder: "" }, "Composer_Footer/FooterLeft/CharacterCount": { content: "42 / 4000" } } })

composerFocus=C(composer, document, { name: "Composer_Focus", context: "Focus state — 2px focus ring on the card.", stroke: { fill: "$focusRing", width: 2 } })

composerDisabled=C(composer, document, { name: "Composer_Disabled", context: "Disabled (rate-limited / read-only).", opacity: 0.5, descendants: { "Composer_Footer/FooterRight/SendButton": { theme: { state: "disabled" } } } })

composerLoading=C(composer, document, { name: "Composer_Loading", context: "Sending — Send button spinner, input read-only.", descendants: { "Composer_Footer/FooterRight/SendButton": { theme: { state: "loading" } } } })

composerError=C(composer, document, { name: "Composer_Error", context: "Over the character limit. Count is $danger with paired alert-circle icon. Send disabled.", descendants: { "Composer_Footer/FooterLeft/CharacterCount": { content: "4127 / 4000", fill: "$danger" }, "Composer_Footer/FooterLeft": { children: [ { type: "icon", iconName: "alert-circle", fill: "$danger", width: 14, height: 14 }, { type: "text", content: "4127 / 4000", fill: "$danger", fontSize: "$textXs" } ] }, "Composer_Footer/FooterRight/SendButton": { theme: { state: "disabled" } } } })
```

5 more ops. Notes:

- I used `C` (copy) so the states share the source layout. If the library convention is the `state` theme axis, I'd skip these copies and instead author state-conditional values on the original component (`fill: [{ value: "$surface", theme: { state: "default" } }, ...]`).
- The descendant paths use the `parent/child/grandchild` syntax from `component-anatomy.md` — the keys I'm using (`Composer_Body/MessageInput/input`) match the named-id chain of the tree I built in call 1.
- The error state demonstrates the *color is never the only signal* rule (accessibility rule 3): icon + color + text, not color alone.
- The disabled state uses `opacity: 0.5` — at the floor of the readable range per the states reference.

**Call 3 (optional) — instantiate one example on the canvas** so the user can see the shape immediately:

```
example=I(document, { type: "frame", name: "Composer_Example", context: "Live demo of the Composer in a chat surface context.", layout: "vertical", padding: "$space-8", width: 800, fill: "$surfaceMuted", placeholder: true })

instance=I(example, { type: "ref", ref: "Composer", width: "fill_container" })

U(example, { placeholder: false })
```

If the canvas already has multiple top-level frames, I'd call `find_empty_space_on_canvas` first and pass `x` / `y` on the example frame so it doesn't overlap.

## Step 6 — Verify (structural-first, screenshots last)

Per the verification ladder, I work the cheap rungs first:

1. **`batch_design` response** — both calls return success arrays of `{ id: ... }` for each op. Confirm no errors. (Free.)
2. **`snapshot_layout({ parentId: composer, maxDepth: 3 })`** — returns positions and sizes as numbers. Things I'd check from the JSON:
   - `Composer_Header` height ≈ 44 (10+10 padding + ~24 icon button) → meets the 44px hit-target rule for the attachment toggle (accessibility rule 2).
   - `Composer_Body` width fills the container, `MessageInput` width fills `Composer_Body`.
   - `Composer_Footer` height ≈ 36-44, `SendButton` width ≥ 44.
   - `HeaderRight` and `FooterRight` actually right-aligned (their `x` value should put them at the parent's right edge minus padding).
3. **`batch_get({ nodeIds: [composer, messageInput, sendButton, charCount] })`** — confirm:
   - `composer.fill` resolved to `$surface` (a variable, not a raw hex)
   - `composer.stroke.fill` resolved to `$borderSubtle`
   - `messageInput.ref` is the actual `TextArea` id from the library (not a stale string)
   - `sendButton.ref` is the actual `ButtonPrimary` id; `descendants.label.content` is `"Send"`
   - `charCount.fill` is `$textMuted`
4. **Final `get_screenshot`** — only one, scoped to the `Composer_Example` frame (or to the worst state — likely `Composer_Error` per the `references/states.md` "screenshot the worst state" guidance). I'd choose the error state because it's where the icon-pairing, the danger color, and the disabled Send button all collide. If it reads correctly, the default state will.

I would **not** screenshot the default state separately, and I would **not** screenshot light + dark separately because the Composer is built entirely from variables that already have both light and dark values declared in `tokens.md`. The variable system guarantees mode parity.

The five baseline accessibility checks at this point:

1. **Contrast** — `$textMuted` against `$surface` ≥ 4.5:1 in both modes (the project's tokens should already satisfy this; I'd only check explicitly if the screenshot looked off). `$danger` (over-limit count) against `$surface` ≥ 4.5:1.
2. **Hit targets** — attachment IconButton ≥ 44×44, Send button ≥ 44×44. Snapshot confirms.
3. **Color is never the only signal** — over-limit error has the `alert-circle` icon paired with the danger color and the count itself reading `4127 / 4000` (the number is also a signal). Done.
4. **Names map to roles** — every node has a semantic name (`AttachmentToggle`, `MessageInput`, `SendButton`, `CharacterCount`). Done.
5. **Component states cover keyboard focus** — `Composer_Focus` exists with a 2px `$focusRing` outline. Done.

## Step 7 — Iterate or report

Assuming verification is clean, I'd report back something like:

> *Composer landed. It's a `reusable: true` component in `system.lib.pen` with three named regions (`Composer_Header`, `Composer_Body`, `Composer_Footer`), a slot for additional header actions (`HeaderActions`), and five state variants (default / filled / focus / disabled / loading / error). Send is an instance of your `ButtonPrimary`; the attachment toggle is an instance of `IconButton`. There's a live demo on the canvas at `Composer_Example`. Anything you want different — header layout, footer affordances, or the over-limit threshold (currently 4000 chars)?*

If something failed verification — e.g. `Composer_Header` came out 28px tall and breached the 44px hit-target rule — I'd fix it with a targeted `U` op (`U(header, { padding: [12, 12, 12, 12] })`) and re-snapshot before reporting.

## What I'd flag to the user proactively

- **Composer is a strong candidate for the `.lib.pen`.** It's a compound component with multiple states — the kind of thing other chat surfaces in the product will want to reuse. I'd confirm with the user that promoting it to the library is the intent (vs a one-off in the open `.pen`).
- **The character count's max value (4000) is a guess.** The user didn't say. I'd ask, or default to 4000 with a note that they can override it per-instance.
- **The Send button could be icon-only** (just `arrow-up`) on mobile breakpoints. If `design-system.md` says the project ships mobile, I'd offer a `Composer_Mobile` variant or build the Send as a `ButtonIcon` ref instead.
- **Voice input, slash commands, mention pickers** — common Composer companions I deliberately did not add. I'd ask whether any of those are in scope for v1.

That's the full plan and the ops I'd run.
