# Cognitive load

Every design asks the user to spend mental energy: to understand the surface, to find what they're looking for, to act, to recover from mistakes. Cognitive load is that spend. The job of design is to reduce it where reduction helps and to invest it where investment pays off.

This reference is the theory behind the density rules in [product.md](product.md) and the hierarchy guidance in [typography.md](typography.md). Use it whenever a design feels *"busy"*, *"cluttered"*, *"overwhelming"*, or *"empty for no reason"*; those are cognitive-load signals.

## Three types of load

From educational psychology (Sweller); the framing translates directly to UI work.

### Intrinsic load
The difficulty of the task itself. Tax software is intrinsically hard. A login screen is intrinsically easy. You can't reduce intrinsic load by changing the design; the task is what it is. You can recognise it and design proportionally.

### Extraneous load
Mental energy the design forces on top of the task. A confusingly-labelled button, a misleading icon, a form that demands fields in an unintuitive order, copy that buries the action. This is the load to eliminate. It adds friction without serving the user.

### Germane load
The mental work that helps the user build understanding. A well-named control teaches; a clear hierarchy makes the surface re-learnable; a thoughtful empty state explains what the populated state will be. This is the load to invest in; it pays back across repeat visits.

A good Pencil design *minimises extraneous* load, *respects intrinsic* load (doesn't pretend hard tasks are simple), and *invests in germane* load (teaches the surface as the user works).

## Attention budget per surface

Different surfaces deserve different cognitive-spend budgets.

| Surface | Budget | Implication |
|---|---|---|
| **First-use onboarding** | High germane investment | The user is willing to learn; teach generously |
| **Daily-use dashboard** | Low extraneous, high pattern-recognition | The user knows the surface; don't re-introduce it every session |
| **Settings / configuration** | Moderate; tolerate explanation | The user is here intentionally and infrequently; help them get it right |
| **Emergency surface (incident, error, billing failure)** | Minimum extraneous | The user is stressed; surface what matters, hide what doesn't |
| **Marketing landing** | High budget for one moment | The user gives 5–10 seconds; spend all of it on the headline plus one image |
| **Documentation** | High intrinsic, high germane | The user came to learn; structure beats brevity |

The mistake: applying the same budget across surfaces. A dashboard built like a marketing landing wastes its budget on hero animations. A settings page built like a dashboard hides explanations behind icons because *"power users will figure it out."*

## Hierarchy as cognitive principle

Visual hierarchy isn't decoration; it's a cognitive scaffolding move. A well-ordered hierarchy reduces extraneous load by answering the user's pre-conscious question *"where do I look first?"* before they know they're asking it.

Three working hierarchy mechanisms, in order of cost-to-the-design:

1. **Spacing.** The cheapest, most powerful. A 24px gap before a heading separates it from the section above without any chrome. Most designs under-use spacing and over-use other mechanisms.
2. **Type weight and size.** A 600-weight heading reads as a heading without needing a colour or an icon. A heading at the same weight but 1.5× the size also reads as a heading. Combining the two compounds.
3. **Colour and chrome.** Tinted backgrounds, borders, accent emphasis. The most expensive in design budget; spend last, after spacing and type contrast have done their work.

The compounding-decoration anti-pattern from [product.md](product.md) is a cognitive-load failure: when a heading gets larger font, bold weight, accent colour, a bottom border, an icon next to it, and a tinted background, the design has stacked five hierarchy signals where one would have worked. The user processes all of them, which costs extraneous load.

## Density and density-load mismatch

Density is not the same as cognitive load. A dense table read by a trader who knows every column is low load (high familiarity, high pattern recognition). The same table shown to a new user is high load (every cell demands attention).

This is the **density-load mismatch:** a surface's density should match its user's familiarity. Common failures:

- **Dense surface for first-time users.** A new analyst opening a trading interface; a new admin opening a configuration matrix. The surface is dense because experts can handle it; the first user can't. Either include progressive disclosure (collapsed by default; expand to dense) or give first-use the airy treatment.
- **Airy surface for power users.** A senior PM with a thousand projects opening a sparse, friendly UI; they want density they can scan. Their screen is wasted on whitespace.
- **Toggling without commitment.** A density toggle in the corner is a band-aid for not deciding. Pick the default density based on the dominant user; offer the toggle as a power-user affordance, not the default escape hatch.

## Per-register implications

### Brand
Brand surfaces sit in the "high budget for one moment" column. The user is willing to spend 5–10 seconds on the hero, less on each subsequent section. Front-load the cognitive investment; let the page taper.

Brand-specific failures:
- **The information-dense landing page** that reads like a feature comparison spreadsheet (a SaaS reflex). Cuts the budget on the moment that needs it.
- **The hero that demands three things at once** (a video, a headline, a form, a chevron). Pick one.

### Product
Product surfaces sit in the "low extraneous, high pattern-recognition" column for daily-use, and the "high germane investment" column for first-use. The first-use to daily-use transition is where most product UIs fail: they're either over-explained forever (germane load never tapers) or under-explained from day one (germane load was skipped).

The fix is conditional copy: first-use shows the explanation; daily-use hides it. *"Learn more"* affordances that the user can dismiss once read are the simplest pattern.

## Anti-patterns that compound cognitive load

These are unforced extraneous-load multipliers; refuse them on sight.

- **Icon-only buttons in unfamiliar layouts.** Icon meanings aren't universal. *"Send"* with no label asks the user to map the icon every time. Use label-plus-icon for any action that isn't part of a recognised pattern (X-to-close, magnifying-glass-for-search, gear-for-settings).
- **Headings that demand colour decoding.** *"Red sections are critical; yellow are caution; blue are info."* The user keys-and-decodes every section. Use icon plus text together (per [accessibility.md](accessibility.md)).
- **Dense surfaces with no scanning structure.** A wall of unbroken text or a flat table with no visual rhythm. The user has to read every cell to find anything.
- **Modal stacks.** A modal that opens another modal. Each new modal pushes the previous context further from working memory; the user loses track of what they were doing.
- **Inconsistent terminology across the surface.** *"Workspace"* in one place, *"team"* in another, *"organisation"* in a third. The user maintains three mental models.
- **Tooltips substituting for clear labels.** *"Click to find out what this does."* Tooltips are footnotes; the primary copy should communicate.
- **Empty states that don't explain.** *"No items."* The user has to figure out *what* would have been here and *why* it isn't.

## Pencil-specific

### Use `context` to keep cognitive load down for the next agent
The discipline rule in SKILL.md about populating `context` on every non-trivial node is itself a cognitive-load move. Each `context` reduces the load on the next agent reading the design: they don't have to reverse-engineer what a node was for; the prior author told them.

The same logic applies to `name`: a meaningful semantic name (`PrimaryAction`, `SearchResultsEmpty`) is a cognitive-load reduction for everyone who reads the file later.

### Screenshot rhythm and load
The screenshot loop in SKILL.md works partly because it caps the cognitive load on each iteration. A small `batch_design` chunk plus one screenshot plus a narrated reaction is easier for the agent to reason about than 60 ops at once. The same applies to the user watching the design unfold.

If a design feels overwhelming to compose, the chunks are too large. Shrink the chunk, screenshot more often.

### When to ask the user about familiarity
If a Pencil design is for a known user archetype (existing product team using their daily tool), the agent can default to higher density without asking. If the user archetype is unknown or first-time-heavy (marketing landing, onboarding, public app), default to airier composition and surface the question: *"Is this for first-time users or experienced ones? It changes the density call."*

### Verify load against the populated state
The most common cognitive-load mistake in Pencil work: designing the empty or low-data version of a surface, where everything looks calm, then shipping it without testing the populated state. A dashboard with three rows in design is unrecognisable from the same dashboard with three hundred rows in production. Always populate at least one design frame with realistic data volume before declaring it done.
