# Product register

Product work is design where design *serves* the product: app surfaces, dashboards, settings, admin tools, configuration screens, internal tools, data-heavy workflows. The user has a job to do; the design's job is to get out of their way. Distinctive product design is design that makes the job easier, not design that calls attention to itself.

This reference is the depth behind the product entry in SKILL.md's register section. If you're working on a marketing page, landing page, or anything where the design itself is the point, you want [brand.md](brand.md) instead.

## Information density

Product work has three legitimate density modes. Pick one per surface and apply it consistently; cycling through densities inside the same screen reads as accidental.

### Dense
For users who spend hours in the surface and know what they're doing: trading interfaces, observability dashboards, IDEs, log viewers, ticketing systems. Row padding 4–8px, tight type (12–14px body), mono numerals on data columns, hairline borders or no borders at all.

Moves: tables go right to the viewport edges where they can, no card chrome around primary content, secondary metadata in 11–12px muted text.

### Balanced
For users who use the product daily but not for hours at a stretch: CRMs, project management, most SaaS app surfaces. Row padding 12–16px, body 14–16px, more breathing room between sections, light card chrome where it aids scanning.

Default density for product work when nothing else is specified. Don't reach for it because it's safe; reach for it because the surface genuinely is general-purpose.

### Airy
For occasional surfaces: settings, profile pages, account management, billing. Larger spacing (24–32px between sections), generous form fields, fewer items per screen.

Moves: form fields at 44–56px height, section spacing in the 32–48px range, single-column on most viewports.

The fail mode is unconsidered balanced everywhere. The fix is naming the density at the start of step 2 (*"this is a dense data surface; tables go to viewport edges, mono numerals throughout"*) so the rest of the design reads against the call.

## Surface treatment

Product surfaces should default to borders over shadows, hierarchy through spacing rather than decoration.

### Borders over shadows
Drop shadows on cards in product UI are usually thoughtless decoration. They add visual weight without conveying information, they compound when nested, and they're a 2018-era SaaS default. Reach for hairline borders (1px, low-contrast neutral) or pure spacing instead.

Shadows earn their place only when:
- The element actually floats above other content (popovers, dropdowns, command palettes, modals)
- The product is specifically going for skeuomorphic depth as part of brand expression

### Hierarchy through spacing
Visual hierarchy in product surfaces comes from spacing rhythm and type contrast, not from decorative chrome. A section heading at 18px semibold sitting 24px above its content reads as a heading without needing a coloured underline, a tinted background, or an icon.

The compounding-decoration anti-pattern: heading gets larger font + bold weight + accent colour + a bottom border + an icon next to it + a tinted background. Pick at most two; spacing does the rest.

### Corner radii
Pick one corner radius value per surface and stay there. Mixing radii (cards at 8, buttons at 6, inputs at 4, badges at 999) reads as accidental. The choice itself is a brand decision:

- **Sharp** (`cornerRadius: 0` or `2`) reads technical, serious, dense.
- **Subtle** (`cornerRadius: 4` or `6`) reads modern, restrained.
- **Standard** (`cornerRadius: 8` or `10`) reads friendly, default-SaaS.
- **Soft** (`cornerRadius: 12+`) reads consumer, approachable.
- **Pill** (`cornerRadius: 999` on buttons only) is fine if intentional; never on cards.

## Colour strategy

Product is restrained by default. The accent earns its visibility by appearing in fewer places with more meaning.

### Semantic role weight
Product UIs depend on a small, stable palette of semantic colours that the user learns over time:

- **Error** (red, often desaturated): destructive actions, validation failures, alerts that block work
- **Success** (green): completion of significant actions, positive state confirmations
- **Warning** (amber): non-blocking attention, deprecation notices
- **Info** (blue): neutral notifications, system messages

These four shouldn't double as the brand accent or each other. Reserving them for their semantic role keeps the signal strong. If the brand accent is blue, the "info" colour shifts to a different blue or a muted variant.

### One accent
Product UIs work best with one true accent applied to primary actions only. The accent on every link, every active state, every selected row, every chart bar, every badge dilutes the signal to nothing.

Strip the accent from at least five places where the model defaulted to using it: links can be neutral with underlines, active tabs can be a heavier weight, selected rows can be a tinted background, chart bars can be a single neutral, badges can be outline-only. The CTA earns the saturated accent because nothing else fights for it.

### Restrained chroma
Tinted neutrals throughout. No raw `#000` or `#FFF` (banned in SKILL.md). The neutral family tints toward the brand hue at low chroma (0.005–0.01 in OKLCH). Mixing warm and cool greys reads as accidental.

For palette construction methodology, see [color-and-contrast.md](color-and-contrast.md). For semantic role accessibility (the colour-is-never-the-only-signal rule), see [accessibility.md](accessibility.md).

## Typography for data

Product surfaces routinely render numbers, identifiers, and structured data. Typography choices for these surfaces look different from brand work.

### Mono numerals on data
Wherever numbers stack vertically (tables, KPI cards, transaction lists, financial figures), use a monospace or tabular-figure variant. Proportional figures look ragged when stacked; mono or tabular figures align cleanly:

```
Proportional:    Tabular:
  1,234            1,234
    567              567
12,345           12,345
```

Most modern UI fonts (Geist, SF Pro, Söhne, Inter) support tabular figures via OpenType (`font-feature-settings: 'tnum'` in CSS, the equivalent property in Pencil). Use this feature explicitly on tables and numeric columns.

For dedicated data surfaces (trading interfaces, log viewers, observability), reach for a true monospace (JetBrains Mono, Berkeley Mono, IBM Plex Mono) at least for the numeric content.

### Type scale for product
Tighter scale than brand. Modular ratio 1.2 to 1.25:

| Role | Size | Weight |
|---|---|---|
| Display (rare in product) | 32–40px | 600 |
| H1 / page title | 24–28px | 600 |
| H2 / section heading | 18–20px | 600 |
| H3 / subsection | 16px | 600 |
| Body | 14–16px | 400 |
| Caption / metadata | 12–13px | 400 |
| Micro / legal | 11–12px | 400 |

Don't oscillate between sizes mid-page. Pick a step on the scale per role and stay there.

### Special moves for product

- **Small caps on metadata labels.** *"STATUS"*, *"OWNER"*, *"LAST RUN"*. Quieter than all-caps and more deliberate than sentence case.
- **Tracking on small uppercase**. All-caps below 13px needs 4–6% letter-spacing to remain legible.
- **Italic restraint.** Italics for emphasis read fine in long-form product copy; on short UI labels they read as accidental.

For deeper typography decisions, see [typography.md](typography.md).

## State motion

Product motion is functional, not expressive. The job of a transition is to maintain spatial continuity so the user doesn't lose context.

- **Instant feedback on press.** ≤16ms response to a click or tap. Anything slower reads as broken.
- **State transitions 150–250ms.** Hover, focus, selection. Long enough to register, short enough not to feel laborious.
- **Layout shifts 200–300ms.** Panel expansion, accordion open, content reflow. Ease out with a quart or quint curve.
- **Skeleton loading for content that takes >300ms.** Use shaped placeholders (text-line skeletons match the line height of the loaded content) rather than spinners.

Refuse:

- Bouncing or elastic ease curves on UI transitions (they read as overdone)
- Long fade-ins on content that should appear immediately
- Spinner-only loading (use skeletons; reserve spinners for indeterminate post-action waits)
- Background animations on idle surfaces

## Empty-state taxonomy

Product surfaces have four distinct empty-state types. Each deserves a different shape; collapsing them all into a generic *"No items"* card is the most common mistake.

| Type | When | Copy shape | Action shape |
|---|---|---|---|
| **First use** | The user has never used this surface | Onboarding intent: what is this, why does it matter, what to do | A primary CTA that starts the meaningful first action |
| **No results** | A query or filter returned nothing | Acknowledge the query: *"No invoices from May 2026"* | Adjust filters CTA, or clear-filters affordance |
| **No permission** | The user can't see content here | Explain what they're missing and why | Contact-admin or request-access CTA (or nothing) |
| **Post-action** | The user cleared a queue or completed a list | Acknowledge the completion: *"Inbox zero"* | Optional CTA to next-meaningful-thing, or nothing |

The first-use state is the most under-invested. It's the user's first impression of the surface and deserves more design care than the populated state. Resist the urge to copy-paste an icon-plus-headline-plus-button template.

For deeper state coverage (loading, error, partial-failure, etc.), see [states.md](states.md).

## Microcopy

Product copy is functional, specific to the user's domain, and ideally written in the same vocabulary the user thinks in.

Replace generic SaaS copy with domain-specific copy at every opportunity:

| Generic (refuse) | Domain-specific (reach for) |
|---|---|
| *"How your product performed over the last 7 days"* | *"API calls this week"* |
| *"Something went wrong. Please try again."* | *"Connection lost. Retry now."* |
| *"No items found"* | *"No invoices match these filters"* |
| *"Save changes?"* | *"Publish the 3 edits?"* |
| *"You don't have permission"* | *"Only workspace admins can edit billing"* |

Button labels go outcome-first: *"Delete 5 items"* over *"Remove selected"*. Form-submit buttons name the outcome: *"Create the workspace"* over *"Submit"*.

For the full UX writing depth (error message shape, empty-state copy patterns, the AI cliché list to refuse), see [ux-writing.md](ux-writing.md).

## Product-specific anti-patterns

In addition to the bans in SKILL.md, product work has its own:

- **The SaaS-violet default.** Reaching for violet (`#7C3AED` and adjacent) as the brand accent without any thought. Violet is over-saturated in B2B SaaS. Pick a colour with intent.
- **Hero-metric cards stacked across the dashboard top.** Already banned in SKILL.md; worth repeating because product UIs revert here constantly. The four big-number row is a SaaS cliché.
- **The settings page that's nine sections of identical card-and-form rows.** Settings deserves more variation: short forms inline, dangerous actions in a destructive zone with different chrome, paid features grouped separately.
- **The cramped table with 9px padding and no visual breathing.** Density is a choice; *cramped* is the failure to make one. If dense, commit (4–8px padding, mono numerals, hairline borders); if balanced, commit (12–16px); don't land in 9.
- **Generic admin chrome.** The same sidebar + topbar + main area template applied without thought. The chrome itself can be a brand expression; don't waste the surface area.
- **Modal-as-first-thought.** Already banned in SKILL.md; worth repeating because product work falls into it for every editing surface. Most edits should be inline or progressive, not modal.

## Pencil-specific

### Density tokens
Declare density-aware spacing tokens so the same components can render in different densities across surfaces:

```
$spacingRow_dense: 4
$spacingRow_balanced: 12
$spacingRow_airy: 24
```

Then frames bind their row-spacing variable based on the density they're representing. This lets the same `Row` component serve a dense table and an airy settings list without forking the component.

### Table anatomy
A product table in Pencil usually wants:

- A header row with `fontWeight: 500`, slightly muted text colour
- Body rows with mono or tabular figures on numeric columns
- Hairline borders (or no borders, just spacing rhythm) between rows
- Sticky header if the table will scroll
- Right-align numeric columns, left-align text columns

Build the table as a frame with auto-layout direction `column`, each row a frame with auto-layout direction `row`. The header is a separate frame above. For a worked table build, see the table section of `references/chart-anatomy.md`.

### Empty-state component
Build a reusable `EmptyState` component in your `.lib.pen` with slots for icon, headline, body copy, and primary action. The four empty-state types (first-use, no-results, no-permission, post-action) become variants of the same component rather than four hand-built surfaces.

### Component-first discipline
Product work compounds the components-first rule from SKILL.md. A dashboard built from primitives instead of a `KpiCard`, `DataTable`, and `EmptyState` library is a maintenance bug at scale. Scan the `imports` field and `reusable: true` nodes first; build from primitives only when the library genuinely lacks a fit.

### Dark mode parity
Product UIs are routinely used in dark mode. Every colour variable carries both light and dark values from the first variable declaration onward. Verify under both modes before declaring done. Tokens that pass contrast in one mode often fail in the other; `accessibility.md` has the verification approach.
