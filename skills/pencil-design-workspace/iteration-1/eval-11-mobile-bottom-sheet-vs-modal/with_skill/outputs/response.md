# iOS compose flow: filter selection, attachments picker, discard confirmation

## References I consulted

I read the skill's `SKILL.md` and then loaded the references the routing rules pointed me at for this exact prompt:

- `references/mobile-patterns.md` — owns the bottom-sheet-vs-modal call, sheet detents, safe areas, keyboard avoidance, haptics, swipe-to-dismiss, and the iOS action-sheet conventions. Loaded because the prompt names "iOS app", "bottom sheet vs modal" is the central question, and one of the three surfaces is destructive.
- `references/interactions.md` — owns the destructive-action discipline (Pattern A confirmation vs Pattern B undo, focus on Cancel, action-labelled confirm button, no combination), modal mechanics, focus restore, hit-target floor on touch.
- `references/microcopy.md` — owns the destructive confirmation copy shape ("state the consequence; label the action button with the action; never 'Confirm' or 'Yes'"), action-specific CTA patterns, and the "show what's possible" empty-state framing for the picker.
- `references/flows.md` — owns the modal-vs-sheet-vs-popover decision table, the hard-confirmation-vs-undo rule for destructive actions, and the back-stack model for iOS modals.
- `assets/examples/example-mobile-app.md` — the worked walkthrough is almost a direct precedent: a Compose sheet at iPhone-15 dimensions with safe-area handling, keyboard-up state, haptic markers in `context`, and a `Mobile / Compose / NN / ...` hierarchical naming pattern. I'm extending that example rather than reinventing it.

I did not load `forms.md`, `states.md`, `industry-patterns.md`, `iconography.md`, `accessibility.md`, `composition-patterns.md`, or `colour-palettes.md` — they're relevant in a real session but the prompt is bounded to three sheets/modals and I have the patterns I need. I'd reach for `states.md` next if the user asked for the upload-progress state on the picker, and `composition-patterns.md` if I was promoting `BottomSheet` to the library.

## The three-surface decision (sheet vs modal vs action sheet)

The skill's routing forces this call up-front, before any `batch_design` op. From `mobile-patterns.md` § Bottom sheets vs modals and `flows.md` § Modal vs page vs sheet vs popover:

| Surface | Decision | Why |
|---|---|---|
| Filter selection | **Bottom sheet, half detent** | Picking from a finite list. Underlying compose context still matters (the user is filtering *what they're composing against*). Reversible. Matches Apple Mail's filter picker and Linear iOS. Half detent default per `mobile-patterns.md` § Sheet detents. |
| Attachments picker | **Bottom sheet, full detent (with half drag stop)** | Editor-shaped surface — the user is browsing a grid of media that needs canvas. Default detent is `full` because the photo grid wants room; drag-down to `half` lets the user peek the compose body underneath. Matches iMessage's photo picker and Discord iOS. |
| Discard draft | **Action sheet (iOS UIAlertController.actionSheet equivalent)** | Three-to-five contextual options where one is destructive. iOS-native pattern, slides up from the bottom, NOT a centred modal. From `mobile-patterns.md` § Native conventions per platform: "Action sheet for 3-5 contextual options where one is destructive." |

Two notes on that last call. First, an action sheet IS the iOS-native destructive-confirmation surface — using a centred modal here would read as Android-blind or web-blind. The action sheet is what Apple Mail uses on swipe-to-delete-trash, what Photos uses on Delete Photo, and what Notes uses on Delete Note. Second, this is `interactions.md` Pattern A (confirmation), not Pattern B (undo). Discarding a draft destroys typed work that the system can't realistically resurrect once the sheet closes; an undo toast on the home feed wouldn't be reachable while the user is still inside the compose context. So: confirmation, focus-on-cancel-equivalent (the iOS pattern is to make Discard the destructive-tinted option and Cancel the bottom-anchored default), action-labelled button (`Discard draft`, not `Confirm` or `Yes`).

## Plan I'd present to the user before any batch_design call

Per the skill's step 4: state the plan in 2-3 sentences, name the frames, name the components I'll instantiate, name the components I'll have to build from primitives.

> *"I'll add four sibling frames to your `.pen`, all at iPhone 15 dimensions (390 × 844), placed in the canvas region right of any existing compose work via `find_empty_space_on_canvas`. Frame names follow your hierarchical pattern: `Mobile / Compose / 03 / FilterSheet / Default / iPhone15`, `Mobile / Compose / 04 / AttachmentsPicker / Default / iPhone15`, `Mobile / Compose / 05 / DiscardActionSheet / Default / iPhone15`, and `Mobile / Compose / 06 / DiscardActionSheet / Pressed / iPhone15` (the destructive-button-pressed state, since the visual feedback matters for the action that's about to delete work). I'll instantiate `Sheet`, `BottomSheetGrabber`, `IconButton`, `Input`, `ListRow`, and `ButtonPrimary` from your `.lib.pen`; if `Sheet` doesn't yet exist as a reusable I'll build the chrome inline and surface it as a library candidate at the end. The destructive surface uses the iOS action-sheet shape — not a centred modal — with the discard option in red and Cancel anchored at the bottom in the iOS-conventional 'safe' position."*

This is the moment to catch bad assumptions cheaply. If the user says "no, the picker should match our existing share-sheet detent (peek-then-half)" or "we don't ship a destructive action sheet pattern, use a centred modal because that's what the rest of the app does" — those are pivots I'd want before opening `batch_design`.

## Tools I'd call (and what I'd check)

### Step 1 — host detection
```
get_editor_state({ include_schema: false })
```
Expecting: success with the open document's id, the current selection, the schema version, and the `imports` field. Failure (`transport not connected to app: desktop`) means stop and tell the user to open the Pencil desktop app or IDE extension. Per the skill, never silently fall back to the CLI.

### Step 2 — filesystem context
List the project root for `design-system/`. If the folder exists, read `README.md`, then `mobile.md`, `tokens.md`, `voice.md`, and `components.md` (the four most relevant for this task). If it doesn't exist, offer the scaffold once per the skill's failure-mode #3 and proceed.

### Step 3 — guidelines + component inventory
```
get_guidelines()
```
Confirm the live category list, then load `Mobile App` for the iOS conventions Pencil's server is currently teaching.

```
batch_get({ patterns: [{ reusable: true }], readDepth: 2 })
batch_get({ filePath: "./design/system.lib.pen", patterns: [{ reusable: true }], readDepth: 2 })
```

I'd expect responses listing the reusable components in the open doc and the imported `.lib.pen`. What I'm scanning for: existing `Sheet`, `BottomSheet`, `ActionSheet`, `Sheet_Header`, `Sheet_Grabber`, `ListRow`, `IconButton`, `ButtonPrimary`, `ButtonDestructive`, `MediaGrid`, and `MediaTile`. The deeper inspection per `references/component-anatomy.md`:

```
batch_get({ nodeIds: ["Sheet", "ListRow", "IconButton"], readDepth: 4 })
```

I'm looking for `slot` frames (so I know what content holes I can fill via `descendants`), named children whose ids form valid `descendants` keys, and any `theme` axes (e.g. `state` with `default | hover | pressed | destructive`). If a `ButtonDestructive` variant exists or `ButtonPrimary` carries a destructive state, I use it; if not, I build the discard button from `ButtonPrimary` with a `$dangerFill` override and surface it as a library candidate.

### Step 4 — plan (above) and find canvas space
```
find_empty_space_on_canvas({ width: 390 * 4 + 60 * 3, height: 844, padding: 60, direction: "right" })
```

Returns `(x, y)` for the leftmost frame; the other three sit at `x + 450`, `x + 900`, `x + 1350`. Four frames at iPhone width plus 60px gutters between them — wide enough that a code generator or a teammate can scrub the sequential states without zooming.

### Step 5a — first batch_design (Filter sheet)

The compose body sits underneath, dimmed by a scrim. The sheet occupies the bottom half. From `mobile-patterns.md`: drag handle visible, swipe-down dismisses, half detent default. The filter is a list of options with a checkmark on the current selection.

```
filter=I("doc", { type: "frame", name: "Mobile / Compose / 03 / FilterSheet / Default / iPhone15", layout: "vertical", x: <x>, y: <y>, width: 390, height: 844, fill: [{ type: "solid_color", color: "$scrim" }], context: "Filter selection sheet at half detent (~422px). Underlying Compose body visible above. Swipe-down or backdrop-tap dismisses without commit. Selection commits on tap; haptic selection feedback fires." })
backdrop=I(filter, { type: "frame", name: "BackdropTap", width: "fill_container", height: 422, context: "Tap to dismiss without committing selection." })
sheet=I(filter, { type: "frame", name: "Sheet", layout: "vertical", width: "fill_container", height: 422, cornerRadiusTopLeft: "$radiusXl", cornerRadiusTopRight: "$radiusXl", fill: [{ type: "solid_color", color: "$surface" }], context: "Half detent. Drag handle present. Drag up to full not enabled — finite list does not benefit." })
grabber=I(sheet, { type: "frame", name: "Grabber", width: 36, height: 5, cornerRadius: 2.5, fill: [{ type: "solid_color", color: "$borderMuted" }], alignSelf: "center", marginTop: 8, context: "iOS-conventional drag handle. Centered." })
header=I(sheet, { type: "frame", name: "SheetHeader", layout: "horizontal", justifyContent: "space-between", alignItems: "center", padding: "$space-4", width: "fill_container" })
title=I(header, { type: "text", text: "Filter by", fontSize: "$textBase", fontWeight: 600 })
clear=I(header, { type: "ref", ref: "LinkText", descendants: { label: { text: "Clear" } }, context: "Resets selection to All. Disabled when current selection IS All." })
list=I(sheet, { type: "frame", name: "OptionsList", layout: "vertical", width: "fill_container", paddingBottom: 34, context: "Bottom inset 34px clears home indicator. Each row is 56px to honor 44px hit floor with 6px top/bottom padding." })
optAll=I(list, { type: "ref", ref: "ListRow", descendants: { label: { text: "All posts" }, trailingIcon: { iconName: "check" } }, theme: { state: "selected" }, context: "Currently selected. Filled checkmark in $accent." })
optMine=I(list, { type: "ref", ref: "ListRow", descendants: { label: { text: "From you" } } })
optMentions=I(list, { type: "ref", ref: "ListRow", descendants: { label: { text: "Mentions of you" } } })
optSaved=I(list, { type: "ref", ref: "ListRow", descendants: { label: { text: "Saved" } } })
optHidden=I(list, { type: "ref", ref: "ListRow", descendants: { label: { text: "Hidden" } } })
```

About 13 ops. Notes:
- The sheet is exactly `844 / 2 = 422` tall — the half detent. The backdrop fills the gap above.
- `paddingBottom: 34` on the list clears the home indicator per `mobile-patterns.md` § Safe areas. Selection rows have a 44px-floor hit zone via 56px row height with 6px vertical padding.
- The selection haptic is documented in the sheet's `context`, not buried in tokens. Per `mobile-patterns.md` § Pencil expression, haptics are behavioural, not visual.
- I'm using `ListRow` from the library; if it carries a `selected` theme state, I activate it via `theme: { state: "selected" }`. If it doesn't, I add an inline `IconButton` for the check and note the selected-state variant as a library follow-up.
- Copy is short, semantic. "All posts" not "All" alone, because alone is ambiguous. "From you" and "Mentions of you" are second-person per the skill's content rules.

### Step 5b — second batch_design (Attachments picker)

This is the editor-shaped surface. Full detent default; the user can drag down to half to peek the compose body. The grid is a 4-column thumbnail layout that's grown to fill the canvas, with a header row for the system row (Camera, Files, Recent) and a bottom action bar with `Cancel` and `Add (n)`.

```
picker=I("doc", { type: "frame", name: "Mobile / Compose / 04 / AttachmentsPicker / Default / iPhone15", layout: "vertical", x: <x + 450>, y: <y>, width: 390, height: 844, fill: [{ type: "solid_color", color: "$scrim" }], context: "Attachments picker at full detent. Drag-down to half exposes the compose body for context. Drag-down again dismisses without committing selection. Selected count surfaces in the bottom action bar." })
sheet=I(picker, { type: "frame", name: "Sheet", layout: "vertical", width: "fill_container", height: 800, cornerRadiusTopLeft: "$radiusXl", cornerRadiusTopRight: "$radiusXl", fill: [{ type: "solid_color", color: "$surface" }], context: "Full detent (800px ≈ full minus 44px top peek)." })
grabber=I(sheet, { type: "frame", name: "Grabber", width: 36, height: 5, cornerRadius: 2.5, fill: [{ type: "solid_color", color: "$borderMuted" }], alignSelf: "center", marginTop: 8 })
header=I(sheet, { type: "frame", name: "Header", layout: "horizontal", justifyContent: "space-between", alignItems: "center", padding: "$space-4", width: "fill_container" })
hCancel=I(header, { type: "ref", ref: "LinkText", descendants: { label: { text: "Cancel" } }, context: "Dismisses picker. Selected items not added to the post." })
hTitle=I(header, { type: "text", text: "Recent", fontSize: "$textBase", fontWeight: 600 })
hAlbum=I(header, { type: "ref", ref: "IconButton", descendants: { icon: { iconName: "chevron-down" } }, context: "Opens album switcher (sub-sheet). Triggers iOS Photos permission prompt on first use." })
sourceRow=I(sheet, { type: "frame", name: "SourceRow", layout: "horizontal", gap: "$space-3", padding: "$space-4", width: "fill_container", context: "Three system source affordances. Camera, Files, GIFs. Tapping Camera triggers iOS camera permission prompt on first use." })
camera=I(sourceRow, { type: "ref", ref: "IconButton", descendants: { icon: { iconName: "camera" }, label: { text: "Camera" } } })
files=I(sourceRow, { type: "ref", ref: "IconButton", descendants: { icon: { iconName: "folder" }, label: { text: "Files" } } })
gifs=I(sourceRow, { type: "ref", ref: "IconButton", descendants: { icon: { iconName: "image-play" }, label: { text: "GIFs" } } })
grid=I(sheet, { type: "frame", name: "MediaGrid", layout: "grid", columns: 4, gap: 2, padding: 0, width: "fill_container", height: "fill_container", context: "4-column thumbnail grid. 2px gap reads as a continuous mosaic. Tap selects with selection-count badge; long-press previews. Multi-select supported." })
// 12-16 thumbnail tiles, two of which are in selected state
tile1=I(grid, { type: "ref", ref: "MediaTile", theme: { state: "selected" }, descendants: { image: {}, badge: { text: "1" } } })
tile2=I(grid, { type: "ref", ref: "MediaTile", descendants: { image: {} } })
tile3=I(grid, { type: "ref", ref: "MediaTile", theme: { state: "selected" }, descendants: { image: {}, badge: { text: "2" } } })
// ... fill grid
actionBar=I(sheet, { type: "frame", name: "ActionBar", layout: "horizontal", justifyContent: "space-between", alignItems: "center", padding: "$space-4", paddingBottom: 34, width: "fill_container", fill: [{ type: "solid_color", color: "$surface" }], stroke: { thickness: 1, fill: "$border", side: "top" }, context: "Bottom inset 34px for home indicator. Action bar pinned above home indicator; sticky to bottom of sheet." })
addBtn=I(actionBar, { type: "ref", ref: "ButtonPrimary", descendants: { label: { text: "Add 2" } }, context: "Label dynamic with selection count. Disabled when count is 0. Tap fires success haptic, dismisses sheet, attaches selections to compose body." })
```

About 18 ops, not counting the rest of the grid tiles which I'd add in a continuation `batch_design` to stay under the 25-op floor (`batch-design-grammar.md`). Notes:
- Two tiles show selected state with numeric badges (`1`, `2`) — iOS Photos uses this exact pattern. Selection order is preserved and surfaced in the badge.
- The Add button's label restates the count: `Add 2`, not `Done` or `Confirm`. Per `microcopy.md`: action-specific verbs that include the noun.
- The G op for media: I'd use `G(<tileImage>, "unsplash", "city skyline")`, `G(<tileImage>, "unsplash", "morning coffee")`, etc., to fill thumbnails with plausible content rather than gray placeholders. Per `flows.md` § Plausible content.
- The album-switcher chevron in the header is a sub-sheet pattern; I'd note in `context` that it's a separate frame I haven't drawn ("opens album switcher sub-sheet — design as `Mobile / Compose / 04a / AlbumSwitcher / iPhone15` if needed").
- Permission prompts are iOS-modal and system-rendered; I name them in `context` so the engineer wires `requestAuthorization` correctly but I don't mock the system modal.

### Step 5c — third batch_design (Discard draft action sheet)

This is the destructive surface. iOS action sheet shape: dimmed scrim covering everything; a "card stack" anchored to the bottom safe area; the destructive option on top in red; Cancel anchored at the bottom in a separate visual group, with the iOS-conventional larger tap target.

```
discard=I("doc", { type: "frame", name: "Mobile / Compose / 05 / DiscardActionSheet / Default / iPhone15", layout: "vertical", justifyContent: "flex-end", x: <x + 900>, y: <y>, width: 390, height: 844, fill: [{ type: "solid_color", color: "$scrim" }], context: "iOS-native action sheet for destructive draft discard. Triggered from Cancel tap on Compose sheet when draft body is non-empty. Esc key (hardware keyboard) cancels. Tapping scrim cancels (non-destructive default)." })
backdrop=I(discard, { type: "frame", name: "BackdropTap", width: "fill_container", height: "fill_container", context: "Tap dismisses with no action — equivalent to Cancel. Per iOS HIG action-sheet conventions." })
stack=I(discard, { type: "frame", name: "ActionStack", layout: "vertical", gap: 8, padding: 8, paddingBottom: 42, width: "fill_container", context: "iOS action sheet stack. 8px gap visually separates the destructive action card from the Cancel card. Bottom inset 42px (8 + 34) clears home indicator." })
card=I(stack, { type: "frame", name: "ActionCard", layout: "vertical", width: "fill_container", cornerRadius: "$radiusLg", fill: [{ type: "solid_color", color: "$surfaceFloating" }], context: "Top card holds the message and destructive action. iOS-frosted-material treatment in production." })
title=I(card, { type: "frame", name: "Title", padding: "$space-4", width: "fill_container", context: "Action sheet title — explains the consequence." })
titleText=I(title, { type: "text", text: "Discard this draft? You'll lose what you've written.", fontSize: "$textSm", fontWeight: 500, fill: [{ type: "solid_color", color: "$textMuted" }], textAlign: "center", context: "Two-sentence consequence statement. Mirrors microcopy.md guidance: state the consequence, do not soften with 'Are you sure?'." })
divider=I(card, { type: "frame", name: "Divider", width: "fill_container", height: 0.5, fill: [{ type: "solid_color", color: "$borderMuted" }] })
discardBtn=I(card, { type: "frame", name: "DiscardButton", layout: "vertical", justifyContent: "center", alignItems: "center", height: 56, width: "fill_container", context: "Destructive action. Min 56px hit zone. Tap fires light-impact haptic on press, then warning notification haptic on commit. Press state shows $surfaceMutedPressed background." })
discardLabel=I(discardBtn, { type: "text", text: "Discard draft", fontSize: "$textBase", fontWeight: 600, fill: [{ type: "solid_color", color: "$danger" }], context: "Action-labelled per microcopy.md — never 'Confirm' or 'Yes'. The verb 'Discard' restates the consequence." })
cancelCard=I(stack, { type: "frame", name: "CancelCard", layout: "vertical", justifyContent: "center", alignItems: "center", height: 56, width: "fill_container", cornerRadius: "$radiusLg", fill: [{ type: "solid_color", color: "$surfaceFloating" }], context: "Separated Cancel card. iOS-conventional bottom anchor — the 'safe' default is reachable by thumb. Tap dismisses sheet, returns to Compose with draft preserved." })
cancelLabel=I(cancelCard, { type: "text", text: "Cancel", fontSize: "$textBase", fontWeight: 600, fill: [{ type: "solid_color", color: "$accent" }] })
```

About 13 ops. Notes:
- The destructive card and Cancel card are visually separated by the 8px gap in the stack, exactly the iOS HIG pattern. This is what makes it read as an action sheet rather than a generic centred modal.
- "Discard draft" is the action label per `microcopy.md` § Confirmation copy and `interactions.md` § Destructive actions: never "Confirm", never "Yes", never bare "Discard" without the noun.
- The title text is two sentences: consequence statement + "you'll lose what you've written". From `microcopy.md`: "State the consequence. Don't soften ('Are you sure?')." It's not framed as a question — questions invite slip-clicks.
- The destructive label is `$danger` red; the Cancel label is `$accent` — colour signals the destructive option without colour being the *only* signal (the verb "Discard" alone tells the user what's about to happen).
- Haptics: light impact on press, warning notification haptic on commit. This is per `mobile-patterns.md` § Haptic feedback: error/warning haptic for destructive commits. Skipping the haptic on a destructive action is one of the silent-state-change anti-patterns.
- Bottom inset is `8 + 34 = 42` to clear the home indicator while preserving the 8px stack gap above.

### Step 5d — fourth batch_design (Discard pressed state)

A short fourth frame showing the destructive-button-pressed state — the press visual is the moment that needs to feel deliberate, not accidental. From `interactions.md` § Hit targets: the press affordance reassures the user that the system registered their tap.

```
pressed=C("discard", "doc", { name: "Mobile / Compose / 06 / DiscardActionSheet / Pressed / iPhone15", x: <x + 1350>, y: <y>, context: "Destructive button mid-press. Background is $dangerSurfaceSubtle to confirm the press registered. Light-impact haptic has fired; warning haptic fires on release." })
U("<copied DiscardButton id>", { fill: [{ type: "solid_color", color: "$dangerSurfaceSubtle" }] })
```

2 ops. The copy-with-overrides pattern keeps the rest of the action sheet identical so the difference is visible.

### Step 6 — verification (structural-first)

Per the skill's verification ladder, I'd walk rungs 1-3 before screenshotting:

1. `batch_design` response — confirm all four calls succeeded, no schema errors. Common issues to watch: id contains `/` (the schema rejects it; my hierarchical names live in `name`, ids stay PascalCase like `discardBtn`); used `width: "100%"` (would fail; I used `"fill_container"`); used `paddingTop` (the schema uses `padding` array; I used the array form).

2. `snapshot_layout({ parentId: "filter", maxDepth: 3 })`, then for `picker`, `discard`, `pressed`. What I'd check:
   - Filter sheet height is exactly 422 (half of 844). Backdrop height is 422 (the gap above). Sum is 844.
   - Picker sheet height is 800 (full minus 44 top peek). Action bar pinned to bottom with 34px inset clearing home indicator. Add button reachable.
   - Discard action sheet: stack pinned to bottom with 42px clearance. Cancel card visually separated from action card by exactly 8px gap. Title text centred.
   - Pressed: destructive button background is `$dangerSurfaceSubtle`, all other geometry identical to the Default frame.

3. `batch_get({ nodeIds: ["discardLabel", "cancelLabel", "addBtn"], readDepth: 1 })`. Confirm:
   - `discardLabel.fill` resolves to `$danger` variable (not raw hex).
   - `cancelLabel.fill` resolves to `$accent`.
   - `addBtn` text content is `Add 2`, not the placeholder.
   - Both `light` and `dark` theme values exist on `$danger` and `$accent` per the get_variables check earlier.

4. `get_screenshot({ nodeId: "discard" })` — one screenshot, scoped to the destructive surface only. This is the surface where pixels matter most: the contrast of the red against the floating-card surface in light mode, the visual rhythm of the action-sheet stack, and the optical centring of the Cancel card's label. I'd skip screenshotting the filter and picker sheets if their structural snapshot looks clean — they're built from library components whose render I trust. If the screenshot shows the red label fails contrast against `$surfaceFloating` in dark mode, I'd `set_variables` to bump `$danger`'s dark-mode value and re-screenshot.

Total screenshots: 1, possibly 2 if the discard surface needs a dark-mode confirmation. Per the skill: routine theme-aware designs don't need a second screenshot; the variable system guarantees parity.

### Step 7 — report

Concise summary of what landed; surface the library candidates (`Sheet` if not already in the lib, `MediaTile` if not, `ActionSheet` and the `ButtonDestructive` variant), name the next states the user might want (picker upload-progress, picker permission-prompt mock, filter empty-state when zero items match, discard-confirmed transition back to home feed), and stop. Per the skill: don't keep polishing past the requirement.

## What I'd ask the user about before opening batch_design (only if signals are absent)

Per the skill's "Request is open-ended" rule, I'd skip the discovery questions if the project has a populated `design-system/` and the prompt names a clear surface. This prompt names "iOS app", "compose flow", "filter selection", "attachments picker", and "discard draft" — all clear. I'd only ask:

- "Does this attach to an existing Compose flow already in the file? If so, what frame should I align style with?" (because the example already establishes a `Mobile / Compose / 01 / Sheet` and `02 / Confirm` pair, and I'd want to match)
- "For the filter, is the selection persisted to the URL or only to component state? It changes whether selecting closes the sheet immediately or keeps it open for multi-select." (my plan assumes single-select-then-close, the iOS-native default)

Both are quick. If the user says "use the Compose pattern from earlier", I extend the `01`/`02` numbering with `03`/`04`/`05`/`06`. If they say "this is a fresh stack", I start at `01`/`02`/`03`/`04` for these four frames.

## Things I deliberately did not do

- I did not mock the iOS system keyboard inside the filter sheet or attachments picker. The filter has no input. The picker's only input affordance is the album switcher dropdown, which is a sub-sheet, not a keyboard.
- I did not design the post-discard transition. The user's prompt scopes to the three sheets/modals, not the return-to-home animation. I'd surface that as a follow-up.
- I did not put the discard option in red AND prefix it with a warning icon. The colour-as-only-signal rule (`SKILL.md` accessibility check #3) is satisfied by the verb "Discard" being the explicit action — colour reinforces but isn't the only signal.
- I did not nest the discard action sheet INSIDE the compose sheet visually. Action sheets stack on the modal layer above any presenting sheet; the underlying compose sheet remains visible but dimmed. Per `interactions.md`: don't nest modals, but a triggered action sheet from a sheet is the OS-conventional layered pattern, not nesting.
- I did not add an undo toast for the discard. Per `interactions.md` § Destructive actions: never combine confirmation and undo. Discard is non-recoverable once committed.

## Confirming the artifact

This response is being saved to `/Users/travis/Development/open-source/pencil-dev-skill/skills/pencil-design-workspace/iteration-1/eval-11-mobile-bottom-sheet-vs-modal/with_skill/outputs/response.md` as my single output artifact.
