# File architecture

How `.pen` files are organised, at the single-file level (frame regions, naming, status) and at the project level (one `.pen` vs many, what each file owns, when to split). The discipline is what keeps a project navigable as it grows from a one-page sketch to a multi-team product surface.

**What this file owns:** the Cover frame template, the section-region layout (SourceOfTruth / BuildReady / UXStates / Responsive / Exploration / Archive), hierarchical naming patterns for multi-screen flows, file-level and component-level status taxonomies, single-`.pen` vs multi-`.pen` decision tree, what NOT to put in a `.pen`, completeness checklists per project type (SaaS / Website / Mobile), AI-readiness as a meta-principle.

**What this file does NOT own:** the discipline rules themselves (Cover frame, section frames, hierarchical naming). Those live in SKILL.md § File architecture and apply unconditionally. The schema for `.lib.pen` libraries lives in [`pen-schema.md`](pen-schema.md). When to load each reference file lives in SKILL.md § Design intelligence: when to deviate.

## When to load this file

- You're starting a new `.pen` for a real project (not a one-off sketch).
- The project has multiple screens, multiple flows, or multiple contributors.
- The user names *file structure*, *file architecture*, *cover frame*, *source of truth*, *exploration*, *archive*, *split files*, *design system file*, *governance*, *handoff*.
- You're auditing a `.pen` that's grown organically and is becoming hard to navigate.
- You're scaffolding a project's design system and need to decide on file layout.

## The Cover frame

Every `.pen` file opens with a top-level frame named `Cover`, positioned at canvas origin `(0, 0)` (or close to it; leave room above and to the left if the canvas already has content). The Cover answers, in under 30 seconds, *"is this safe to build from?"*.

**Required fields** (each as a child text node inside the Cover frame):

- **Owner.** File owner / design lead. *"Owner: Alex Chen, Product Design"*.
- **Status.** Current file-level status (see taxonomy below). *"Status: Ready for build"*.
- **Version.** Semver or date-stamp. *"Version: 1.4.2"*.
- **Last updated.** ISO date. *"Last updated: 2026-05-09"*.
- **Scope (in).** What this file covers. *"In scope: signup flow, sign-in, password reset, MFA setup."*.
- **Scope (out).** What this file deliberately does NOT cover. *"Out of scope: SSO admin config (separate file), enterprise account provisioning."*.
- **Links.** Brief, ticket, prototype, design system. Each as `Label: URL`.

**Status taxonomy (file-level):**

| Status | Meaning |
|--------|---------|
| `Discovery` | Research, sketches, exploration. Not yet design. |
| `In design` | Active design work. Not yet reviewed. |
| `Design review` | Awaiting design review. |
| `Engineering review` | Awaiting engineering / handoff review. |
| `Ready for build` | Approved, source of truth. Engineers can build from this. |
| `In build` | Engineering is implementing. Design changes need coordination. |
| `QA` | Built; design reviewing the implementation. |
| `Shipped` | In production. The file is now historical reference. |
| `Deprecated` | No longer accurate. Either updated, replaced, or sunset. |

**Recommended Cover `context`:** *"File operating manual: owner, status, version, scope, links. Read first to determine if this file is safe to build from and what's in or out of scope."*

**Cover frame layout.** A simple two-column layout works: labels on the left (`Owner:`, `Status:`, `Version:`, `Last updated:`, `In scope:`, `Out of scope:`, `Links:`), values on the right. Use the project's `tokens.md` if present; otherwise default to `$textBase` for labels and `$textBase` bold for values. Keep the Cover frame ≤ 800px wide so the whole thing reads at a glance.

**Backfill a Cover when you open a `.pen` without one.** The cost is one frame plus a few text children; the value is permanent. Place it before any other content, document the file's *current* status, and surface to the user: *"This file didn't have a Cover. I added one with my best guess at status, please review the fields."*

## Section frames as canvas regions

Top-level frames (siblings of the Cover) belong in named *section regions* on the canvas. Each region is a logical group; not a literal `frame` containing children, but a spatial region you keep your section frames within. Use `find_empty_space_on_canvas` between regions so they don't overlap.

**The standard regions** (in canvas-position order from top-left):

| Region | Purpose | Canvas position |
|--------|---------|-----------------|
| `Cover` | The Cover frame. | `(0, 0)` |
| `SourceOfTruth` | Approved current designs. The canonical reference for engineering. | Right of Cover, top row |
| `BuildReady` | Current iteration in active design / awaiting review. Will become SourceOfTruth on approval. | Below SourceOfTruth |
| `UXStates` | State matrices (loading / empty / error / partial) for components in SourceOfTruth. | Below BuildReady |
| `Responsive` | Per-breakpoint frames for designs that ship across viewport sizes. | Below UXStates or to the right of SourceOfTruth |
| `Exploration` | Drafts, rejected directions, design alternatives. NOT canonical. | Far-right region of canvas |
| `Archive` | Superseded designs kept for historical reference. NOT canonical. | Bottom region of canvas |

**The discipline:** a frame in the SourceOfTruth region is approved; a frame in Exploration sits outside that approval. The agent (and the next teammate) can answer "which is canonical?" by checking which region a frame sits in. Code generators and downstream tools should *only* generate from SourceOfTruth.

**Mark each region with a header.** Place a large heading text node in canvas space at the top of each region: `── SOURCE OF TRUTH ──`, `── EXPLORATION ──`. Plain visual separators. Cheap to add; impossible to misread.

**Promotion: never dual-track.** When you promote an exploration to SourceOfTruth, *move* the frame; don't copy it. Two versions of the same screen in different regions is exactly the bug this discipline prevents. The exception: if you want to preserve the exploration as a record of an alternative considered, *move it to Archive* simultaneously.

**Per-task workflow:**

- New design (greenfield): create the frame in `BuildReady`. On review-approval, move it to `SourceOfTruth`.
- Editing approved design: move the SourceOfTruth frame to `BuildReady`, edit, on approval move it back to `SourceOfTruth`. The SourceOfTruth region should never contain in-flight work.
- Exploration: create in `Exploration`. On promotion, move to `BuildReady` (or directly to `SourceOfTruth` for trivial picks).
- Sunsetting: move the SourceOfTruth frame to `Archive` and document why in the frame's `context`.

This sounds heavyweight; it isn't. The first time someone (or a downstream tool) asks "is this frame canonical?", the discipline pays for itself.

## Hierarchical naming for multi-screen flows

SKILL.md § Naming requires PascalCase, semantic names. For multi-screen flows, extend with a `/`-delimited path:

```
[Area] / [Flow] / [Step] / [Screen] / [State] / [Breakpoint]
```

Examples:

```
Auth / SignUp / 01 / EmailEntry / Default / Desktop
Auth / SignUp / 01 / EmailEntry / ValidationError / Desktop
Auth / SignUp / 02 / EmailVerify / Sent / Desktop
Auth / SignUp / 02 / EmailVerify / VerifyExpired / Desktop
Auth / SignUp / 03 / Welcome / Default / Desktop

Reporting / Export / 03 / Configure / Default / Desktop
Reporting / Export / 03 / Configure / ValidationError / Desktop
Reporting / Export / 04 / InProgress / Loading / Desktop
Reporting / Export / 05 / Complete / Success / Desktop

Onboarding / FirstLaunch / 01 / Welcome / Default / Mobile
Onboarding / FirstLaunch / 02 / PermissionRequest / Default / Mobile
Onboarding / FirstLaunch / 02 / PermissionRequest / Denied / Mobile
Onboarding / FirstLaunch / 03 / TourStart / Default / Mobile
```

**Rules:**

- **Slashes are forbidden in `id` (the schema rejects them) but allowed and recommended in `name`.**
- **Step numbers are zero-padded to two digits** (`01`, `02`, `12`) so alphabetical sort matches step order even for flows with > 9 steps.
- **State is a state from [`states.md`](states.md)**: `Default`, `Hover`, `Focus`, `Loading`, `Empty`, `Error`, `Success`, `ValidationError`, `Sent`, `VerifyExpired`, `PermissionDenied`, etc.
- **Breakpoint is one of the canonical labels**: `Mobile`, `Tablet`, `Desktop` (or `iOS` / `Android` for native designs that diverge by platform).

**Single-screen designs keep the simple PascalCase form** (`LoginCard`, `PricingCard`, `HeroSection`). The hierarchical path is for *multi-screen flows* where you need to navigate dozens of related frames.

**Section prefixes** are useful when one `.pen` covers multiple unrelated areas: prefix with the section region:

```
SourceOfTruth: Auth / SignUp / 01 / EmailEntry / Default / Desktop
Exploration:   Auth / SignUp / 01 / EmailEntry / Alternative-magic-link / Desktop
```

Optional but useful for very large files.

## Component status (re-stated)

Per `composition-patterns.md` § Component status workflow, every reusable component carries a status in its `context`:

| Status | Meaning |
|--------|---------|
| `draft` | Work in progress. Don't use in canonical designs. |
| `ready` | New, functional, limited adoption. Safe to use; report bugs. |
| `stable` | Battle-tested. Default choice. |
| `needs-review` | Tech-debt accumulated. Avoid new uses. |
| `deprecated` | Replaced. Migrate. |

This is component-level status, distinct from the file-level status on the Cover.

## Single `.pen` vs multi-`.pen`: the decision tree

Start with one `.pen` per project. Split when one or more of these signals fires:

- **File size / load time.** The `.pen` takes more than a few seconds to open or render. The MCP server warns about read budgets. Split by section.
- **Multiple designers blocking each other.** Two designers want to work on the marketing site and the product app simultaneously. Split files.
- **Different speeds of change.** The product app changes weekly; the marketing site changes monthly; the design system changes when components are added. Different cadences mean different files.
- **Different audiences for handoff.** Marketing handoff goes to a different engineering team than product handoff. Different files reduce accidental cross-pollution.
- **Mobile-specific patterns diverge.** When mobile design is just "responsive desktop", one file. When mobile uses native conventions (sheets, gestures, safe areas, platform-specific patterns), the divergence justifies a separate `mobile.pen`.
- **Design system needs controlled publishing.** When components in the `.lib.pen` change in ways that affect downstream files, you want the `.lib.pen` versioned and published independently. Split into a dedicated library file.
- **Archive is polluting active decisions.** When old work in the same file makes it hard to find current work. Move historical material to a dedicated `archive.pen`.

The worst structure is one giant file holding all SaaS app screens, marketing pages, mobile flows, every component, every old version, and every research artifact. *"Comprehensive"* in this case becomes *"unnavigable."*

## Recommended file sets by project size

**Early-stage (one designer, one product):**

```
product.pen          ← the SaaS / app design
website.pen          ← marketing site (only when there is one)
design-system.lib.pen ← shared components and variables
```

Three files. Each owns its domain. The `.lib.pen` is imported by the others.

**Growing (small team, mobile + web):**

```
product.pen          ← web app
mobile.pen           ← native mobile app (iOS + Android share where they can; per-platform Build Ready sections where they diverge)
website.pen          ← marketing site
design-system.lib.pen ← components and variables shared across all three
archive.pen          ← shipped + deprecated reference
```

Five files. Same principle; `mobile.pen` separates because mobile patterns diverge from web; `archive.pen` separates because shipped work pollutes active decisions.

**Large (multi-team, multi-product):**

```
foundations.lib.pen  ← colour, type, spacing tokens; primitives
components.lib.pen   ← Button, Card, Input, Modal. Imports foundations
patterns.lib.pen     ← Onboarding, Empty states, Error recovery. Imports foundations + components
product-app.pen      ← SaaS product, imports all three .lib.pens
mobile-app.pen       ← Mobile, imports all three .lib.pens
website-marketing.pen ← Marketing, imports foundations + components
website-app.pen      ← Logged-in web app surfaces, imports all three
prototypes.pen       ← Click-through prototypes for usability testing
archive-2026-q1.pen  ← Shipped Q1 reference
archive-2026-q2.pen  ← Shipped Q2 reference
```

Many files; each owns one job; each is fast to load and easy to govern.

**Don't split prematurely.** If you have one designer and one product, three files is overhead. Start with one `.pen` and split when a signal above fires.

## What NOT to put in a `.pen`

A `.pen` is for design work the engineer can read and the next agent can understand. Things that don't belong:

- **Long-form research transcripts.** Use Notion / Confluence / Coda. Link to them from the Cover.
- **Full PRDs.** Same. The Cover links the brief; the brief lives elsewhere.
- **Inspiration boards / competitor screenshots.** Use a Figjam / Mural / Pinterest. The relevant takeaways belong in a separate file (or in the design's `context`), not in the active design file.
- **Workshop artifacts.** Sticky notes, voting dots, miro-boards from a brainstorm. Capture the outcomes, not the process, in the `.pen`.
- **Stakeholder presentation decks.** Deck tools exist for a reason. Export the design's screenshots into the deck; don't build the deck inside the `.pen`.
- **Long-form documentation.** Use the project's docs system. The `.pen`'s Cover and per-component `context` strings are the design-side documentation.
- **Unmaintained component experiments.** Either commit to maintaining them (move to `Exploration` or `Archive`) or delete them.
- **Production designs and concept designs side-by-side without status.** Either separate by region (SourceOfTruth vs Exploration) or split into different files.

The Cover should contain enough links to external systems that anyone reading the file can find the broader context. The `.pen` itself stays focused on design.

## Completeness checklists by project type

A design that ships only the happy path is a sales demo. A real product design covers the work. The pressure tests below are the floor; every project should clear them.

### SaaS pressure test

> *"If the file does not show roles, permissions, empty states, loading states and error recovery, it is not comprehensive. It is a sales demo."*

A real SaaS app design covers, at minimum:

- **Auth.** Sign-in, sign-up, password reset, magic-link sent, magic-link expired, MFA, SSO, session expired, account locked, invite accepted, invite expired.
- **Workspace.** No-workspace, create workspace, workspace switcher, multiple-workspace nav, workspace settings, organisation settings, user-removed-from-workspace.
- **Navigation.** Global nav, sidebar collapsed/expanded, breadcrumbs, mobile nav, search, notifications, help, account menu.
- **Core product.** Dashboard, list view, detail view, create flow, edit flow, review flow, approval flow, export flow, delete/archive/restore flow.
- **Admin.** User management, role management, permissions, billing, integrations, API keys, webhooks, audit log, security settings.
- **System states.** Empty, loading, error, partial-data, no-permission, read-only, plan-restricted, trial-expired, background-job running/completed/failed.

If your `.pen` ships fewer than ~80% of these, name what's out of scope (in the Cover) and why. Skipping silently produces a design that demos well and breaks at first contact with users.

### Website pressure test

> *"If the file does not show mobile navigation, forms, validation, cookie/consent states, SEO heading structure and CMS template behaviour, it is not comprehensive. It is a brochure mock-up."*

A real marketing site design covers, at minimum:

- **Page templates.** Homepage, product page, feature page, solutions page, pricing, about, contact, demo request, blog index, blog article, case study, legal pages.
- **Forms & conversion.** Demo request form (with validation, submitting state, success state), newsletter signup, contact form, all states.
- **Navigation.** Top nav, mega menu, mobile hamburger / drawer, footer (multiple footer variants if used).
- **Compliance.** Cookie banner, consent accepted, consent rejected, cookie preferences modal.
- **Errors.** 404, 500, offline (if applicable).
- **SEO structure.** Heading hierarchy on each page (the engineer should be able to derive `<h1>` / `<h2>` / `<h3>` from the design).

### Mobile pressure test

> *"If the file does not show keyboard states, permissions, offline behaviour, platform navigation and safe-area handling, it is not comprehensive. It is resized desktop design."*

A real mobile app design covers, at minimum:

- **Launch & auth.** Splash, first-launch, sign-in, biometric prompt, permission prompts (camera, notifications, location, contacts).
- **Navigation.** Bottom tab bar (≤ 5 items), sidebar drawer (if used), modal sheets, native-style headers with back affordance.
- **Core flows.** Per-platform if iOS and Android diverge; shared if they don't.
- **Keyboard states.** Forms with the keyboard open (does the input scroll into view? does the CTA stay accessible?).
- **Offline & recovery.** Offline state, sync-failed state, retry affordance, partial-cached-data state.
- **System states.** Push permission requested / granted / denied; notification handling; deep-link landing.
- **Safe areas.** Notch, home indicator, dynamic island, status bar. Handled in every full-screen design.

For per-platform sub-sections, organise:

```
SourceOfTruth (iOS)
SourceOfTruth (Android)
Shared mobile patterns
```

Or separate by region within the same file.

## AI-readiness as a meta-principle

Every discipline rule in this skill (naming, context, components-first, themes, responsive, accessibility, file architecture) exists *partly* because the design will be read by AI tools downstream. The next agent that opens the `.pen`, the code-generation step, the design review, the handoff to engineering: all of these consume the design as data, not as visual art.

Practically, this means:

- **Layer names should describe role, not appearance.** A node named `BlueButton` reads as "a blue button" to a human and "no useful semantic information" to an AI. A node named `PrimaryAction` reads as "a primary action" to both, and the AI can map it to `<button>` with an appropriate ARIA role.
- **`context` should describe behaviour, not visual specs.** `batch_get` reads colours, sizes, and spacing from the design's structure. `context` is for the things that *can't* be inferred: data dependencies, interaction patterns, accessibility roles, conditional logic.
- **Components are first-class, not decorative.** A button drawn from primitives in three different places becomes three different buttons to an AI. A `ref` to a `Button` component becomes one button instantiated three times, far more useful for downstream code generation.
- **The Cover and SourceOfTruth section answer "what's canonical?"** without the AI having to guess. Code generators should only generate from SourceOfTruth.
- **Status (file and component) tells the AI what's safe to use.** A `deprecated` component should be flagged when an AI is about to use it.

You're designing for AI-assisted handoff as a first-class consumer. Every discipline rule you follow makes the next AI's job easier, and reduces the cost of generating, reviewing, or shipping the design.

## Pencil expression: putting it together

A well-organised `.pen` looks like:

```
Cover (at canvas origin)
  ├── Title: "Auth: Signup, Sign-in, Password Reset"
  ├── Owner: "Alex Chen"
  ├── Status: "Ready for build"
  ├── Version: "1.4.2"
  ├── Last updated: "2026-05-09"
  ├── In scope: "..."
  ├── Out of scope: "..."
  └── Links: "Brief, Linear AUTH-123, Prototype, Design system"

── SOURCE OF TRUTH ── (heading text in canvas)

  Auth / SignUp / 01 / EmailEntry / Default / Desktop
  Auth / SignUp / 01 / EmailEntry / ValidationError / Desktop
  Auth / SignUp / 02 / EmailVerify / Sent / Desktop
  Auth / SignUp / 02 / EmailVerify / Expired / Desktop
  Auth / SignUp / 03 / Welcome / Default / Desktop
  ... (responsive variants in Responsive region)

── BUILD READY ── (heading text in canvas)

  Auth / SignIn / 01 / Default / Desktop  (in active design)

── UX STATES ── (heading text in canvas)

  EmailField / States  (Default | Hover | Focus | Error | Disabled)
  PasswordField / States  (Default | Hover | Focus | Error | Disabled | RevealPassword)

── RESPONSIVE ── (heading text in canvas)

  Auth / SignUp / 01 / EmailEntry / Default / Mobile
  Auth / SignUp / 01 / EmailEntry / Default / Tablet
  ... (one per Source of Truth screen)

── EXPLORATION ── (heading text in canvas, far right)

  Auth / SignUp / Alternative-magic-link / 01 / EmailEntry / Default / Desktop
  Auth / SignUp / Alternative-passkey / 01 / Default / Desktop

── ARCHIVE ── (heading text in canvas, bottom)

  Auth / SignUp / v1.0 / EmailEntry / Default / Desktop  (shipped 2025-Q4)
```

The structure is verbose to describe; cheap to maintain once in place. A teammate or AI opening the file can navigate immediately.

## Verification checklist

Before declaring file architecture done:

1. **Cover present** at canvas origin, with all required fields filled.
2. **Status accurate** in the Cover (matches actual file state).
3. **Section regions visible** with heading text separating them.
4. **No exploration in SourceOfTruth** and vice versa.
5. **Hierarchical naming** on multi-screen flow frames; PascalCase on single-screen frames.
6. **Component status** present in every `reusable: true` component's `context`.
7. **Completeness.** For SaaS / Website / Mobile, the pressure test passes (or what's out of scope is documented in the Cover).
8. **Links from Cover** resolve and are current.

For projects that span multiple `.pen` files:

9. **Each file has its own Cover** with consistent ownership and version conventions.
10. **The design system file (`*.lib.pen`) is imported** by the consumer files; not duplicated inline.
11. **Archive files** carry their date / period in the filename (e.g. `archive-2026-q1.pen`).

Fix what fails. The point of the discipline is to make the file readable in 30 seconds; verify by simulating that read.

## See also

- SKILL.md § Discipline rules § File architecture: the always-apply rules (Cover frame, section regions, hierarchical naming).
- SKILL.md § Design-system convention: when to scaffold `design-system/` markdown files alongside `.pen` files.
- [`composition-patterns.md`](composition-patterns.md): component status workflow.
- [`pen-schema.md`](pen-schema.md): `.pen` data model, `.lib.pen` libraries, imports.
- [`mcp-tools.md`](mcp-tools.md): `find_empty_space_on_canvas` for placing section regions.
- [`states.md`](states.md): state vocabulary for the `[State]` slot in hierarchical names.
- [`flows.md`](flows.md): multi-screen flow orchestration; flow patterns map to the `[Flow]` slot.
