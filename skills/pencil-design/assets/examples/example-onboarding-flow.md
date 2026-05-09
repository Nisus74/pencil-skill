# Example: design a three-step onboarding flow with progress, skip, and sample data

User says:

> *"Build the onboarding flow. Three steps after signup: workspace name, role, sample-data choice. Each skippable. Show progress."*

This example shows the agent designing a multi-step onboarding flow with progress indication, skip affordances, and the sample-data-vs-blank-slate routing.

---

## Step 1: Read context

```js
get_editor_state();
```

The agent reads `assets/design-system/visual-style.md`, `tokens.md`, `forms.md` (project's form patterns), `onboarding.md` (project commits guided onboarding with sample-data option), and `voice.md` (microcopy tone). Loads `references/flows.md` § Onboarding flows, § Multi-step forms / wizards, and `references/states.md` § Onboarding states.

## Step 2: Plan the screens

Per `references/file-architecture.md` § Hierarchical naming:

- `Onboarding / 01 / WorkspaceName / Default / Desktop`
- `Onboarding / 02 / Role / Default / Desktop`
- `Onboarding / 03 / SampleData / Default / Desktop`
- `Onboarding / Welcome / Default / Desktop` (optional first screen before step 1)
- `Onboarding / 03 / SampleData / SampleSelected / Desktop`
- `Onboarding / 03 / SampleData / BlankSelected / Desktop`

Sibling top-level frames per step + state.

## Step 3: Find canvas space and create the wizard wrapper

```js
find_empty_space_on_canvas({ documentId, width: 1440, height: 900 });
```

Build a `WizardLayout` reusable that holds the progress indicator, content slot, and footer (Back / Continue / Skip). Each onboarding step instantiates `WizardLayout` with the step's content in the slot.

```js
batch_design({
  documentId,
  ops: [
    {
      op: "C",
      parent: "<canvas-root-id>",
      node: {
        type: "frame",
        name: "Onboarding_01_WorkspaceName",
        context: "Onboarding step 1 of 3. Workspace name input. Skippable. Progress indicator: stepper, 1/3 active. Footer: Back disabled (first step), Continue primary, Skip text-link.",
        children: [
          { type: "ref", componentId: "WizardLayout", descendants: { progress: "1/3", content: "<step-1-form>", canSkip: true } },
        ],
      },
    },
  ],
});
```

## Step 4: Pick the progress indicator

Per `references/flows.md` § Multi-step forms § Step indicator: three shapes.

- Stepper (numbered circles, dots, or labels): right for 2-5 steps where the user can see the destination.
- Progress bar: right for 6+ steps or when the count varies per user.
- Step counter ('Step 2 of 4'): right for very simple flows.

For three steps, use a stepper. Active step: filled circle; completed step: filled with check; upcoming: outlined.

## Step 5: Build step 1 (workspace name)

Single text input. Auto-focused on screen entry. Helper text below input: 'You can change this later in settings.'

```js
batch_design({
  documentId,
  ops: [
    {
      op: "C",
      parent: "<step-1-content-slot>",
      node: {
        type: "frame",
        name: "Step1_Form",
        children: [
          { type: "text", text: "What's your workspace called?", fontFamily: "$fontDisplay", fontWeight: "$fontWeightBold" },
          { type: "text", text: "This is the name your team will see.", fontFamily: "$fontBody", color: "$textSecondary" },
          { type: "ref", componentId: "Field", descendants: { label: "Workspace name", input: "<text-input>", helper: "You can change this later in settings." } },
        ],
      },
    },
  ],
});
```

Validation per `assets/design-system/forms.md` § Validation timing: on-blur for sync constraints (length ≥ 1, max 50 chars). On Continue: validate, focus first error if any, advance if clean.

## Step 6: Build step 2 (role)

Choose from a list of roles (Admin, Editor, Viewer, etc.). Use radio buttons or a tile grid depending on count.

For ≤ 4 roles, use tile grid (each role as a card with icon + label + description). For 5+, use a list.

```js
batch_design({
  documentId,
  ops: [
    {
      op: "C",
      parent: "<step-2-content-slot>",
      node: {
        type: "frame",
        name: "Step2_RoleGrid",
        layout: { direction: "row", gap: 16 },
        children: [
          { type: "ref", componentId: "RoleTile", descendants: { icon: "shield-star", label: "Admin", description: "Full access to settings, members, billing." } },
          { type: "ref", componentId: "RoleTile", descendants: { icon: "edit", label: "Editor", description: "Create and edit content." } },
          { type: "ref", componentId: "RoleTile", descendants: { icon: "eye", label: "Viewer", description: "Read-only access." } },
        ],
      },
    },
  ],
});
```

Selection state on `RoleTile`: `$accent` border + `$accentMuted` background.

## Step 7: Build step 3 (sample data choice)

Two-option choice: 'Start with sample data' or 'Start blank'.

```js
batch_design({
  documentId,
  ops: [
    {
      op: "C",
      parent: "<step-3-content-slot>",
      node: {
        type: "frame",
        name: "Step3_SampleDataChoice",
        layout: { direction: "row", gap: 16 },
        children: [
          { type: "ref", componentId: "OptionCard", descendants: {
            icon: "sparkles",
            label: "Start with sample data",
            description: "Pre-populated workspace with realistic example projects. Replace anytime.",
            badge: "Recommended for first-time users",
          }},
          { type: "ref", componentId: "OptionCard", descendants: {
            icon: "layout-grid",
            label: "Start blank",
            description: "Empty workspace. Create your first project right away.",
          }},
        ],
      },
    },
  ],
});
```

Per `assets/design-system/onboarding.md` § With sample data vs blank slate: most products benefit from offering both. Sample data leans toward Recommended for first-time users.

## Step 8: Skip and back affordances

Per `assets/design-system/onboarding.md` § Skip and exit affordances:

- **Back**: disabled on step 1; enabled from step 2 onwards. Clicking Back returns to the previous step with values preserved.
- **Skip**: text link 'Skip' bottom-right of the footer. Available on every step except where skipping breaks the flow (e.g. workspace name might be required).
- **Skip-all**: from any step, returns to a sensible default (typically the empty state of the primary surface).

## Step 9: Persist progress

Per `assets/design-system/onboarding.md` § Save-progress on exit: silently persist progress; resume on next launch. Don't ask 'Save your progress?' on exit.

The design's `context` documents the persistence: *'Workspace name auto-saves on blur to local storage. Progress restored if user closes and reopens.'*

## Step 10: Welcome screen (optional)

If the project ships a welcome screen before step 1: full-screen takeover or centred modal, brand voice, single primary action 'Get started'. Optional 'I'll do this later' link.

```js
batch_design({
  documentId,
  ops: [
    {
      op: "C",
      parent: "<canvas-root-id>",
      node: {
        type: "frame",
        name: "Onboarding_Welcome",
        context: "Welcome screen. Brand voice. Single primary action 'Get started'. Optional 'I'll do this later' text link routes to empty state of the primary surface.",
        children: [
          { type: "text", text: "Welcome to <Product>", fontFamily: "$fontDisplay", fontWeight: "$fontWeightBold" },
          { type: "text", text: "Three quick steps to set up your workspace.", color: "$textSecondary" },
          { type: "ref", componentId: "Button.Primary", descendants: { label: "Get started" } },
          { type: "ref", componentId: "TextLink", descendants: { label: "I'll do this later" } },
        ],
      },
    },
  ],
});
```

## Step 11: States to design

Per `references/states.md` § Onboarding states:

- Welcome state.
- Each step's default state.
- Each step's validation-error state (where applicable).
- Loading state (when step submission is in flight).
- Sample-data routing: post-completion screen showing the populated workspace.
- Blank-slate routing: post-completion screen showing the empty primary surface with first-action prompt.
- Coach marks (optional) on the first surface after onboarding for non-obvious features.

## Step 12: Verify with screenshots

```js
get_screenshot({ documentId, nodeId: "<step-1-frame-id>" });
get_screenshot({ documentId, nodeId: "<step-2-frame-id>" });
get_screenshot({ documentId, nodeId: "<step-3-frame-id>" });
```

Confirm:
- Stepper shows current / completed / upcoming distinctly.
- Each step's primary input is auto-focused.
- Continue button is the only primary action per step.
- Skip link visible but secondary.
- Back disabled on step 1; enabled later.
- Validation errors show inline; focus moves to first error on submit.

Walk through the flow as a new user. Note any friction (per `assets/design-system/onboarding.md` § Verification checklist).

## See also

- `references/flows.md` § Onboarding flows, § Multi-step forms / wizards.
- `references/states.md` § Onboarding states.
- `references/microcopy.md` § Empty state copy (also applies to onboarding prompts).
- `assets/design-system/onboarding.md`: project's onboarding commitments.
- `assets/design-system/forms.md`: validation timing, error display.
- `assets/design-system/voice.md`: tone for welcome, encouragement, skip copy.
- `assets/examples/example-form-flow.md`: multi-step signup with email verification (overlaps onboarding pattern).
