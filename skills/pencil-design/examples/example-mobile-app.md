# Example: design a mobile home screen + Compose flow (iOS)

A worked walkthrough of the seven-step workflow for the prompt:

> *"Design the home screen and a 'Compose' flow for a mobile app. iOS first."*

Assume: Pencil desktop running, no `.pen` open, repo has a `design-system/` folder with `tokens.md`, `mobile.md`, `navigation.md`, `voice.md`, `empty-states.md`, and a `design/system.lib.pen` library that includes `IconButton`, `ButtonPrimary`, `Input`, `TabBarItem`, and `Toast`.

This example exercises:

- iOS safe-area handling on a top-level frame.
- A bottom tab bar with 4 tabs and proper home-indicator clearance.
- A Compose flow as a full sheet with detents.
- Keyboard avoidance, haptic feedback, and inline submit states.
- Cross-references: [`references/mobile-patterns.md`](../references/mobile-patterns.md) for safe areas, sheet detents, keyboard avoidance, and haptics; [`references/file-architecture.md`](../references/file-architecture.md) § Hierarchical naming for the multi-screen layout; [`references/states.md`](../references/states.md) for the loading/success/failure matrix; [`design-system/empty-states.md`](../design-system/empty-states.md) for the first-launch feed.

---

## Step 1. Detect host

```
get_editor_state({ include_schema: false })
```

Result: succeeds. No active document.

## Step 2. Locate context

- No `.pen` open.
- No selection.
- `design-system/` exists with the relevant files.

## Step 3. Load guidelines + inventory components

Read `design-system/README.md`, then `design-system/mobile.md` (the project's mobile commitments: iOS first, Dynamic Type respected, native gestures preserved), `design-system/navigation.md` (commits a 4-tab bottom bar with Home, Search, Notifications, Profile), `design-system/visual-style.md`, and `design-system/tokens.md`. The skill's [`references/mobile-patterns.md`](../references/mobile-patterns.md) is the playbook for safe areas, sheet detents, keyboard handling, and haptic conventions.

Call `get_guidelines()` to confirm the live category list, then load `Mobile App` for native iOS conventions.

Inventory the library:

```
batch_get({ filePath: "./design/system.lib.pen", patterns: [{ reusable: true }], readDepth: 2 })
```

Library has `IconButton`, `ButtonPrimary`, `Input`, `TabBarItem`, `Toast`. No `Sheet` reusable yet, so I'll build the Compose sheet inline and flag it as a library candidate.

## Step 4. Plan (told to user)

> *"I'll create three top-level frames at iPhone 15 dimensions (390×844): `Mobile / Home / Default / iPhone15` shows the feed with a 4-tab bottom bar; `Mobile / Compose / 01 / Sheet / Default / iPhone15` shows the Compose full-sheet at the half detent with the keyboard up; `Mobile / Compose / 02 / Confirm / Default / iPhone15` shows the post-submit toast over the home feed. Safe areas respected on every frame: `env(safe-area-inset-top)` for the status bar, `env(safe-area-inset-bottom)` for the home indicator under the tab bar. Haptics annotated in each component's `context` (selection on tab switch, success on submit, error on failure). The Compose sheet uses a `half` detent by default with `full` available via drag, per your `mobile.md`."*

## Step 4.5. Create the document

Since no `.pen` is open, the user creates a new `.pen` in the editor. The predefined root id is `document`. The library is attached through the editor's import UI; confirm it landed via `get_editor_state`.

## Step 4.7. Place the three frames

Three iPhone-sized frames need ~3 × 390 + gutters of horizontal canvas. Pick anchors with `FindEmptySpace` as the first line inside the `batch_design` snippet (it returns `{x, y}`):

```
batch_design({ filePath: "", input: `
const slot = FindEmptySpace({ width: 390, height: 844, padding: 60, direction: "right" })
// slot.x / slot.y anchor the home frame; the others sit at slot.x + 450 and slot.x + 900.
` })
```

The other frames will sit at `(slot.x + 450, slot.y)` and `(slot.x + 900, slot.y)`. That's 390 wide each plus 60px gutters between, since they represent sequential states an engineer can scrub.

## Step 5a. First batch_design (Home screen)

```
batch_design({ filePath: "", input: `
const slot = FindEmptySpace({ width: 390, height: 844, padding: 60, direction: "right" })
home = Insert(document, { type: "frame", name: "Mobile / Home / Default / iPhone15", layout: "vertical", x: slot.x, y: slot.y, width: 390, height: 844, fill: "$surface", context: "iPhone 15 viewport. Safe areas: top inset 47px (status bar + Dynamic Island), bottom inset 34px (home indicator). Status bar is system-rendered; we leave space for it." })
statusSpacer = Insert(home, { type: "frame", name: "StatusSpacer", height: 47, width: "fill_container" })
header = Insert(home, { type: "frame", name: "Header", layout: "horizontal", justifyContent: "space_between", alignItems: "center", padding: "$space-4", width: "fill_container" })
hTitle = Insert(header, { type: "text", content: "Home", fontSize: "$textXl", fontWeight: 700 })
hSearch = Insert(header, { type: "ref", ref: "IconButton", descendants: { icon: { icon: "search" } }, context: "Selection haptic on tap. Pushes Search tab." })
feed = Insert(home, { type: "frame", name: "Feed", layout: "vertical", gap: "$space-3", padding: "$space-4", width: "fill_container", height: "fill_container" })
post1 = Insert(feed, { type: "frame", name: "Post1", layout: "vertical", gap: "$space-2", padding: "$space-4", cornerRadius: "$radiusLg", fill: "$surfaceMuted", width: "fill_container" })
p1Title = Insert(post1, { type: "text", content: "Mira shipped a new field guide", fontSize: "$textBase", fontWeight: 600 })
p1Body = Insert(post1, { type: "text", content: "Three weeks of edits, finally out the door.", fontSize: "$textSm", fill: "$textMuted" })
post2 = Insert(feed, { type: "frame", name: "Post2", layout: "vertical", gap: "$space-2", padding: "$space-4", cornerRadius: "$radiusLg", fill: "$surfaceMuted", width: "fill_container" })
p2Title = Insert(post2, { type: "text", content: "Reminder: standup at 10", fontSize: "$textBase", fontWeight: 600 })
p2Body = Insert(post2, { type: "text", content: "Bring the prototype on your phone, not your laptop.", fontSize: "$textSm", fill: "$textMuted" })
tabBar = Insert(home, { type: "frame", name: "TabBar", layout: "horizontal", justifyContent: "space_around", alignItems: "center", padding: ["$space-3", "$space-3", 34, "$space-3"], width: "fill_container", fill: "$surface", stroke: "$border", strokeWidth: { top: 1, right: 0, bottom: 0, left: 0 }, context: "Bottom inset 34px for home indicator. Selection haptic on tab change." })
tabHome = Insert(tabBar, { type: "ref", ref: "TabBarItem", descendants: { icon: { icon: "home" }, label: { content: "Home" } }, theme: { state: "active" } })
tabSearch = Insert(tabBar, { type: "ref", ref: "TabBarItem", descendants: { icon: { icon: "search" }, label: { content: "Search" } } })
tabNotif = Insert(tabBar, { type: "ref", ref: "TabBarItem", descendants: { icon: { icon: "bell" }, label: { content: "Notifications" } } })
tabProfile = Insert(tabBar, { type: "ref", ref: "TabBarItem", descendants: { icon: { icon: "user" }, label: { content: "Profile" } } })
` })
```

17 ops. Note:

- `statusSpacer` reserves the 47px iOS top inset. The status bar itself is system-rendered.
- `tabBar`'s 34px bottom padding (the third entry in the `padding` array) clears the home indicator. Labels stay visible at default text size; icon-only mode would fail Dynamic Type.
- Active tab uses the `active` theme state on `TabBarItem` (filled icon + `$accent` label). Inactive tabs render the default outlined-icon styling.
- Selection haptic documented in the tab bar's `context`.

## Step 6a. Verify structure (Home)

```
snapshot_layout({ filePath: "", parentId: home, maxDepth: 3 })
```

Check: status spacer at top (47px), header centered with title left and search right, feed fills the middle, tab bar pinned to the bottom with 34px clearance below the icons. No content rendering under the home indicator. Tab labels visible. Per `references/mobile-patterns.md` § Tab bars, that's the contract.

## Step 5b. Second batch_design (Compose sheet at half detent, keyboard up)

The Compose flow uses a full sheet rather than a peek sheet, since the user is writing content and submitting. That fits the modal-shape decision in `references/mobile-patterns.md` § Bottom sheets vs modals. Default detent is `half`; the user can drag to `full` for long-form. Edge-swipe dismisses.

```
batch_design({ filePath: "", input: `
compose = Insert(document, { type: "frame", name: "Mobile / Compose / 01 / Sheet / Default / iPhone15", layout: "vertical", x: slot.x + 450, y: slot.y, width: 390, height: 844, fill: "$scrim", context: "Compose full-sheet at half detent (~50% viewport height). Keyboard is up (336px). Edge-swipe down dismisses with autosaved draft." })
backdrop = Insert(compose, { type: "frame", name: "BackdropTap", width: "fill_container", height: 422, context: "Tap to dismiss. Edge-swipe also dismisses." })
sheet = Insert(compose, { type: "frame", name: "Sheet", layout: "vertical", width: "fill_container", height: 422, cornerRadius: ["$radiusXl", "$radiusXl", 0, 0], fill: "$surface", context: "Half detent. Drag handle indicates draggability to full detent." })
grabber = Insert(sheet, { type: "frame", name: "Grabber", width: 36, height: 5, cornerRadius: 2.5, fill: "$border", context: "Centered drag handle." })
sheetHeader = Insert(sheet, { type: "frame", name: "SheetHeader", layout: "horizontal", justifyContent: "space_between", alignItems: "center", padding: "$space-4", width: "fill_container" })
cancel = Insert(sheetHeader, { type: "ref", ref: "LinkText", descendants: { label: { content: "Cancel" } }, context: "Dismisses sheet. Confirms discard if draft is non-empty." })
sheetTitle = Insert(sheetHeader, { type: "text", content: "New post", fontSize: "$textBase", fontWeight: 600 })
submit = Insert(sheetHeader, { type: "ref", ref: "ButtonPrimary", descendants: { label: { content: "Post" } }, context: "Disabled until content is non-empty. Success haptic on submit. Error haptic on failure. Stays accessible above the keyboard." })
body = Insert(sheet, { type: "frame", name: "Body", layout: "vertical", gap: "$space-3", padding: "$space-4", width: "fill_container", height: "fill_container" })
textArea = Insert(body, { type: "ref", ref: "Input", descendants: { input: { placeholder: "What's on your mind?", multiline: true, value: "Just got back from the river ride. The new bridge path is" } }, theme: { state: "focus" }, context: "Autosaves draft locally on every keystroke. Restored on next sheet open." })
tagRow = Insert(body, { type: "frame", name: "TagRow", layout: "horizontal", gap: "$space-2", width: "fill_container" })
tagBtn = Insert(tagRow, { type: "ref", ref: "IconButton", descendants: { icon: { icon: "tag" } }, context: "Opens tag picker." })
attachBtn = Insert(tagRow, { type: "ref", ref: "IconButton", descendants: { icon: { icon: "image" } }, context: "Opens iOS image picker. Triggers permission prompt on first use." })
keyboard = Insert(compose, { type: "frame", name: "Keyboard", width: "fill_container", height: 336, fill: "$surfaceMuted", context: "iOS system keyboard placeholder. Accessory bar with 'Done' to dismiss sits at its top edge." })
accessory = Insert(keyboard, { type: "frame", name: "AccessoryBar", layout: "horizontal", justifyContent: "end", padding: "$space-3", width: "fill_container" })
done = Insert(accessory, { type: "ref", ref: "LinkText", descendants: { label: { content: "Done" } }, context: "Dismisses keyboard, sheet stays at half detent." })
` })
```

16 ops. Note:

- The focused text area is shown with content already typed, per the SKILL.md aesthetic-defaults discipline. A blank focused input doesn't pressure-test anything.
- Submit button stays in the header row, accessible above the keyboard. Per `references/mobile-patterns.md` § Input keyboard avoidance.
- Haptics documented in `submit`'s `context`: success on post, error on failure, selection on tab switches in the wider app.
- Cancel uses the iOS-conventional left placement; submit on the right.

## Step 6b. Verify structure (Compose)

```
snapshot_layout({ filePath: "", parentId: compose, maxDepth: 3 })
```

Check: sheet height 422 (half of 844), keyboard height 336, backdrop fills the gap (844 - 422 - 336 = 86 ≈ status area). The text area sits above the keyboard with no overlap. Submit button is reachable in the header row. Grabber centered horizontally.

If the sheet's text area extends under the keyboard (a common bug), it's structural:

```
batch_design({ filePath: "", input: `Update(body, { height: "fill_container" })` })
```

The flex layout now distributes the remaining sheet height to the body, keeping the input visible.

## Step 5c. Third batch_design (post-submit confirm)

The success state per `references/states.md` is: sheet dismisses, toast appears over the home feed, success haptic fires. Frame 03 captures that moment.

```
batch_design({ filePath: "", input: `
confirm = Insert(document, { type: "frame", name: "Mobile / Compose / 02 / Confirm / Default / iPhone15", layout: "vertical", x: slot.x + 900, y: slot.y, width: 390, height: 844, fill: "$surface", context: "Post-submit. Sheet has dismissed. Toast confirms. Success haptic fires on appearance." })
` })
```

Then copy the home frame's content and overlay a toast near the top of the safe area:

```
batch_design({ filePath: "", input: `
homeCopy = Copy(home, confirm)
toast = Insert(confirm, { type: "ref", ref: "Toast", descendants: { icon: { icon: "check-circle" }, label: { content: "Posted." } }, x: 16, y: 60, width: 358, theme: { state: "success" }, context: "Success haptic on appearance. Auto-dismiss after 2s. Tappable to dismiss early." })
` })
```

3 ops. The toast lands just below the status bar, full-bleed minus 16px gutters. Copy is one word: *"Posted."* Specific past-tense confirmation, no exclamation, no clichés.

## Step 6c. Verify structure (Confirm)

```
snapshot_layout({ filePath: "", parentId: confirm, maxDepth: 2 })
```

Check: home content underneath, toast at `y: 60` (clears the 47px status spacer with 13px breathing room). Toast width 358 (390 - 32 gutters).

## Step 7. Final visual sign-off

Three pages, three screenshots. Each scoped to its own page node so the doc root stays out of the capture:

```
get_screenshot({ filePath: "", nodeId: home })
get_screenshot({ filePath: "", nodeId: compose })
get_screenshot({ filePath: "", nodeId: confirm })
```

Verify per page:

- **Home.** Status area clear. Header reads cleanly. Feed posts render with consistent spacing. Tab bar is visible above the home indicator with all four labels showing. Active tab highlighted in `$accent`.
- **Compose.** Sheet at half detent, grabber centered, keyboard occupying the bottom 336px with the accessory bar visible. Focused text area with sample content sits above the keyboard. Submit button reachable in the header.
- **Confirm.** Toast renders near the top with `$success` styling and the *"Posted."* label. Home content visible underneath.

Three screenshots total, one per page.

## Step 8. Surface candidates and notes

Three notes for the user:

1. **`Sheet` is a library candidate.** The Compose sheet is currently composed from primitives. Surface it: *"The Compose sheet (grabber, header row, body, keyboard spacer) is built from primitives here. Want me to promote it to your `.lib.pen` as `Sheet` with detent variants for half, full, and peek?"*
2. **States to design separately.** The submit-loading state (sheet stays, button shows spinner), submit-failure state (sheet stays, inline error using the *"what happened. what to do."* template from `voice.md`), and the empty-feed first-launch state (per `empty-states.md`) deserve their own frames. Surface them as next steps.
3. **Mobile-specific completeness checklist.** Per `references/industry-patterns.md` § Mobile pressure test: splash screen, first-launch onboarding, permission prompts (notifications, camera), offline state (feed unavailable, draft saved locally), push notification appearance. Each gets its own frame when the user's ready.

## Final report to user

> *"Done. Three sibling frames at iPhone 15 dimensions, placed in empty canvas. `Mobile / Home / Default / iPhone15` shows the feed with a 4-tab bottom bar respecting the home indicator. `Mobile / Compose / 01 / Sheet / Default / iPhone15` shows the Compose full-sheet at the half detent with the keyboard up, submit reachable in the header, and a focused text area carrying sample content. `Mobile / Compose / 02 / Confirm / Default / iPhone15` shows the success toast over the home feed. Safe areas respected throughout (47px top, 34px bottom). Haptics documented in `context`. Verified structurally with `snapshot_layout` per page, then one screenshot per page for sign-off. See the notes below for follow-ups on the `Sheet` library candidate and the unfinished submit states."*

## What this example demonstrates

- **iOS safe-area handling** on top-level mobile frames: top spacer for the status bar and Dynamic Island, bottom padding on the tab bar for the home indicator.
- **A full sheet with detents** for a compose flow, with the keyboard rendered inline so layout pressure is visible on the canvas. The submit affordance stays reachable in the header above the keyboard.
- **Haptics documented in `context`** so the engineer ships matching behaviour without a separate spec.
- **Sequential states as sibling frames** an engineer can scrub through, including the post-submit confirmation moment.

## See also

- [`references/mobile-patterns.md`](../references/mobile-patterns.md) for safe areas, sheet detents, keyboard avoidance, and haptics.
- [`references/states.md`](../references/states.md) for the loading, success, failure, and empty-state matrix.
- [`references/industry-patterns.md`](../references/industry-patterns.md) § Mobile pressure test for splash, permissions, offline, and push notifications.
- [`references/file-architecture.md`](../references/file-architecture.md) § Hierarchical naming for the `Mobile / Compose / 01 / Sheet / Default / iPhone15` shape.
- [`design-system/mobile.md`](../design-system/mobile.md) and [`design-system/navigation.md`](../design-system/navigation.md) for the project's mobile and tab-bar commitments.
