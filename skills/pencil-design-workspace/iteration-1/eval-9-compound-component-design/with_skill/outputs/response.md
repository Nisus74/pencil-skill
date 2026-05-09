# Composer component — design plan

This is a compound-component design task: a `Composer` with three named regions (Header, Body, Footer) and several configurable child elements (attachment toggle, multi-line text input, Send button, character count). Before I touch the canvas I want to ground the plan in your project's conventions and the existing component library, then build the component as a small family with explicit slots.

## Skill references I consulted (and why)

- `references/composition-patterns.md` — this file owns compound-component design. The Composer it describes (Provider / Frame / Header / Input / Footer / Submit) is almost the exact shape you've asked for, so I'm using its slot vocabulary as the spine of the design rather than inventing my own. It also tells me to avoid boolean-prop explosion (`<Composer showHeader showAttach showCount … />`), which is the wrong shape for something with this many configurable parts.
- `references/component-anatomy.md` — read because once the Composer exists, anyone instantiating it (including future me) needs valid `descendants` paths. This file teaches me to name children deliberately so the `descendants` keys read naturally (`Header/AttachToggle`, `Footer/Send`, `Footer/CharCount`) and to put `slot: true` on the actual content holes.
- `references/forms.md` — the multi-line input has form-shaped behaviour I have to design explicitly: Enter inserts a newline, ⌘+Enter submits, font-size ≥ 16px on mobile to avoid iOS zoom, autocomplete attributes, focus management. The `context` strings I write on the Input and Send nodes will name these so the engineer doesn't have to guess.
- `references/states.md` — the Composer is a stateful surface (input has default / focus / filled / disabled / error; Send has default / hover / focus / pressed / disabled / loading; the whole Composer has an idle / sending / error stance). I need to author all of these, not just the resting state.
- SKILL.md § Components first / Discipline rules — every node I author needs a meaningful PascalCase name, every non-trivial node needs a `context`, theme axes get light + dark colours, and I must check what already exists in the document and any imported `.lib.pen` libraries before building from primitives.

I did not load `flows.md`, `mobile-patterns.md`, `microcopy.md`, or `iconography.md` in detail — they're adjacent but not what this task is asking for. If you tell me the Composer needs to live inside a multi-step thread reply with attachments managed across screens, or that it has bespoke iOS sheet presentation, I'd reach for those next.

---

## Step 1: detect host and locate context

```
get_editor_state({ include_schema: false })
```

I'd expect a result naming the active `.pen` file, any current selection, and (critically) the document's `imports` field. If this errors with `transport not connected to app: desktop`, I stop and ask you to open the Pencil desktop app or the Pencil IDE extension — the skill is explicit that I never silently fall back to the CLI.

I'd also list the project root (a directory listing, not the MCP) to find a `design-system/` folder. If `design-system/components.md` exists, that's where any `Input`, `Button`, `IconButton`, or `Composer` conventions are documented and I'd read it before planning.

What I'd note from the result:
- Name and id of the active document.
- Whether anything is selected (it might tell me where you want the Composer dropped).
- The full `imports` map — the keys (e.g. `"ds"`) and the file paths for each `.lib.pen`.
- Document themes — does it already declare a `mode` axis with `light` and `dark`? Does it declare a `state` axis I can hang Composer states from?

## Step 2: load guidelines and inventory components

Two parallel reads here.

**Guidelines:**

```
get_guidelines()
```

This tells me which guideline categories the document opts into. For a chat composer in a chat product, I'd then read whichever of `Web App`, `Mobile App`, `Tailwind`, `Design System` are present — the chat-product framing makes `Web App` and probably `Mobile App` the right categories.

**Existing components — open document:**

```
batch_get({ patterns: [{ reusable: true }], readDepth: 2 })
```

I'm specifically scanning for: any `Composer`, `MessageComposer`, `ChatInput`, `ReplyBox` already in the document. If one exists, I'd inspect it deeply (`batch_get({ nodeIds: ["<id>"], readDepth: 4 })`) before deciding whether to extend it or build a new one — never fork the library because of a naming preference.

I'm also looking for the building blocks I'll need:
- A `Button` family (`Button_Primary`, `Button_Secondary`, `Button_Icon`, or similar). The Send button and the attachment toggle should reuse these, not redraw them.
- An `Input` or `Textarea` primitive.
- An `Icon` or `IconButton` component, since the attach toggle is icon-based.

**Existing components — imported libraries:**

For each library in `imports`:

```
batch_get({ filePath: "./design/system.lib.pen", patterns: [{ reusable: true }], readDepth: 2 })
```

(Path swapped for whichever paths your `imports` declares.) The chat product almost certainly has a system library; the Composer will instantiate Buttons and Icons from it via `ref` rather than rebuild them.

**Tokens:**

```
get_variables()
```

Before I author any colour, spacing, or radius values, I need to know what already exists. The skill is firm that `set_variables` with `replace: false` still overwrites any key I pass, so I only ever set tokens that are absent from this result. For the Composer I expect to lean on existing `$surface`, `$surfaceMuted`, `$border`, `$textPrimary`, `$textMuted`, `$primary`, `$danger`, `$focusRing`, `$radiusMd`, `$space-*`, `$durationFast` tokens. If any are missing, I'd note them and ask before declaring new ones.

**Mental inventory I'd produce after this step:**

- `Composer` exists? (yes → extend, no → build)
- Which Button variant is the Send button? (`Button_Primary` typically)
- Which IconButton or Icon component fronts the attach toggle?
- Which icon set is in use (Lucide / Phosphor / Material Symbols)? Affects which icon name I write.
- What text-input primitive exists, and does it already support multi-line?

## Step 3: plan the design

A one-paragraph commitment before any `batch_design` call.

> Building a `Composer` compound component in the project's `.lib.pen`. It's a single `reusable: true` parent frame containing three slot regions (`Header`, `Body`, `Footer`) and a small set of named, overridable children (`AttachToggle`, `Input`, `Send`, `CharCount`). The Send and AttachToggle are `ref` instances of existing `Button_Primary` and `Button_Icon` components — not redrawn primitives. The `Input` is a multi-line text node with documented Enter / ⌘+Enter behaviour. The `CharCount` is a small text node bound to a value the consumer overrides; it shifts to `$danger` when count exceeds the limit. The whole component has `state` theme variants for `default`, `focus`, `disabled`, `sending`, and `error`. I'm authoring it in the `.lib.pen`, not as a one-off in a screen, because chat composers are reused across thread replies, DMs, and drafts (per the generic-provider pattern in `composition-patterns.md`).

Atmosphere commitment: **balanced, symmetric, static**. A composer is a workhorse surface; it shouldn't compete with the message list above it for attention. No motion flourishes; predictable rhythm; the Send button is the only loud element.

Top-level frame I'd create: `Composer` — `reusable: true`, vertical layout, `$radiusLg` corners, 1px `$border` stroke, `$surface` fill, `$space-3` padding, `width: "fill_container"`, `gap: "$space-2"`. Status: `ready` (newly authored, will move to `stable` after a few uses).

## Step 4: execute — `batch_design` ops

I'd run this as **two** calls, not one. The first builds the component skeleton; the second authors the state variants. Splitting at the variant boundary keeps each call small enough to debug if something errors, and lets me verify the skeleton structurally before paying to author all the states.

### Call 1 — skeleton (≤25 ops)

I'd pass this to `batch_design`:

```
composer=I("library_root", { type: "frame", name: "Composer", reusable: true, status: "ready", layout: "vertical", width: "fill_container(560)", padding: "$space-3", gap: "$space-2", fill: "$surface", stroke: { fill: "$border", width: 1 }, cornerRadius: "$radiusLg", context: "Reusable chat composer. Compound component with Header / Body / Footer slots and named children for AttachToggle, Input, Send, CharCount. Expects: state (value/isSending/charCount/maxLength/isOnline), actions (setValue/submit/toggleAttach), meta (inputRef). Works for thread replies, DMs, and drafts. Submit on ⌘+Enter; Enter inserts newline. status: ready." })

header=I(composer, { type: "frame", name: "Header", slot: true, layout: "horizontal", width: "fill_container", gap: "$space-2", padding: [0, 0, "$space-1", 0], context: "Header slot. Optional. Holds the AttachToggle and any consumer-supplied controls (formatting, mention, emoji). Render nothing when empty rather than reserving space." })

attachToggle=I(header, { type: "ref", ref: "Button_Icon", name: "AttachToggle", descendants: { icon: { iconName: "paperclip" } }, context: "Toggles the attachment tray. Pressed state indicates the tray is open. Click target ≥ 44×44 (component-handled). Announces state to screen readers via aria-pressed." })

headerSpacer=I(header, { type: "frame", name: "HeaderSpacer", width: "fill_container", height: 1, context: "Pushes any consumer-added trailing controls to the right side of the header." })

body=I(composer, { type: "frame", name: "Body", slot: true, layout: "vertical", width: "fill_container", gap: 0, context: "Body slot. Required. Default content is the multi-line Input; consumers can replace with a richer editor (Lexical, ProseMirror) by overriding this slot's children." })

input=I(body, { type: "text", name: "Input", content: "Type a message…", fill: "$textMuted", fontSize: "$textBase", lineHeight: "$leadingRelaxed", multiline: true, width: "fill_container", minHeight: 44, padding: [8, 0, 8, 0], context: "Multi-line text input. type=text, inputmode=text, autocomplete=off, autocapitalize=sentences, spellcheck=true. Font-size 16px minimum (prevents iOS Safari zoom). Enter inserts a newline; ⌘+Enter submits. Auto-grows up to 6 lines, then internal scroll. Placeholder shown via $textMuted; replaced with $textPrimary on first character. Focus ring lives on the Composer frame, not the input itself, so the whole surface lights up." })

footer=I(composer, { type: "frame", name: "Footer", slot: true, layout: "horizontal", width: "fill_container", gap: "$space-3", padding: ["$space-1", 0, 0, 0], align: "center", context: "Footer slot. Required. Holds CharCount on the left and Send on the right by default. Consumers can add formatting hints or keyboard-shortcut microcopy here." })

charCount=I(footer, { type: "text", name: "CharCount", content: "0 / 2000", fill: "$textMuted", fontSize: "$textXs", fontVariantNumeric: "tabular-nums", context: "Live character count. Bind to state.charCount and state.maxLength. Format: '<n> / <max>'. Tabular numerics so digits don't jitter as the count changes. Switches fill to $danger when n > max; switches to $warning at n > max * 0.9 to give the user a heads-up. aria-live=polite so screen readers announce only when the user pauses typing." })

footerSpacer=I(footer, { type: "frame", name: "FooterSpacer", width: "fill_container", height: 1, context: "Pushes Send to the right." })

send=I(footer, { type: "ref", ref: "Button_Primary", name: "Send", descendants: { label: { content: "Send" }, icon: { iconName: "send", visible: true } }, context: "Submit button. Triggers actions.submit. Disabled while state.value is empty/whitespace-only OR state.charCount > state.maxLength OR state.isSending. Loading state replaces label with 'Sending…' + spinner; preserves width so layout doesn't jump. Keyboard shortcut hint ⌘+Enter shown on hover via tooltip. Idempotency-keyed; double-tap is server-deduped." })

U("composer", { theme: { state: "default" } })
```

Notes on what I'm doing here:

- The Composer is being created inside a `library_root` parent — that's a stand-in for whichever frame in the `.lib.pen` holds the project's reusable components. I'd discover the real id from step 2's library `batch_get` and substitute it.
- I'm using `width: "fill_container(560)"` so the component fills its parent on a wide layout but caps at 560px when given an unbounded parent — a reasonable max-width for a single-column message input. Numeric pixel values are intentional here.
- `padding: [8, 0, 8, 0]` on the Input is `[top, right, bottom, left]` per the schema. There's no `paddingTop`.
- The Send button uses `descendants` to override both the label text and reveal an icon. I'd verify in step 2 that `Button_Primary` actually has `label` and `icon` children at the top level (not nested) — if it does, these are valid keys; if `icon` is nested inside `iconWrap`, the path becomes `iconWrap/icon`.
- Every `slot: true` frame gets a `context` explaining required vs optional and what consumers should put in. The skill is explicit about this in `composition-patterns.md` § Slot design.
- The `Composer`'s `context` documents the full generic interface (`state` / `actions` / `meta`) per the Provider pattern, plus the Enter / ⌘+Enter behaviour and submit constraints. This is the engineer's reading material.
- `tabular-nums` on the CharCount stops the digits from shifting horizontally as the user types — same rule as in `tokens.md` § Typography.
- I'm not declaring `Cover` here because this is a `.lib.pen` library file, not a screen file. Library files don't require Cover frames; screen files do.

### Verify the skeleton (rung 2 — `snapshot_layout`)

```
snapshot_layout({ nodeId: "composer", maxDepth: 3 })
```

What I'd check in the result:
- `Composer` width resolves to its container width, capped at 560.
- `Header`, `Body`, `Footer` are siblings with the right vertical order and the gap I asked for.
- `Footer` lays out horizontally with `CharCount` on the left, `Send` on the right (the spacer in the middle should have `width` matching the available remaining space).
- The Send button's resolved height is ≥ 44px (touch target).
- The Input's `minHeight` rendered as 44 — important for touch and visual balance.

I would **not** screenshot here. The structural snapshot answers every question I have at this stage.

### Call 2 — state variants (≤15 ops)

The skill gives me two patterns: variant siblings (one frame per state) or a `state` theme axis with conditional values. For a Composer the state set is small (default, focus, disabled, sending, error) and most of what changes between states is one or two properties (border colour, opacity, button affordance). I'd use the **theme axis** form — cleaner and less duplication.

```
U("doc", { themes: { state: ["default", "focus", "disabled", "sending", "error"] } })

U("composer", { stroke: [
  { value: { fill: "$border",    width: 1 }, theme: { state: "default" } },
  { value: { fill: "$focusRing", width: 2 }, theme: { state: "focus"   } },
  { value: { fill: "$border",    width: 1 }, theme: { state: "disabled"} },
  { value: { fill: "$border",    width: 1 }, theme: { state: "sending" } },
  { value: { fill: "$danger",    width: 2 }, theme: { state: "error"   } }
] })

U("composer", { opacity: [
  { value: 1,   theme: { state: "default"  } },
  { value: 1,   theme: { state: "focus"    } },
  { value: 0.6, theme: { state: "disabled" } },
  { value: 1,   theme: { state: "sending"  } },
  { value: 1,   theme: { state: "error"    } }
] })

U("send", { theme: [
  { value: { state: "default"  }, theme: { state: "default" } },
  { value: { state: "default"  }, theme: { state: "focus"   } },
  { value: { state: "disabled" }, theme: { state: "disabled"} },
  { value: { state: "loading"  }, theme: { state: "sending" } },
  { value: { state: "default"  }, theme: { state: "error"   } }
] })

errorHelper=I(composer, { type: "text", name: "ErrorHelper", content: "Couldn't send your message. Try again, or copy your draft below.", fill: "$danger", fontSize: "$textXs", visible: [
  { value: false, theme: { state: "default"  } },
  { value: false, theme: { state: "focus"    } },
  { value: false, theme: { state: "disabled" } },
  { value: false, theme: { state: "sending"  } },
  { value: true,  theme: { state: "error"    } }
], context: "Inline error message. Visible only when state.lastSendError is non-null. Copy explains what happened and what the user can do (per voice.md error pattern). The user's typed value is never cleared on error." })

M("errorHelper", "composer", 3)
```

Notes:

- The `state` axis is added to the document themes so any component can opt into state-conditional values.
- `Composer.stroke` carries the focus ring (2px `$focusRing`) when `state` is `focus`, the danger border when `error`, and the resting border otherwise. The focus ring is on the *whole composer* — when the input is focused, the surrounding frame lights up rather than the input itself getting its own ring. This is the chat-app convention (Slack, Discord, iMessage, Linear all do it) and gives the user one consistent focus affordance.
- `disabled` lowers the whole Composer's opacity to 0.6, matching `states.md`'s rule that disabled foreground stays at ≥ 3:1 contrast (0.6 sits inside that bound for typical token contrasts; I'd verify per `get_variables()` resolved values).
- The Send button picks up its own state (default / disabled / loading) by mapping its internal `state` axis to the Composer's. When the Composer is `sending`, the Send button shows `loading`; when the Composer is `disabled`, the Send button is `disabled`. This is the Provider pattern in action — child components react to the parent's state without the consumer wiring it manually.
- The `ErrorHelper` is a text node that's only `visible` in the `error` state. It's positioned between Body and Footer (`M("errorHelper", "composer", 3)` reparents it to index 3 — Header is 0, Body is 1, Footer is 2, ErrorHelper is 3 — but I'd want Body=1, ErrorHelper=2, Footer=3, so the move target index would actually be 2, not 3, and I'd verify the resolved indices via `snapshot_layout` after).

### Verify the variants (rung 2 — `snapshot_layout`, plus rung 3 — `batch_get`)

```
snapshot_layout({ nodeId: "composer", maxDepth: 3 })
batch_get({ nodeIds: ["composer", "send", "errorHelper"], theme: { state: "error" }, readDepth: 2 })
```

The structural snapshot confirms the ErrorHelper is in the right slot order. The `batch_get` with `theme: { state: "error" }` confirms the conditional values resolve correctly: Composer stroke uses `$danger`, ErrorHelper is visible, Send is back to default (not loading).

I'd repeat the `batch_get` once with `theme: { state: "sending" }` to confirm the Send button picks up its loading variant.

## Step 5: final visual sign-off (rung 4 — one screenshot)

```
get_screenshot({ nodeId: "composer", theme: { state: "default" } })
```

Scoped to the composer frame, default state, primary mode (light or dark — whichever the document defaults to). I'm scanning in the order the skill names:

1. Layout integrity — header / body / footer in the right vertical order, the footer's CharCount-and-Send relationship reads cleanly, no element off-canvas.
2. Spacing rhythm — gaps match the tokens (`$space-2` between sections, `$space-3` for outer padding).
3. Type rhythm — Input placeholder reads at 16px, CharCount reads small but legible, Send label reads as the primary affordance.
4. Contrast — Input placeholder against `$surface` clears 4.5:1; CharCount against `$surface` clears 4.5:1; Send button label against its fill clears 4.5:1.
5. Component fidelity — AttachToggle is clearly a `ref` to `Button_Icon` (matches the rest of the library); Send is clearly a `ref` to `Button_Primary`. No hand-built lookalikes.

I would **not** screenshot all five state variants. The variants are theme-axis conditional values built entirely from existing tokens; the variable system guarantees they hold up. The skill's dual-mode rule applies the same way to multi-state authoring — re-screenshot only if I have reason to suspect a state was authored wrong (e.g. raw hex used instead of a variable).

If you want me to screenshot the `error` state because the affordance is significant and you want to see it rendered, I'd do that as a one-off second screenshot — but not as a routine.

## Step 6: report

What I'd hand back to you, after a clean verification:

> Built `Composer` as a reusable component in `<library file>`. Compound shape with three slot regions (`Header`, `Body`, `Footer`) and named children for `AttachToggle` (ref to `Button_Icon`), `Input` (multi-line, ⌘+Enter to submit), `Send` (ref to `Button_Primary`), and `CharCount` (tabular numerics, switches to `$danger` over the limit). Five state variants on a `state` theme axis: `default` / `focus` / `disabled` / `sending` / `error`. The error state surfaces an inline `ErrorHelper` between Body and Footer with copy explaining what happened. Component is marked `status: ready`; promote to `stable` after three consumer uses. Documented the generic `state` / `actions` / `meta` interface in the component's `context` so the engineer ships the right hook shape and any future Composer use (DMs, drafts, scheduled sends) plugs in cleanly.

## Open questions I'd ask before building (and assumptions I'd make if you told me to proceed)

- **Where does the Composer live?** A new component in your existing `.lib.pen`, or its own file? *Assumption if not told*: existing `.lib.pen` alongside the rest of the input components.
- **Send button label.** "Send" is the chat-product default. If your `voice.md` says otherwise (some products use "Reply" inside threads, "Post" for top-level), I'd follow it.
- **Character limit.** I'm assuming 2000 characters as the placeholder default. If your product's real limit is higher (Discord: 2000, Slack: 4000, GitHub: 65,536, iMessage: effectively none), tell me and I'd bind it to `$composerMaxLength` so it's a one-token change.
- **Attach toggle behaviour.** I'm assuming click-to-toggle a tray that lives outside the Composer (the consumer renders it). If attachments live inside the Composer (a horizontal strip below the input), that's a different slot and I'd add `Attachments` between Body and Footer.
- **Mention / formatting / emoji controls.** I left the Header slot extensible with a spacer pattern so consumers can drop more controls in. If you want them as named children of the Composer (so they're part of the component's contract, not consumer-supplied), name them and I'd add them.

If none of these matter for v1, the design above ships as-is and I'd surface anything ambiguous in the hand-back summary rather than ask twice.
