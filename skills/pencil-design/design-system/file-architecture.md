# File architecture

The project's chosen `.pen` file structure: which files exist, where they live, what each one owns, and the governance for adding or splitting files. The agent reads this file at session start to know which `.pen` is the source of truth for which surfaces.

This file complements `references/file-architecture.md` (the canonical reference covering Cover frames, section regions, hierarchical naming, and multi-`.pen` decision trees); this file holds the project's specific commitments.

## File set

The project's `.pen` files (commit one per row; expand or trim as the project grows):

| File | Path | Owns | Status |
|---|---|---|---|
| `<product.pen>` | `<repo path or design tool location>` | Core product UI: dashboards, list views, detail pages, settings | `<Discovery / In design / Design review / Engineering review / Ready for build / In build / QA / Shipped>` |
| `<design-system.lib.pen>` | `<path>` | Reusable components: buttons, inputs, cards, modals, etc. Imported by every other `.pen` in the project. | `<status>` |
| `<website.pen>` | `<path>` | Marketing pages: home, pricing, features, about, blog templates | `<status>` |
| `<mobile.pen>` | `<path>` | Native-mobile screens. Add when mobile goes from web-responsive to platform-specific. | `<status>` |
| `<archive.pen>` | `<path>` | Superseded designs kept for historical reference. Never imported. | `<status>` |

Recommended file sets per project size (per `references/file-architecture.md` § Recommended file sets):
- **Early-stage**: `product.pen`, `design-system.lib.pen`, `website.pen`. Three files cover most needs.
- **Growing**: add `mobile.pen` when native-mobile is a separate codebase. Add `archive.pen` when explorations pile up.
- **Large**: split `design-system.lib.pen` into `foundations.lib.pen`, `components.lib.pen`, `patterns.lib.pen` for controlled publishing.

## Naming convention

All `.pen` files follow lowercase-with-hyphens. Library files use the `.lib.pen` suffix so the agent recognises them as importable.

Examples: `product.pen`, `design-system.lib.pen`, `mobile-ios.pen`, `mobile-android.pen`, `marketing-pricing.pen`.

## Hierarchical naming for flows

Multi-screen flows in any `.pen` use slash-delimited names per `references/file-architecture.md` § Hierarchical naming patterns:

`[Area] / [Flow] / [Step] / [Screen] / [State] / [Breakpoint]`

Examples:
- `Reporting / Export / 03 / Configure / ValidationError / Desktop`
- `Auth / SignUp / 01 / Email / Default / Mobile`
- `Settings / Billing / 02 / PaymentMethod / EditMode / Tablet`

Single-screen designs use the simple PascalCase form (`LoginCard`, `Dashboard`, `Settings_Profile`).

## Section regions per `.pen`

Each `.pen` organises its top-level frames into sections, positioned in named canvas regions:

| Section | Canvas region | Holds |
|---|---|---|
| Cover | (0, 0) | The Cover frame: file owner, status, version, scope, links |
| Source of Truth | Row 1 (top, after Cover) | Build-ready, approved frames. Code generation reads from here. |
| Build Ready | Row 2 | Current iteration in flight; about to be promoted |
| UX States | Row 3 | State matrices (loading, empty, error per surface) |
| Responsive | Row 4 | Per-breakpoint variants of Source-of-Truth frames |
| Exploration | Far-right region | Drafts and rejected directions |
| Archive | Bottom region | Superseded designs |

Use `find_empty_space_on_canvas` between sections to honour the regions. Never place an exploration frame in the Source of Truth region; if an exploration gets promoted, move it.

## Cover frame template

Every `.pen` opens with a top-level `Cover` frame at canvas origin. Contents per `references/file-architecture.md` § Cover frame template:

- File owner (name + role)
- Status (one of: Discovery / In design / Design review / Engineering review / Ready for build / In build / QA / Shipped / Deprecated)
- Version
- Last updated (date)
- Scope (in / out): what this file covers and what it explicitly doesn't
- Links: brief, ticket / Linear / Jira, prototype, design-system

The Cover's `context` reads `"File operating manual: owner, status, version, scope, links."`.

## Source-of-truth designation

Code generation and engineering handoff read only from the Source of Truth section. The agent treats:
- **Source of Truth**: canonical for downstream code generation.
- **Build Ready**: about to be promoted; engineering may begin scaffolding.
- **Exploration**: do not generate code from these frames.
- **Archive**: do not generate code; do not import.

When the agent reads a `.pen` file, it identifies which section a target frame lives in via the section's containing parent or canvas position. Frames outside the Source of Truth aren't candidates for handoff.

## Status taxonomy

File-level status (lives in the Cover frame):
- Discovery
- In design
- Design review
- Engineering review
- Ready for build
- In build
- QA
- Shipped
- Deprecated

Component-level status (lives in the component's `context`):
- draft (under construction; don't use yet)
- ready (functional; safe to use; may evolve)
- stable (locked; safe to use long-term)
- needs-review (changed recently; verify before use)
- deprecated (replaced by another component; see `replacedBy: "<componentId>"`)

Per `references/composition-patterns.md` § Component status workflow.

## Library imports

`design-system.lib.pen` is imported by every other `.pen` in the project via the document's `imports` field. Agents check the `imports` list before designing; if the library isn't imported, add it via a `U` op on the document root before instantiating any components.

For multi-library projects, the `imports` list shows the load order. Foundations first (`foundations.lib.pen`), then `components.lib.pen`, then patterns.

## What NOT to put in a `.pen`

Per `references/file-architecture.md` § What NOT to put in a `.pen`:
- Long-form research transcripts (link to external system instead).
- Full PRDs (link to ticket).
- Inspiration boards (use Pinterest / Are.na / Notion).
- Competitor screenshots (use external bookmark / link).
- Presentation decks (use the deck tool of choice).
- Unmaintained component experiments (move to Exploration or delete).

Cross-link from the Cover's links to where these external assets live.

## Multi-`.pen` governance

When to split into multiple files (per `references/file-architecture.md` § Single-`.pen` vs multi-`.pen` decision tree):
- File size grows past ~50 top-level frames or load time exceeds a few seconds.
- Multiple designers are working in parallel and merge conflicts happen weekly.
- The design system needs controlled publishing (versioning, breaking-change discipline).
- Website and product move at different speeds.
- Mobile platform-specific patterns diverge from the web app.

When to keep a single `.pen`:
- Project is early-stage, single designer, < 30 top-level frames.
- The design system is tightly coupled to the product (no other consumers).
- Refactor cost outweighs the benefit (you'd lose history).

## AI-readiness as a meta-principle

Every discipline rule above (Cover frames, section regions, hierarchical naming, status taxonomy) exists partly so the design is machine-readable for downstream AI tools (the next agent that reads the `.pen`, the code-generation step, the design review). The project commits: *we design for AI-assisted handoff as a first-class consumer.*

## Completeness checklists by project type

Per `references/industry-patterns.md` § Completeness pressure tests, the project covers (where applicable):

**SaaS**: roles, permissions, empty states, loading states, error recovery, plan-limit / upgrade states, notification states, admin surfaces (users, billing, integrations, audit).

**Website**: mobile nav, forms with validation, cookie / consent, 404 / 500, SEO heading hierarchy, CMS template behaviour.

**Mobile**: keyboard states, permissions, offline behaviour, native platform patterns, safe areas.

The project ticks the relevant boxes per surface. Missing items flag during design review.

## Verification checklist

Before approving a new `.pen` for the project:

1. Cover frame at (0, 0) with all required fields populated.
2. Section regions present and used (Source of Truth, Build Ready, etc.).
3. Hierarchical naming applied to multi-screen flows.
4. `design-system.lib.pen` imported (check `imports` field).
5. Status reflected in Cover and per component.
6. No Exploration frames in the Source of Truth region (or vice versa).
7. Completeness checklist for the project type ticked off.

## See also

- `references/file-architecture.md` (in the pencil-design skill): the canonical file-architecture reference covering Cover frames, sections, naming, multi-`.pen` decisions.
- `references/composition-patterns.md` (in the pencil-design skill): § Component status workflow.
- `references/industry-patterns.md` (in the pencil-design skill): completeness pressure tests per project type.
- `design-system.md`: the project's design system overview.
- `components.md`: the per-component status table.
