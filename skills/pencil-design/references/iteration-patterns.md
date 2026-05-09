# Iteration patterns

The first version of any design is rarely the right one. This file gives the agent a vocabulary for *what's wrong* and a recipe for *what to change*. Most iteration cycles fail by changing the wrong thing. They make a sparse design sparser, or a busy design busier, because the diagnosis was off. Get the diagnosis right and the rescue is usually obvious.

**What this file owns:** the common failure modes (too busy, too sparse, too generic, doesn't feel premium, hierarchy unclear, breakpoints don't hold), the rescue recipes for each, the four-question self-critique gate, the reference-image translation protocol, and the three-iteration limit before stopping to ask the user.

**What this file does NOT own:** the visual hierarchy levers themselves. That's [`visual-hierarchy.md`](visual-hierarchy.md). The token system the rescues lean on. That's [`assets/design-system/tokens.md`](../assets/design-system/tokens.md). The verification ladder this file's three-iteration limit hooks into. That's `SKILL.md` § Verification.

## When to load this file

- The agent has shipped a first pass and the user said it doesn't feel right.
- The design feels generic, busy, sparse, or 'AI-generated' and the agent doesn't know which lever to pull.
- The agent is working from a reference image (a screenshot, a competitor site, a Dribbble shot) and needs to translate it into the project without copying it verbatim.
- The agent has iterated twice and wants to know whether to push for a third pass or stop and ask the user.

## Failure mode: too busy

The most common iteration-one failure. Symptoms: the eye doesn't know where to land. Three or more elements compete for primary attention. The user reports 'overwhelming', 'cluttered', 'hard to scan'.

Rescues, in order of effect:

- **Remove a hue.** Three accent colours becomes one. The page calms immediately.
- **Remove a typeface.** A serif heading + sans body + mono code is plenty; adding a display font for accents tips into busyness.
- **Add whitespace.** Increase section padding by one step in the spacing scale (`$space-8` to `$space-12`). The same content reads quieter.
- **Drop a colour stop.** A 5-stop neutral ramp becomes 3. The greys stop competing.
- **Simplify a shadow.** A 4-layer shadow becomes 2. Subtle wins over dramatic.
- **Mute decorative elements.** Decorative borders, divider lines, and badges drop in saturation or disappear. Save visual weight for content.

Don't add anything when the diagnosis is too busy. Adding a hierarchy element to 'fix' busyness is the most common second-iteration failure.

## Failure mode: too sparse

The opposite. Symptoms: the page reads as a wireframe. The user reports 'feels empty', 'lacks personality', 'where's the content?'.

Rescues:

- **Add density via supporting metadata.** A list of project names becomes project name + last-modified + owner avatar. Same shape, more texture.
- **Add a visual anchor.** A hero illustration, a featured stat, a customer logo wall. One concrete element for the eye to land on.
- **Add a secondary action.** Beside the primary CTA, a quieter 'Learn more' or 'See examples'. Two-tier action invites exploration.
- **Raise type contrast.** A heading that was `font-weight: 500` becomes `font-weight: 700`. The page gets a backbone.
- **Tighten line-height on body.** From `1.6` to `1.5`. Density without crowding.
- **Add a background treatment.** A subtle gradient, a grid texture, or a single coloured shape behind the hero. Not on every page; once is enough.

Sparse-by-design is a real choice (Things, Cron, Apple's product pages). Sparse-by-accident is what this rescue addresses. The user's description distinguishes them: 'minimal' is intentional; 'empty' is accidental.

## Failure mode: too generic / reads as AI

The most insidious. The design is technically fine. Nothing is broken. The user can't articulate what's wrong, only that it 'feels generic' or 'looks AI-generated'.

Rescues:

- **Commit harder to one direction.** A design that hedges between brutalist and editorial reads as neither. Pick one and lean into it. If the brand is brutalist, the buttons should be sharp-cornered, the type should be heavy, the layout should be ungrid.
- **Add an unexpected detail.** A custom illustration in place of a stock icon. A dramatic photo crop. An asymmetric layout where the user expected symmetry. One specific, intentional choice that no template would have made.
- **Change the typeface.** Inter is the safe choice and the AI default. Try something with personality (Söhne, Recoleta, Geist, Fraunces). Bold typography choices read as decisive.
- **Crop a photo unconventionally.** A face cut at the eye line, a product shot from below, a hero image bleeding off the page. Compositional risk reads as intentional.
- **Use real content.** Generic Lorem-ipsum-shaped copy reads as generic. Replace with copy that names a real benefit, a real metric, a real customer.

The single biggest tell of AI design: every choice was the safe one. Pick one place to be brave.

## Failure mode: doesn't feel premium

Symptoms: the design works but feels mid-market. The user wants the polish of Linear or Stripe or Apple.

Rescues:

- **Tighten type tracking.** Headings get `letter-spacing: -0.02em` (or `-0.03em` for very large display type). Premium type sits tighter than default.
- **More white space.** Premium designs use 1.5x to 2x the spacing of mid-market ones. Increase section padding, gutter widths, and component padding by one full step.
- **Fewer colours.** Strip back to 2 to 3 hues total. Adding a fourth or fifth dilutes the brand.
- **Layered shadows.** Two layers minimum: an ambient `0 1px 2px rgba(0,0,0,0.04)` plus a direct `0 8px 24px rgba(0,0,0,0.08)`. The depth reads as cared-for. Single-layer shadows read as a template default.
- **Slower motion.** Default 200ms transitions become 280ms. Hover states ease in over 250ms instead of 150ms. Deliberation reads as premium.
- **Custom illustrations or icons.** Stock icon sets are the giveaway. A premium product has at least one drawing that no other product has.

Premium isn't a single rescue; it's a pile of small ones. Ship them together.

## Failure mode: hierarchy unclear

Symptoms: the user can't tell what's most important. Two or three elements claim primary status. The eye flicks between them.

Rescues:

- **Pick one primary.** The page should have one primary action, one primary heading, and a single primary visual element anchoring them. Everything else demotes.
- **Demote two competing elements.** If a 'Get started' button and a 'Watch demo' button both look primary, pick one. The other becomes a secondary button or a text link.
- **Increase one size step.** The headline goes from `$text2xl` to `$text3xl`. The primary action is the only button at that size.
- **Reduce visual weight on secondaries.** Secondary buttons drop from filled to ghost. Tertiary text drops from default to muted.
- **Add spatial separation.** The primary element gets more whitespace around it. Negative space is the cheapest hierarchy lever.

For the underlying theory of the six levers (size, weight, colour, position, spacing, motion), see [`visual-hierarchy.md`](visual-hierarchy.md).

## Failure mode: breakpoints don't hold

Symptoms: the desktop design is great. The tablet looks awkward. The mobile is broken. The user sees three different products.

Rescues:

- **Restate the constraints.** What's the smallest screen the design has to work on? Mobile-first defaults often catch this earlier than desktop-first.
- **Drop a column at smaller sizes.** A three-column dashboard becomes two on tablet, one on mobile. The columns stack.
- **Swap nav patterns.** Desktop sidebar becomes mobile bottom-tab-bar or hamburger drawer. Don't try to keep the sidebar visible at 375px.
- **Re-order content for mobile.** The hero image that sits beside the form on desktop moves above the form on mobile. The visual hierarchy adjusts.
- **Hide non-essential elements.** Decorative graphics, secondary navigation, advanced filters can disappear at smaller sizes. Document what's hidden in the design's `context`.
- **Use container queries where the component cares about its container.** Viewport queries are right when the component cares about the page.

For the per-breakpoint discipline rules, see `SKILL.md` § Discipline rules § Responsive.

## The four-question self-critique gate

Before declaring a design done, run the 60-second gate. This is the same one summarised in `SKILL.md` § Self-critique gate, expanded with examples:

1. **Could a non-designer recognise this as the brand's voice or industry?**
   - A fintech design should read as fintech to someone who's never used the product. The same goes for developer tools: someone who's never used Linear should still recognise it as a developer's home turf.
   - Test: show the design to someone outside the team for 5 seconds. Ask 'what kind of product is this?'. If they can't tell, the brand voice is missing.

2. **Where does the eye go first, second, third? Does that match priority?**
   - Squint at the design. The visual hierarchy collapses to its essential shapes. The thing that survives the squint should be the thing the user is meant to do first.
   - Test: cover the design, then uncover for 1 second. What did you see? If the answer isn't the primary action, the hierarchy is off.

3. **Is anything decorative-only that doesn't communicate meaning?**
   - Decorative borders, badges, dividers, and shadows that don't carry information are noise. Each visual element should either guide the eye, carry content, or mark a state. If it doesn't, cut it.
   - Test: for each decorative element, ask 'what would change if I removed this?'. If nothing, remove it.

4. **What single change would make this feel less AI-generated?**
   - The honest answer is usually one of: pick a more opinionated typeface, add a custom illustration, commit harder to a style direction, replace generic copy with real copy, take a compositional risk.
   - Test: imagine a designer who hates AI-generated work looking at this. What would they criticise first? Fix that.

Run all four. The gate takes 60 seconds; the design is better for it.

## Reference-image translation protocol

When the user provides a screenshot, a competitor site, or a Dribbble shot as a reference, the agent's job is to translate the *intent* into the project's design language. The output should feel like a sibling of the source, never a clone.

The protocol:

1. **Name the layout pattern out loud.** 'This is a centred hero with a split CTA below, an asymmetric features bento, and a sitemap footer.' Naming the patterns from [`layout-patterns.md`](layout-patterns.md) makes the structure portable.
2. **Extract the palette.** Identify the 2 to 4 hues and their roles (background, primary surface, accent, text). Sample the hex values if needed and map them onto the project's existing tokens. The source's literal values rarely belong in the output.
3. **Identify the type pairing.** Heading typeface + body typeface. If the source uses a custom font, find the closest open-source equivalent in [`font-pairings.md`](font-pairings.md) (Phase 3) or the project's `tokens.md`.
4. **Recognise the design movement or era.** Is it brutalist? Editorial? Glassmorphism? Y2K? Naming the movement makes the choices coherent. The source belongs to a tradition; the translation should belong to one too.
5. **Call out what to deliberately change.** Identify two or three places to deviate. The source might use three colours where the project's brand allows two. The source's display font might not be licenced. The source's density might be wrong for the project's audience.
6. **Recreate in `.pen` without copying verbatim.** Build from the project's tokens, the project's components, the project's spacing scale.

Document the translation choices in the design's `context` so the next agent reading the file can trace which decisions came from the source.

## Three-iteration limit before asking the user

Per `SKILL.md` § Verification ladder, the agent gets three iterations on a design before stopping to ask the user. The limit catches two failure modes: grinding endlessly on the same design, and pestering the user after every single attempt.

How the count works:

- **Iteration 1.** First pass. User sees it; gives feedback or doesn't.
- **Iteration 2.** Apply feedback or apply self-critique. Ship.
- **Iteration 3.** Final attempt with a different approach. Smaller adjustments to iteration 2 don't count.
- **Stop.** If the user is still unsatisfied, the agent stops iterating and surfaces a question: 'I've tried three directions and we're not landing. Could you give me a reference image, name a brand whose feel we're after, or describe the atmosphere in three words?' This is the open-ended-request clarify-intent protocol from `SKILL.md` § Design intelligence.

The trap: iterating with shrinking adjustments. Iteration 3 should look meaningfully different from iterations 1 and 2. If iteration 3 is iteration 2 with one colour change, the agent is grinding. Pick a different lever.

## Pencil expression

Iterations don't usually need new file structure; they happen on the existing frames. Two conventions help:

- **Place iterations side-by-side in the Exploration section.** Per [`file-architecture.md`](file-architecture.md), the Exploration region of the canvas is where iterations live. Name them `Hero_v1`, `Hero_v2`, `Hero_v3`. When one is promoted, move it into the Source of Truth region; archive the others.
- **Annotate the diagnosis in `context`.** When iterating, the previous version's `context` should say what was wrong: *'V1 was too busy. Three competing accents. V2 dropped to one accent.'* The next agent (or the next iteration of this agent) reads the rationale.
- **Don't dual-track once promoted.** When V2 is promoted to Source of Truth, V1 leaves the canvas. Two versions of the same design at the same status confuses everyone.

## Anti-patterns

These read as iteration-blind designs and should be fixed in passing:

- **Adding to fix busyness.** The diagnosis was 'too busy'; the fix added another accent. Subtract instead.
- **Subtracting to fix sparseness.** The diagnosis was 'too sparse'; the fix removed an element. Add instead.
- **Iteration with shrinking adjustments.** V2 differs from V1 by a single colour change. V3 differs from V2 by a single pixel. Pick a different lever.
- **Copying a reference image verbatim.** The output is the source with the project's logo on it. The translation protocol prevents this.
- **Skipping the self-critique gate.** The agent ships V1, the user critiques, and the agent realises three of the four self-critique questions would have caught the issue. Run the gate before shipping.
- **Iterating past three without surfacing.** The agent grinds on iteration 4, 5, 6. Stop at three and ask.
- **Treating 'doesn't feel premium' as a colour problem.** Premium is mostly whitespace, type tightening, and motion timing. Colour is rarely the issue.

## Sources

- **Refactoring UI** (Adam Wathan, Steve Schoger): the canonical reference for the rescue recipes in this file. The 'premium feel' patterns (whitespace, type tracking, layered shadows) come directly from there.
- **Linear, Stripe, Vercel, Apple, Things, Cron**: exemplars of premium SaaS design referenced throughout (accessed 2025/2026).
- **Nielsen Norman Group**: research on iterative design, the diminishing returns of small adjustments, and reference-image translation.
- **Apple HIG**: hierarchy and visual weight principles underlying the 'hierarchy unclear' rescues.
- **Material 3** (Google): responsive breakpoint patterns.
- **AI-generated design tells** derived from observable patterns in 2025/2026 design tooling output, including the 'every choice was the safe one' diagnosis.

## See also

- [`visual-hierarchy.md`](visual-hierarchy.md): the six levers (size, weight, colour, position, spacing, motion) the rescues operate on.
- [`layout-patterns.md`](layout-patterns.md): the named layout patterns the reference-image translation protocol maps onto.
- [`file-architecture.md`](file-architecture.md): the Exploration section where iterations live before promotion.
- [`modern-patterns.md`](modern-patterns.md): container queries and animation timing the breakpoint and premium-feel rescues lean on.
- [`assets/design-system/tokens.md`](../assets/design-system/tokens.md): the type, colour, and spacing scales the rescues operate on.
- `SKILL.md` § Self-critique gate: the same four-question gate, summarised.
- `SKILL.md` § Verification ladder: where the three-iteration limit lives.
