# Translating Linear's issue list into our project

Quick callout before I dive in: no screenshot is attached to this turn, so I can't read the actual pixels. What follows is the protocol I'd run the moment one lands. I'll tell you which references in the skill I'm leaning on at each step, what MCP calls I'd make, and where I'd stop to check with you.

The skill has a specific branch point for exactly this case (SKILL.md, "Design intelligence: when to deviate"):

> **User shows you a reference image.** Read the image, name the layout pattern out loud (e.g. "split-screen with hero left, form right"), and only then plan the tree. Don't skip naming — the model produces visibly better designs when it labels the pattern first.

That naming step is the spine of the whole protocol below. Everything else hangs off it.

---

## Step 1 — Host check + locate context

Before I touch the screenshot at all, I run the standard preamble from the default workflow.

```
get_editor_state({ include_schema: false })
```

What I'm looking for in the response: which `.pen` is open (if any), what's selected, what the document's `imports` field says (because Linear's list is component-heavy and I want to know what's already in your library before I plan).

Failure paths I'd handle here:

- If the host isn't reachable I stop and ask you to open the Pencil desktop app or the Pencil IDE extension. Skill says explicitly not to fall back to the CLI silently.
- If no `.pen` is open I ask: open an existing one, or `open_document("new")` for a fresh file?

Then I check the project filesystem (not via MCP — just a directory listing) for `design-system/`. If it exists I read `README.md`, then `design-system.md` (for the `.lib.pen` path, tech stack, icon library), then `tokens.md` and `components.md`. If it doesn't and this looks like real project work, I'd offer to scaffold once.

## Step 2 — Read the reference image and name the pattern

Now I look at the screenshot. I do this before any guidelines call or component inventory because the layout pattern shapes what guidelines and components matter.

For Linear's issue list specifically, my read out loud would land on something like:

> "Vertical-density data list, left-anchored sidebar, single-column issue rows. Each row: status icon, title, metadata (assignee avatar, labels, priority, project, date). No alternating row stripes; rows separated by hairline dividers. Dense — roughly 36–40px row height. Sticky filter bar on top. Section group-by headers (e.g. 'In Progress · 12') break the list into bands. The whole table reads as a list, not a grid — there are no visible column headers most of the time."

Then I'd call out the specific Linear-isms I'd choose to keep or drop:

- **Keep:** the row density, the inline-edit affordance (everything is clickable in place), the group-by section headers, the keyboard-driven feel (visible focus rings).
- **Translate, don't copy:** the exact icon set (Linear uses a custom mark; we'd use whatever your `iconography.md` declares, almost certainly Lucide or Phosphor), the exact priority pills, the column ordering.
- **Drop:** Linear's specific brand purple, their typography choices, anything that screams "this is Linear" rather than "this is your product".

This is the moment I'd pause and ask you the four questions that have outsized leverage on the final design:

1. What product is this for? (Bug tracker? Task manager? CRM? It changes which fields belong in a row.)
2. Which entity is the row? (Issue, ticket, deal, contact?)
3. Mobile a real target, or desktop-only? (Linear's list pattern doesn't translate cleanly to mobile; on mobile it usually becomes a stacked card list.)
4. Any field types I should infer (priority, status, assignee, due date, labels) from your existing data model?

I would not start designing until I had these answers, even though I'd have plenty of options to invent. The skill is explicit that fabricated metrics and placeholder content are AI tells.

## Step 3 — Load guidelines + inventory components

Now I know it's a data-list / table-shaped UI, so I pick the right `get_guidelines` categories. From the live category list (mcp-tools.md, "Categories live as of 2026-05"):

```
get_guidelines()                         // confirm live category list first
get_guidelines({ category: "Web App" })  // baseline for product UI
get_guidelines({ category: "Table" })    // data-heavy list specifically
```

I'd add `Tailwind` if your `design-system.md` declares Tailwind v4 as the stack. I would *not* load `Design System` here unless I expected to author new components into your `.lib.pen` — and I don't yet, that depends on the inventory.

Then the components-first scan (Discipline rules, "Components first"):

```
batch_get({ patterns: [{ reusable: true }], readDepth: 2 })
```

against the open document, and again with `filePath` set against each `.lib.pen` listed in the document's `imports`:

```
batch_get({
  filePath: "./design/system.lib.pen",
  patterns: [{ reusable: true }],
  readDepth: 2
})
```

What I'm hunting for, in order of importance:

- A `Row` / `ListRow` / `IssueRow` component (most leverage — if it exists I just instantiate it many times)
- A `Badge` / `StatusPill` / `Priority` component for the status indicator
- An `Avatar` component for assignees
- A `Toolbar` / `FilterBar` component for the top chrome
- Any `Sidebar` / `NavRail` for the left side
- An `Icon` / `IconButton` if iconography is wrapped

For any unfamiliar component the inventory surfaces, I'd do the deep read the skill recommends (component-anatomy.md):

```
batch_get({ nodeIds: ["RowComponentId"], readDepth: 4 })
```

And in the result I'd specifically scan for: `slot` frames (content holes I'd fill via `descendants`), top-level child `id` values (those are my primary `descendants` keys), nested children (paths joined with `/`, e.g. `"meta/avatar"`), and any `theme` axes (likely a `state` axis with `default`/`hover`/`focus`/`selected`).

I'd also call `get_variables()` once. Linear's design has a strong neutral palette and a single accent — I want to know what tokens you've already named (`$surface`, `$surfaceMuted`, `$border`, `$textMuted`, `$primary`) so I can bind to existing names instead of either re-declaring (which `set_variables` will silently clobber per the Token Clobber failure mode) or worse, hardcoding raw hex.

## Step 4 — Plan, with the atmosphere named

Per the aesthetic defaults, before any `batch_design` call I commit to a one-line vibe. For a Linear-style list:

> **Dense, symmetric, static.**

That stance forces consistent decisions later: tight gaps (`$space-2` / `$space-3`, not `$space-6`), every row identical in height, no decorative motion. I'd also pick the canonical breakpoint — almost certainly Desktop 1440 first (Linear is a desktop-first product), and I'd flag whether you want Tablet/Mobile companions.

Then I'd state the plan to you before writing any ops. Something like:

> "Building a desktop issue list at 1440 width. Three top-level regions inside the page frame: a 240px `Sidebar` on the left (project nav), a `MainColumn` filling the remainder containing a sticky `Toolbar` (search + filters + view-switcher + new-issue button) and a `IssueList` below. Each issue is a `ref` to your existing `IssueRow` component (or, if absent, a new component I'd add to `.lib.pen` first). Group-by sections render as `SectionHeader` + a stack of rows. I'd use 8 sample issues across 3 sections — no fabricated metrics, just plausible task titles. Light mode primary; dark mode comes free from your variables."

I'd name which existing components I plan to instantiate vs. anything I'd need to build from primitives. If I had to build (say) a `SectionHeader` from primitives because none exists, I'd flag it as a candidate to add to your `.lib.pen` rather than living one-off in this file.

I'd also ask permission before introducing the row component if it doesn't exist. The components-first rule says: surface new patterns rather than silently shipping one-off lookalikes.

Crowded canvas check: if your file already has multiple top-level frames, I'd call `find_empty_space_on_canvas` and pass the returned `x`/`y` on the new page frame's first op — otherwise the new frame can land invisibly under existing content.

## Step 5 — Execute

I'd structure this as 2–3 `batch_design` calls, each ≤25 ops, because cramming 60 ops into one call (per the skill) invites ordering bugs. The shape I'd use:

**Call 1 — page chrome.** The outer page frame, sidebar, main column, toolbar. Bind every node with `foo=I("parent", {...})` so later ops can reference them. Every node gets a meaningful `name` (PascalCase: `IssueListPage`, `Sidebar`, `MainColumn`, `Toolbar`, `FilterStack`, `NewIssueButton`) and a `context` string explaining its role. Colors come from `$variableName` bindings, never raw hex. Auto-layout is structured for fluid resize: sidebar `width: 240`, main column `width: "fill_container"`.

**Call 2 — the list scaffold and section headers.** The `IssueList` frame inside the main column, plus three `SectionHeader` rows ("Todo · 5", "In Progress · 2", "Done · 1"). The list itself uses vertical auto-layout with `gap: 0` (rows are flush, dividers come from a 1px bottom border on each row) and `padding: 0`.

**Call 3 — the rows themselves.** Each row is a `ref` to `IssueRow` with `descendants` overrides for the per-instance content: title text, status icon, priority, assignee avatar, label pills, date. For example:

```
I("IssueList", {
  type: "ref",
  ref: "IssueRow",
  name: "Row_AuthBug",
  context: "Sample row — represents a bug ticket assigned to one user.",
  descendants: {
    "title": { content: "Auth flow throws 500 on Safari < 16" },
    "status/icon": { iconName: "circle-dot" },
    "meta/assignee": { ref: "Avatar", descendants: { "img": { src: "..." } } },
    "meta/priority": { theme: { level: "high" } },
    "meta/date": { content: "Tue" }
  }
})
```

The exact `descendants` paths come from the deep read I did in step 3 — I would have already mapped `title` vs `meta/avatar` vs `meta/priority` from the component's actual structure, not guessed.

A few specific choices that distance us from "copied Linear":

- **Typography.** Whatever your `tokens.md` says. If silent, I'd default to `Geist` + `Geist Mono` per the aesthetic defaults — never `Inter`, which is an AI tell. Linear uses Inter; I'd deliberately not.
- **Accent.** One accent, low saturation, drawn from your `$primary` (or `$accent`) — not Linear's purple.
- **Surfaces.** `$surface` / `$surfaceMuted`, never raw `#FFFFFF` or `#000000`. The skill calls pure black/white "the strongest visual AI tell after Inter."
- **Selected state.** Per `patterns.md`'s list+detail guidance, selected rows get both a background tint AND a 3px left accent bar — subtle hover should not be confusable with selected.
- **Status color is never the only signal.** Each status has an icon shape AND a color, so colorblind users can read the list. (Accessibility rule 3.)
- **Hit targets ≥ 44×44.** Even though rows look dense, the actual click target for action icons inside each row needs to clear 44px. If the visual icon is 16px, the surrounding hit area has to extend.

One thing I would *not* invent: row counts in section headers, fake project names, made-up assignee names. The skill bans `John Doe` / `Acme` / `Lorem Ipsum` placeholder content. I'd ask you for plausible sample content, or use `G(node, "ai", "<prompt>")` for avatar imagery.

## Step 6 — Verify (structural-first, screenshots last)

The skill is emphatic that screenshots are the most expensive thing it does and that I should walk the cheapest-rung-first verification ladder. For this task:

1. **`batch_design` response.** Each call returns success/failure per op. If anything failed, I read the error verbatim and cross-reference `batch-design-grammar.md` — common causes are id-contains-`/`, raw color where a `$variable` was expected, or the older `{sizing: "fill_container"}` object form that the live server now rejects (use the bare string).

2. **`snapshot_layout(parentId: "IssueList", maxDepth: 2)`.** Confirms structural intent in numbers. Did the rows actually stack vertically with the gap I asked for? Are they all the same height? Is the sidebar 240 and the main column the remainder? This is where I catch most layout bugs before they show up in pixels.

3. **`batch_get({ nodeIds: ["Row_AuthBug", "Toolbar", "SectionHeader_InProgress"] })`.** Confirms property-level intent — that `fill` resolved to `$surface` (not a raw hex), that the `ref` actually points at `IssueRow`, that the title text is what I set.

4. **`get_screenshot(nodeId: "IssueListPage")`.** Reserved for the end. Scoped to the page (not the whole canvas), and used to verify: WCAG contrast under real rendering, type rhythm, the overall density read, and how it compares to Linear's screenshot at a glance. Per the dual-mode rule, I'd screenshot the primary mode only — dark mode comes free from variables and doesn't need a re-screenshot unless I made a mistake with raw hex.

When I scan the rendered image I'd run through the five checks in `mcp-tools.md`'s ladder section: layout integrity, spacing rhythm, type rhythm, contrast, and component fidelity (every visual that should be a `ref` to your library is one — no hand-built buttons drifting from `.lib.pen`).

Then the accessibility floor (Discipline rules):

- Body text ≥ 4.5:1 against its background under both modes — verifiable from the variable values themselves without re-rendering.
- Hit targets ≥ 44×44 on every interactive element, even icon-only ones.
- Status conveyed by icon AND color, never color alone.
- `name`s map to roles (`PrimaryAction`, `RowSelectionToggle`).
- The row component has default / hover / focus / selected / disabled states. If the existing component doesn't, I'd flag adding them as a follow-up (skipping focus states ships inaccessible UI).

And the design-completeness check:

- **States** — does the row component actually have hover/focus/selected? Empty state for "no issues match your filter"? Loading skeleton for the initial fetch?
- **Flows** — is "click row → detail view" a separate screen, a side sheet, or in-place expand? Worth pinning down even if I'm not designing the detail screen yet.
- **Accessibility** — keyboard nav order through rows, visible focus, escape to close the toolbar's filter popover.

If a check fails I fix it before reporting done — not as a TODO.

## Step 7 — Hand back

One paragraph: what landed (page frame name + id, the components used, the list count, the breakpoint), the sample content I used and where you can swap real data, anything I noticed that's a candidate for your `.lib.pen` (e.g. "the SectionHeader I built ad-hoc looks reusable — want me to promote it?"), and any design-completeness gaps I flagged but didn't close (e.g. "your `IssueRow` component lacks a focus state — happy to add it as a follow-up").

---

## What I am specifically *not* doing

A few things worth naming so it's clear what "translate, don't copy verbatim" means in practice:

- I'm not pixel-matching Linear's spacing. I'm matching the *atmosphere* (dense, symmetric, static) but binding to your tokens.
- I'm not lifting Linear's icon set, typography, or accent color. I'm lifting the layout pattern.
- I'm not inventing fields you don't have. If your data model doesn't include `priority` or `labels`, those columns don't exist in the row.
- I'm not designing the detail view as a bonus. The brief is the issue list.
- I'm not adding "modern patterns" Linear doesn't use just because they're current — no glassmorphism on the toolbar, no gradient text, no parallax. The skill's "dated defaults" list calls these out as AI tells.

---

## References I consulted (and why)

- **`SKILL.md`** — for the reference-image branch point (Step 2 naming), the discipline rules (Naming, Context, Components first, Themes, Responsive, Accessibility), the aesthetic defaults (atmosphere, color, typography, anti-patterns), the default workflow (steps 1–7), and the verification ladder.
- **`references/component-anatomy.md`** — for how to read the `IssueRow` component once inventory finds it: scanning for slots, building `descendants` paths with `/` for nested children, knowing that `theme: { state: "..." }` activates designed states rather than inventing new ones.
- **`references/modern-patterns.md`** — for the dated-defaults list (so I don't reach for glassmorphism / parallax / three-column grids unprompted), and for the dark-mode rules (no pure inversions, slightly desaturated brand colors).
- **`references/mcp-tools.md`** — for the live `get_guidelines` category list, the decision shortcuts ("data-heavy table → `Table`, `Web App`"), and the verification-tool cost ordering.
- **`assets/design-system/patterns.md`** — for the list+detail conventions specifically: 360px list column on desktop, selected rows get a 3px left accent bar in addition to a background tint, mobile collapses to a push-transition flow.

I did *not* load `references/states.md` or `references/flows.md` for this protocol because the user asked for a layout translation, not a multi-state or multi-screen design. I'd load them in step 6 if the design-completeness check surfaced a need (e.g. "the empty state for filter-with-no-matches isn't designed").

---

## Where I'd pause for your input

Three checkpoints, in order:

1. **After step 2 (pattern named).** I'd confirm the four questions: product context, what the row entity is, mobile target, available field types. No code until those are answered.
2. **After step 4 (plan stated).** I'd confirm component choices — especially if I'm proposing to add a new component to your `.lib.pen` rather than building it inline.
3. **After step 6 final screenshot.** I'd confirm the result reads as "yours" and not "Linear painted with our palette." If it reads too close, the fix is usually in the typography or the accent's saturation, not in the layout.
