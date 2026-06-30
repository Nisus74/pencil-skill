# Example: design a settings page with sidebar nav, autosave, and explicit Save for billing

User says:

> *"Design a settings page for the project. Sections: Profile, Notifications, Billing, Integrations. Autosave by default; explicit Save for Billing."*

Four sections sit on the boundary between tabs and a sidebar. The project's main app already commits to a left sidebar, so the settings page rhymes with that pattern. Three save patterns coexist on the same surface, which means the agent has to make the difference legible without it feeling inconsistent.

---

## Step 1. Read context

Pull the live editor state and the design-system commitments that affect this surface.

```js
get_editor_state({ include_schema: false })
```

Then read the project files. They tell the agent what's already been decided so it doesn't redecide:

- `design-system/visual-style.md`: chosen style, palette, font pairing.
- `design-system/tokens.md`: variable names for colour, spacing, type.
- `design-system/navigation.md`: confirms the project commits to a left-sidebar main nav.
- `design-system/forms.md`: § Save patterns by surface confirms autosave by default plus explicit Save for high-stakes surfaces like Billing.

Inventory the library too:

```js
batch_get({ filePath: "./design/system.lib.pen", patterns: [{ reusable: true }], readDepth: 2 })
```

The library has `Field`, `Toggle`, `Form`, `Button`, `Card`, and a `Banner` component. That's the palette of refs the design will use.

## Step 2. Plan the layout

Reference [`references/layout-patterns.md`](../references/layout-patterns.md) § Settings pages: four sections sits on the boundary between tabs (≤ 6) and sidebar (> 6). Tabs would technically work, but the project's main nav is already a left sidebar, so the settings page reuses that mental model. A nested sidebar inside the settings surface keeps navigation coherent.

Three-column layout: main app sidebar | settings sidebar | settings content. The main app sidebar renders collapsed (icons only) so the settings sidebar gets its proper visual weight.

## Step 3. Find empty space and build the layout shell

Run `FindEmptySpace` as the first line inside the `batch_design` snippet (it returns `{x, y}`), then build the shell:

```js
batch_design({ filePath: "", input: `
const slot = FindEmptySpace({ width: 1440, height: 900, padding: 80, direction: "right" })
page = Insert(document, { type: "frame", name: "Settings", layout: "horizontal", x: slot.x, y: slot.y, width: 1440, height: 900, fill: "$bg", placeholder: true, context: "Settings surface. Three-column: collapsed main nav, settings sidebar, settings content. Profile section is the default route." })
mainNav = Insert(page, { type: "ref", ref: "MainNav", descendants: { state: { value: "collapsed" } }, context: "Collapsed reference to the project's main nav. Renders icon-only in this surface so the settings sidebar gets visual priority." })
settingsNav = Insert(page, { type: "frame", name: "SettingsNav", layout: "vertical", gap: "$space-1", padding: "$space-4", width: 240, fill: "$surface", context: "Settings section list. Active section is highlighted with $accent background; others use $textSecondary." })
settingsContent = Insert(page, { type: "frame", name: "SettingsContent", layout: "vertical", gap: "$space-6", padding: "$space-8", width: "fill_container", height: "fill_container", context: "Slot for the active section's body. Profile section renders here by default." })
` })
```

The settings sidebar's section list is built next as four `LinkText` rows (`Profile`, `Notifications`, `Billing`, `Integrations`), with the active one highlighted.

## Step 4. Build the four sections as sibling frames

Per [`references/file-architecture.md`](../references/file-architecture.md) § Hierarchical naming, each section becomes a sibling top-level frame named with the `Settings_` prefix. They live side-by-side on canvas so an engineer can scrub between them:

- `Settings_Profile`
- `Settings_Notifications`
- `Settings_Billing`
- `Settings_Integrations`

Each frame holds the section's body and gets dropped into `settingsContent` at the appropriate route in code. The agent designs them as siblings so all four are visible simultaneously.

## Step 5. Profile section (autosave)

Avatar upload, display name, email (read-only with edit affordance), timezone. Each field is a `Field` ref with `context` documenting the autosave behaviour.

```js
batch_design({ filePath: "", input: `
profile = Insert(document, { type: "frame", name: "Settings_Profile", layout: "vertical", gap: "$space-6", x: <x1 + 1520>, y: <y1>, width: 720, padding: "$space-8", fill: "$bg", context: "Profile settings. Autosave on blur for every field. Saved indicator appears for 2 seconds, then decays." })
hdr = Insert(profile, { type: "text", name: "SectionHeading", content: "Profile", fontSize: "$text2xl", fontWeight: 700, fill: "$textPrimary" })
avatar = Insert(profile, { type: "ref", ref: "AvatarUpload", descendants: { label: { content: "Profile photo" }, helper: { content: "PNG or JPG, 2MB max." } }, context: "Autosaves on file selection. Uploads via signed URL. Saving spinner replaces avatar during in-flight upload." })
displayName = Insert(profile, { type: "ref", ref: "Field", descendants: { label: { content: "Display name" }, input: { value: "Alex Chen" }, helper: { content: "Visible to teammates and in mentions." } }, context: "Autosaves on blur. Saved indicator appears for 2 seconds, then decays. Validates non-empty, ≤ 60 chars." })
email = Insert(profile, { type: "ref", ref: "Field", descendants: { label: { content: "Email" }, input: { value: "alex@startup.io", readOnly: true }, action: { content: "Change email" } }, context: "Read-only; the action link opens a secure flow with re-auth and verification, that flow lives in Auth / ChangeEmail." })
tz = Insert(profile, { type: "ref", ref: "Select", descendants: { label: { content: "Timezone" }, value: { content: "Australia/Sydney (AEDT)" } }, context: "Autosaves on selection. Used for scheduled digests, due-date calculations, and displayed timestamps." })
` })
```

That's one section done. The other three follow the same shape: a frame, a heading, a stack of refs, every interactive node carrying a `context` that names the behaviour.

## Step 6. Notifications section (autosave)

A toggle list grouped by category. The `context` lives on the section frame because the behaviour is uniform.

```js
batch_design({ filePath: "", input: `
notifs = Insert(document, { type: "frame", name: "Settings_Notifications", layout: "vertical", gap: "$space-6", x: <x1 + 3040>, y: <y1>, width: 720, padding: "$space-8", fill: "$bg", context: "All toggles autosave on change. Saving indicator appears in the section header during in-flight changes; decays once all changes settle." })
nhdr = Insert(notifs, { type: "text", name: "SectionHeading", content: "Notifications", fontSize: "$text2xl", fontWeight: 700, fill: "$textPrimary" })
mentionsGroup = Insert(notifs, { type: "frame", name: "MentionsGroup", layout: "vertical", gap: "$space-3" })
mentionsTitle = Insert(mentionsGroup, { type: "text", content: "Mentions", fontSize: "$textSm", fontWeight: 600, fill: "$textSecondary" })
mEmail = Insert(mentionsGroup, { type: "ref", ref: "Toggle", descendants: { label: { content: "Email me when someone @mentions me" }, value: { checked: true } } })
mPush = Insert(mentionsGroup, { type: "ref", ref: "Toggle", descendants: { label: { content: "Push notify on @mentions" }, value: { checked: true } } })
activityGroup = Insert(notifs, { type: "frame", name: "ActivityGroup", layout: "vertical", gap: "$space-3" })
activityTitle = Insert(activityGroup, { type: "text", content: "Activity", fontSize: "$textSm", fontWeight: 600, fill: "$textSecondary" })
aDigest = Insert(activityGroup, { type: "ref", ref: "Toggle", descendants: { label: { content: "Daily activity digest" }, value: { checked: false } } })
sysGroup = Insert(notifs, { type: "frame", name: "SystemGroup", layout: "vertical", gap: "$space-3" })
systemTitle = Insert(sysGroup, { type: "text", content: "System", fontSize: "$textSm", fontWeight: 600, fill: "$textSecondary" })
sBilling = Insert(sysGroup, { type: "ref", ref: "Toggle", descendants: { label: { content: "Billing receipts" }, value: { checked: true } }, context: "Cannot be disabled in some jurisdictions; legal compliance." })
` })
```

## Step 7. Billing section (explicit Save)

This is the one that's different. A `Form` ref wraps the fields so dirty-state and submit live at the form level, not field-by-field.

```js
batch_design({ filePath: "", input: `
billing = Insert(document, { type: "frame", name: "Settings_Billing", layout: "vertical", gap: "$space-6", x: <x1 + 4560>, y: <y1>, width: 720, padding: "$space-8", fill: "$bg" })
bhdr = Insert(billing, { type: "text", name: "SectionHeading", content: "Billing", fontSize: "$text2xl", fontWeight: 700, fill: "$textPrimary" })
planCard = Insert(billing, { type: "ref", ref: "Card", descendants: { title: { content: "Pro plan" }, body: { content: "$24 per seat per month, billed monthly." }, action: { content: "Change plan" } } })
form = Insert(billing, { type: "ref", ref: "Form", descendants: { label: { content: "Payment and address" }, submitLabel: { content: "Save changes" } }, context: "Explicit save. Dirty state triggers beforeunload warning per forms.md § Unsaved-changes warning. Submit revalidates the card via the payment provider before persisting." })
payment = Insert(form, { type: "ref", ref: "Field", descendants: { label: { content: "Payment method" }, value: { content: "Visa ending 4242" }, action: { content: "Update card" } } })
addrLine1 = Insert(form, { type: "ref", ref: "Field", descendants: { label: { content: "Billing address" }, input: { placeholder: "123 George St" } } })
addrCity = Insert(form, { type: "ref", ref: "Field", descendants: { label: { content: "City" }, input: { placeholder: "Sydney" } } })
addrPost = Insert(form, { type: "ref", ref: "Field", descendants: { label: { content: "Postcode" }, input: { placeholder: "2000" } } })
cancelBlock = Insert(billing, { type: "ref", ref: "DangerZone", descendants: { title: { content: "Cancel subscription" }, body: { content: "You'll keep access until the end of the current billing period." }, action: { content: "Cancel subscription" } }, context: "Confirmation modal before destructive action: type the workspace name to confirm. Per voice.md: irreversible actions name the consequence first." })
` })
```

## Step 8. Integrations section

A card grid of available integrations. Each card has a Connect or Disconnect button depending on state. The empty case (nothing connected) needs its own treatment.

```js
batch_design({ filePath: "", input: `
integ = Insert(document, { type: "frame", name: "Settings_Integrations", layout: "vertical", gap: "$space-6", x: <x1 + 6080>, y: <y1>, width: 720, padding: "$space-8", fill: "$bg" })
ihdr = Insert(integ, { type: "text", name: "SectionHeading", content: "Integrations", fontSize: "$text2xl", fontWeight: 700, fill: "$textPrimary" })
grid = Insert(integ, { type: "frame", name: "IntegrationsGrid", layout: "horizontal", gap: "$space-4" })
slack = Insert(grid, { type: "ref", ref: "IntegrationCard", descendants: { logo: { source: "slack" }, title: { content: "Slack" }, body: { content: "Post updates to a channel." }, action: { content: "Connect" } } })
linear = Insert(grid, { type: "ref", ref: "IntegrationCard", descendants: { logo: { source: "linear" }, title: { content: "Linear" }, body: { content: "Connected to acme-design." }, action: { content: "Disconnect" } } })
github = Insert(grid, { type: "ref", ref: "IntegrationCard", descendants: { logo: { source: "github" }, title: { content: "GitHub" }, body: { content: "Mirror PR comments into threads." }, action: { content: "Connect" } } })
` })
```

For the empty case (nothing connected at all), the section renders the empty-state pattern from [`design-system/empty-states.md`](../design-system/empty-states.md) § Settings: a small illustration, a one-line headline (*"Connect your tools."*), a single explanation, and the same grid below as a teaser. Don't gate the grid behind the empty state, the user needs to see what's available to act.

## Step 9. States to design

Per [`references/states.md`](../references/states.md) § Settings states, the states that matter on this surface:

- **Saved.** Default. No indicator. The absence is the signal.
- **Saving.** Subtle spinner inline next to the field, label *"Saving..."* in `$textSecondary`.
- **Saved-just-now.** Check-mark icon for 2 seconds, then decay to default.
- **Dirty.** Billing form only. Save button enables; *"Unsaved changes"* badge in the page chrome; beforeunload warning fires on navigation.
- **Validation.** Inline error per [`design-system/forms.md`](../design-system/forms.md) § Error display.
- **Conflict.** Banner above the section: *"<Other user> changed this setting <time> ago. <View their version> or <Save anyway>."* Forces a conscious choice; relevant because the project is collaborative.

Build at least the dirty-Billing state and one validation error on Profile as canvas-visible variants so the engineer can read them directly.

## Step 10. Verify with one screenshot

Per `SKILL.md` § Verification ladder, structural verification first:

```js
snapshot_layout({ filePath: "", parentId: page, maxDepth: 3 })
```

Confirm the three columns landed at the right widths (collapsed nav ~64px, settings sidebar 240px, content fills the rest). If geometry's right, take one screenshot of the settings surface in the primary mode:

```js
get_screenshot({ filePath: "", nodeId: page })
```

Verify on the screenshot:

- Sidebar nav reads as a navigation column, distinct from the main app nav next to it.
- The active section is highlighted in `$accent`.
- The autosave indicator is visible on the Profile screenshot (one field showing the saved-just-now check).
- The Billing form's Save button is visible and the *"Unsaved changes"* badge has rendered.
- Validation error on the Profile email field renders inline in `$danger` with the icon.

If anything reads off, fix structurally and re-snapshot. Don't take a second screenshot just to confirm dark mode, the design uses `$tokens` everywhere so the variable system guarantees both modes hold up.

Then strip the placeholder flag:

```js
batch_design({ filePath: "", input: `
Update(page, { placeholder: false })
` })
```

## In Pencil

Five sibling top-level frames placed side-by-side on canvas: `Settings` (the shell with three columns), `Settings_Profile`, `Settings_Notifications`, `Settings_Billing`, `Settings_Integrations`. Profile and Notifications autosave on blur or change with a brief saved-just-now check. Billing uses an explicit `Form` with dirty-state, beforeunload warning, and a confirmation modal on the destructive cancel action. Integrations is a wrapping card grid with empty-state copy when nothing's connected. Every interactive node carries a `context` describing its save behaviour, validation rules, or destructive-action gating, so the engineer reads behaviour directly off the design.

## See also

- [`references/layout-patterns.md`](../references/layout-patterns.md) § Settings pages: tab vs sidebar threshold, autosave default.
- [`references/states.md`](../references/states.md) § Settings states: the six states this surface needs to handle.
- [`references/file-architecture.md`](../references/file-architecture.md) § Hierarchical naming: the `Settings_*` sibling-frame convention for multi-screen flows.
- [`design-system/forms.md`](../design-system/forms.md) § Save patterns by surface and § Unsaved-changes warning.
- [`design-system/navigation.md`](../design-system/navigation.md) § Main nav patterns: why the settings sidebar rhymes with the project's main nav.
- [`design-system/empty-states.md`](../design-system/empty-states.md) § Settings: the no-permission and nothing-connected templates.
- `SKILL.md` § Verification ladder: structural-first verification, one screenshot for sign-off.
