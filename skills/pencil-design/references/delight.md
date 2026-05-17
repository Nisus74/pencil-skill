# Delight

Delight is the difference between a design that does its job and a design the user remembers. It's the small personality moves that survive once the rest of the surface fades into pattern-recognition: the loading state that says something funny, the empty state that earns a smile, the cursor that does something the user didn't expect.

This reference is the *signature-moment* layer that sits on top of competent design. Use it after the design is functionally complete (heuristics scoring passes, distinctiveness checklist passes, accessibility checks pass) and you want one more pass to give the surface character. Not for use as an excuse to skip the work that comes first.

## What delight is

Three working definitions; each one is a different lever:

1. **Personality in functional moments.** The loading skeleton has a colour or shape that ties to the brand. The empty-state copy is warm, not robotic. The success toast doesn't say *"Saved."*; it says *"Saved. 2 new collaborators can now see this."* The job gets done with character.
2. **Signature moments.** One element on the page that wouldn't survive being deleted. A custom data visualisation. A particular type move on the hero. A motion sequence the user looks at twice. The page's *"thing."*
3. **The unexpected positive.** A cursor that subtly attracts toward an actionable area. A confetti pop on a meaningful first-time success. A keyboard shortcut that does something elegantly. The user notices, and the noticing is positive.

What delight is *not*: ornament for ornament's sake. Animation for animation's sake. Whimsy that fights the user.

## When delight earns its place
- **First-use surfaces.** The first session is when the user decides whether the product has character. Front-load delight here.
- **Brand pages.** Brand work is partly memorable-moment work; delight is part of the assignment.
- **Repeat-use surfaces with one recurring moment.** A daily-use dashboard with one moment of delight per day (a different opening greeting; a small visual rhythm change). Repeated daily, the cumulative impression compounds.
- **Recovery moments.** After an error, after a long task, after a frustrating flow: a moment of warmth lands disproportionately.

## When delight is wrong
- **High-stakes, high-frequency surfaces.** A trading interface, an incident response tool, an emergency form. The user is stressed; whimsy reads as inappropriate.
- **Surfaces the user uses for hours.** A moment that delights once becomes irritating on the 200th view. Loops are usually wrong.
- **As a substitute for the real work.** A bad form with a confetti success state is still a bad form.
- **When the brand voice doesn't warrant it.** A serious B2B compliance tool is allowed to be serious. Don't shoehorn whimsy into a brand that has earned the right to be quiet.

## Delight moves that work

### Copy with character
The cheapest, most under-used delight lever. Replace a generic line with a specific one.

| Generic | With character |
|---|---|
| *"Loading..."* | *"Wrangling the data..."* |
| *"No results."* | *"Nothing matches. Try fewer filters?"* |
| *"Saved."* | *"Saved. Your edits are live."* |
| *"You don't have permission."* | *"This one's locked. Ask Aiko (the workspace owner) for access."* |
| *"Welcome back!"* | *"Welcome back, Travis. You're 3 reviews ahead of last week."* |

The pattern: keep the function; add a specific, in-context detail. See [ux-writing.md](ux-writing.md) for the broader copy register.

### Personality in functional motion
Most state transitions are functional (see [motion-design.md](motion-design.md)). One or two per design can carry a small flourish without crossing into overdone:

- A submit button that briefly inverts before its success state.
- A toggle that has a tiny bounce on activation.
- A favourite-heart that fills with a brief scale-up.
- An empty state where a small illustration nudges in response to cursor movement.

The discipline: pick *one* or *two* moments. Putting flourish on every interaction makes the surface feel busy.

### Signature moments
The page's distinguishing element. Not every surface deserves one; the ones that do should commit.

- A landing page's hero treatment that isn't a stock template.
- A dashboard's primary KPI rendered as a custom visualisation instead of a number-and-label.
- An onboarding flow's first interaction that demos the product immediately rather than collecting info.
- A login screen with a specific brand expression (not a generic centred card).

Signature moments are where the design earns the right to be *this* product, not *any* product in the category.

### The thoughtful empty state
Empty states are an under-invested delight surface. The user lands on a screen with nothing populated; the design has the user's full attention with no competing content.

Bad empty state: *"No items."*
Better: *"No invoices yet. When you bill a customer, they'll show up here."*
Delightful: *"Nothing here yet. Most teams send their first invoice within 3 days. Here's how →"*

The delight is in the specificity, the warmth, and the gentle path forward. See [onboard.md](onboard.md) for first-use empty states.

### The unexpected useful
A keyboard shortcut the user discovers by accident and is glad they did. A bulk action that auto-suggests. A column the user can sort that they didn't realise was sortable. The design rewards exploration without requiring it.

### The recovery warmth
After a long task, a small acknowledgement: *"Done. That took 47 seconds; faster than usual."* After an error fix: *"Resolved. Continuing from where you left off."* The warmth lands disproportionately because the user expected the system to be transactional.

## Delight discipline

Three rules:

### One moment per surface
Stacking delight (custom hero + custom empty state + custom 404 + custom success animation + custom loader) becomes noise. One signature moment per surface is plenty. The rest is competent functional design.

### Test the moment at scale
A loading message that delights on the first view irritates by the hundredth. If the surface is repeat-use, randomise (a pool of three or four messages) or fade the delight over use (the first session shows the warm welcome; subsequent sessions are quieter).

### Calibrate to the brand voice
Whimsy on a fintech compliance tool feels inappropriate. Quiet competence on a creative-tools brand feels under-delivered. The delight register matches the brand register; both are decisions, not defaults.

## Delight anti-patterns

- **Confetti on every success.** Cheapens every actually-significant moment.
- **Forced humour that doesn't land.** A loading message that tries too hard reads worse than a neutral one.
- **Animation tax.** Adding a 600ms decorative animation to a 100ms action; the user waits for the animation.
- **The "make it pop" pass.** Adding gradients, glows, drop shadows, and accent colours late in the process *"to add visual interest"* usually compounds into noise.
- **Easter eggs the user can't find.** Hidden delight that requires Konami code-style discovery delights almost no one; the people who would have appreciated it never see it.
- **Whimsy that breaks the flow.** A success state that's so visually engaging the user forgets they were doing something else.

## Per-register considerations

### Brand
Brand delight is choreographed and integrated with the brand voice. A landing page's hero IS the delight if it does its job. A brand pricing page can have personality in the copy and a custom illustration on the recommended-tier card. The whole page can be the signature moment.

### Product
Product delight is restrained and pointed. One moment per surface, integrated into a functional flow. The empty state, the first-use welcome, the recovery message, the success confirmation; these are the legitimate delight surfaces.

## Pencil-specific

### Build the signature moment first
When a design has an identified signature moment (a custom hero, a custom data viz, a specific motion sequence), build it first or early. It's the hardest part of the design; getting it right early lets the rest of the surface compose around it. Saving it for the polish pass usually means it gets rushed.

### Document the delight intent in `context`
A signature moment in Pencil needs the engineer to implement it as designed. Write the intent into the component's `context` string: *"Hero KPI: custom radial visualisation, segments animate in over 800ms with 100ms stagger. Implement as SVG with GreenSock TweenLite."* Without this, the engineer reverts to a stock chart.

### Empty-state delight as `EmptyState` variants
The reusable `EmptyState` component (recommended in [product.md](product.md)) can carry register-specific copy variants: a *"warm"* variant for first-use, a *"neutral"* variant for no-results, a *"quiet"* variant for no-permission. Build the variants in the `.lib.pen` so consumers pick the right tone per surface.

### Verify delight doesn't fight the design discipline
After adding a signature moment, run the [distinctiveness-checklist.md](distinctiveness-checklist.md) again. The moment should make the design *more* itself, not push it toward a generic *"polished"* default. If the signature moment landed in violet-glow-on-the-CTA territory, it's contributing to the AI-default reflex, not breaking it.

### Don't replace the work
Delight is the layer on top of competent design. If the heuristics-scoring pass surfaced issues (per [heuristics-scoring.md](heuristics-scoring.md)) and the response is to add an animation, the surface is regressing. Fix the underlying issues first; then add the moment.
