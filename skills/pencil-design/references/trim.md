# Trim

Trim is the performance pass. Most of the actual runtime work happens after handoff (engineering owns first paint, network, and rendering on the device), but the design carries decisions that set the ceiling. Asset count, font weight, motion budget, render-blocking choices, perceived-versus-actual-performance trade-offs. Trim is about the decisions the designer makes that engineering can't undo.

Use this reference once the design's content and structure are settled. Trimming before then is premature; the design might cut content that mattered for performance, or skip skeleton states for sections that get pared away later.

Trim isn't [pare.md](pare.md). Pare cuts content for clarity; trim cuts weight for speed. A pared surface might still be heavy (one custom font, three high-resolution images, four concurrent animations); a trimmed surface is lighter regardless of how much content it has.

## Register

On brand surfaces, trimming means the hero image is sized for the device, the font subset matches what's on the page, the motion runs at 60fps on a phone, the atmospheric video is replaced by a still on slow connections. Brand pages have more rope on visual ambition; the trim pass is what keeps that ambition shippable.

On product surfaces, trimming means the surface renders fast at first paint. Skeletons replace spinners; optimistic UI replaces blocking confirmations; perceived performance beats actual performance. The user opens the dashboard and sees structure within 200ms even if the data takes a second more.

## Assess current state

Build the weight inventory.

1. **Images.** List every image on the surface and rate each: hero (must show on first paint), supporting (above the fold but not critical), decorative (below fold, can defer). For each, note the expected weight (full-page hero is 200–600KB; thumbnail icon is 10–40KB).
2. **Fonts.** Count font families on the surface. Two is the comfortable ceiling (display + body); a third (mono) is acceptable when it carries data. Beyond three is a problem. Count weights per family; one weight per family is the cheap option, more weights add bytes.
3. **Motion sequences.** List every active animation on first paint and on scroll. Three concurrent is the working ceiling; more starts to cost perceptible frame drops on mid-tier mobile.
4. **Effects.** Count backdrop-blur surfaces, layered shadows, gradient backgrounds, blur filters. Each one costs render time; the cost compounds when they stack.
5. **Skeleton coverage.** For every async section (data tables, image grids, lazy-loaded content), check that a skeleton state exists. Missing skeletons are silent perceived-performance failures.
6. **Optimistic UI candidates.** List the actions that succeed >95% of the time (saving a note, toggling a setting, sending a known-good form). Each one is a candidate for *"success state appears immediately; rollback on failure"*.

Output is a weight map and an opportunity list. *"Hero is 800KB unoptimised; three font families load on first paint; four concurrent entrance animations; no skeleton on the dashboard charts; the save-note action blocks for 600ms."*

## Plan

Pick the perceived-performance lane plus the actual-performance constraints.

- **Perceived-performance lane:** skeleton-first (structure shows before content), optimistic-UI (action confirms before server), progressive-disclosure (load the visible part, defer the rest). Pick one as the default for the surface; mix where individual sections benefit.
- **Actual-performance constraints:** image-weight ceiling per type (hero ≤300KB after compression, thumbnail ≤30KB), font-family count cap (two plus one mono), motion-budget cap (three concurrent), backdrop-blur surface cap (one per fold).

A design with no perceived-performance strategy and no constraints is undelivered weight that engineering will absorb as runtime cost.

## Apply across dimensions

### Images

Declare image variants for different breakpoints; document expected weights in `context` strings for engineering.

For generated imagery, use `Generate(nodeId, "ai", "<prompt>")` to specify a generated image that matches the surface direction. Engineering substitutes the production image at the right weight.

- Hero images: WebP or AVIF; 80% quality; sized to the largest expected viewport (1920w) with downsized variants at 1280, 768, 320.
- Supporting images: thumbnails 200–400px wide; aggressive compression (60–75% quality); lazy-loaded if below the fold.
- Decorative: lazy-loaded always; consider SVG or CSS for shapes that don't need raster.
- Avatars: 40–80px standard; serve at 2x for retina; fall back to coloured initials when missing.

Document the weight budget per image in the `context` string on the image node. *"Hero image: ≤300KB after compression, AVIF preferred, WebP fallback, JPEG for ≤IE-equivalent."*

### Fonts

Two families maximum (display + body). One mono optionally as a third when data or code is on the page. Beyond three is a refactor opportunity, not a port.

- One weight per family for first paint. *"Inter at 400 + 600"* is two weights on one family; the page can render with both immediately. *"Inter at 200, 300, 400, 500, 600, 700, 800, 900"* is eight weights; that's a network cost.
- Defer extra weights or styles to lazy load if used only below the fold.
- Subset to Latin or Latin-extended for English content; subset to the specific language if the surface is single-language.
- Document the subset in `context` on the variable that names the font: *"$fontDisplay = Söhne; subset Latin-extended; weights 400, 700; ~45KB."*

OpenType features (tabular figures, stylistic sets) are part of the font; they don't cost extra bytes. Activate them freely.

See [typography.md](typography.md) for the font choice and pairing depth.

### Motion budget

Cap concurrent animations at three on any surface. Beyond three, mid-tier mobile starts dropping frames on the page-load sequence.

- Hero choreography: one sequence; stop sequencing for subsequent sections.
- Scroll-anchored reveals: one per fold visible; stagger reveals so no more than three are mid-animation at once.
- Hover affordances: instantaneous (≤16ms); not a budget concern.
- Idle motion: avoid on product surfaces; on brand pages cap at one slow background element.
- `prefers-reduced-motion`: provide the zero-motion fallback. The fallback is also faster, by definition.

See [motion-design.md](motion-design.md) for the easing and duration depth.

### Skeleton states

For any content that takes >300ms to load, build a skeleton state. The skeleton matches the line height and shape of the loaded content; the user sees structure, not a spinner.

- Build the skeleton as a sibling frame of the loaded frame inside the same `reusable` component.
- Call `SetVariables` inside `batch_design` to declare `$skeletonBase` and `$skeletonHighlight` tokens for the animated shimmer surface.
- Skeletons that match the loaded shape feel like *"the content is coming"*; skeletons that don't (every loading state shows the same rectangle grid) feel like *"this is a loading screen"*. The first one preserves perceived performance; the second one breaks it.

See [states.md](states.md) for the skeleton-state pattern and [interaction-design.md](interaction-design.md) for the loading-state design.

### Optimistic UI

For actions that succeed >95% of the time, show the success state immediately and roll back on failure.

- Toggle switches: flip on press; revert if the server rejects.
- Save-note actions: show *"Saved"* immediately; surface a banner if the save fails async.
- Like, favourite, vote actions: increment the count immediately; revert with a brief shake if the server rejects.
- Form submissions: only optimistic when the submission is idempotent and the failure rate is low. Most form submits aren't candidates; bulk-edit toggles often are.

Document the optimism in the component's `context` string: *"Optimistic on press; revert to default state if server returns non-200 within 3s; show toast on failure."*

See [flows.md](flows.md) for the optimistic-UI pattern and the rollback design.

### Shadow and blur budget

Backdrop-blur and large soft shadows cost render time; the cost compounds when they stack.

- Cap layered shadows at two per element. A card with three shadows (outer, inner, glow) is rendering three composite operations.
- Cap surfaces with backdrop-blur to one per fold. A page with five glassmorphism surfaces stacked on top of each other will frame-drop on mid-tier mobile.
- Replace `backdrop-blur` with solid surfaces wherever the design tolerates it. Glassmorphism is refused elsewhere in this skill; trim is the pass that catches any stragglers.
- Subtle shadows are cheap; large soft shadows are expensive. The visual difference is small; the render cost is large.

## Never

- **Never ship a design without skeleton states on slow surfaces.** Spinners on >300ms loads break perceived performance.
- **Never use three or more font families.** The cap is two plus an optional mono. Each additional family is a network cost the user pays before first paint.
- **Never ship glassmorphism on product surfaces.** Backdrop-blur is expensive and the AI default. The trade isn't worth it.
- **Never stack five backdrop-blur surfaces on top of each other.** Performance collapses on mid-tier mobile; the surface doesn't render at 60fps.
- **Never animate everything.** Animation cap is three concurrent; everything-animates eats the render budget.
- **Never document image weights in design copy that engineering can't read.** Weight budgets go in `context` strings on the image nodes themselves.
- **Never substitute *"trust the model"* for explicit budgets.** Specific limits (≤300KB hero, ≤2 fonts, ≤3 animations) ship; vague guidance doesn't.

## Verify

Walk the surface and check:

- **Skeleton states present.** Every async section has a designed skeleton; no raw spinners on >300ms loads.
- **Font count ≤ 2 + 1 mono.** Three families maximum; weight counts under five per family for first paint.
- **Motion budget ≤ 3 concurrent.** Page-load sequences and scroll reveals respect the cap.
- **Image variants declared.** Each image has a documented weight budget and a multi-breakpoint plan.
- **`prefers-reduced-motion` fallback present.** Designed, not omitted.
- **Backdrop-blur ≤ 1 per fold.** Glassmorphism is absent or explicitly justified for the brand context.
- **Optimistic UI on high-success actions.** Toggles, saves, and likes confirm immediately where the action is reversible.

When the result feels right, hand off to [finalise.md](finalise.md) for the alignment, spacing, and token-consistency pass.
