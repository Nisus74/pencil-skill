# Rescuing a "too busy, can't tell where to look" design

"Feels too busy" is almost always one of three diseases, sometimes all three at once: too many competing focal points (no hierarchy), too many distinct values in use (token drift — the design has accreted variations of the same thing), or not enough breathing room (gaps and padding too tight relative to content density). The user's second clause — "can't tell where to look" — confirms the first one is in play. The protocol below diagnoses which combination it is, then fixes them in the cheapest order.

I don't have a live Pencil session attached, so I'll narrate the calls I'd make, what I'd expect back, what I'd check, and the targeted ops I'd issue. No `mcp__pencil__*` tool will actually run.

## References I consulted

Loaded for this task:

- **`SKILL.md`** — for the default workflow, the verification ladder, the discipline rules (Naming, Context, Themes, Aesthetic defaults / "name the atmosphere"), and the Failure modes table. The atmosphere axes (density / variance / motion) are the spine of this rescue: the user is essentially saying "the current density is wrong and the variance is too high."
- **`references/mcp-tools.md`** — for the audit-and-cleanup composite recipe (`search_all_unique_properties` → review → `replace_all_matching_properties`), and to confirm `snapshot_layout` and `batch_get` are the right cheap tools for diagnostic reads before any pixel-level screenshot.
- **`references/batch-design-grammar.md`** — for the exact `U` / `R` op forms I'd use to consolidate type sizes, gaps, and fills. Also for the `padding: [t, r, b, l]` shape (no `paddingTop`) and the rule that variable bindings like `"$primary"` are preferred over raw hex.

I deliberately did **not** load `references/states.md`, `references/flows.md`, `references/accessibility.md`, or `references/modern-patterns.md` — none are on the critical path for a "too busy" diagnosis. I'd reach for `accessibility.md` only if the contrast diagnostic in step 4 turned up failures and I wanted the deeper checks (focus order, `prefers-contrast`).

I did not load `references/component-anatomy.md` either; we're not introducing or restructuring components, just consolidating values and re-establishing hierarchy on what's already there.

## The rescue protocol

### Step 0 — Detect host and locate the design

```
get_editor_state({ include_schema: false })
```

Expected response shape: an object with the active document path, the current selection, and document metadata. I want three facts:

1. Which `.pen` is open and what its top-level frame ids are.
2. What the user has selected — selection is a strong hint about *which* part of the design they think is too busy. If they have a single card selected, the rescue is scoped to that card. If nothing is selected, the rescue is page-wide.
3. Whether `imports` lists a `.lib.pen` — if a library exists, hand-built lookalikes drifting from library components are a likely contributor to the busyness.

If it errors with `transport not connected`, I stop and tell the user to open the Pencil desktop app or the IDE extension (Failure mode §1). I do not silently fall back to the CLI.

If no document is open (Failure mode §2), I ask which one they mean before doing anything else.

### Step 1 — Establish the scope before touching anything

Before any audit, I confirm with the user in one sentence what they want rescued: *"Quick check — do you want me to rescue the whole `[FrameName]` page, or just the `[selected node]`? And is the goal a light cleanup (consolidate, calm down) or a more serious re-hierarchy (pick a single hero, demote everything else)?"*

This is cheap and prevents the most expensive mistake — me re-arranging the page when the user only meant the sidebar, or me doing a calm consolidation when they wanted a bold "make one thing the hero, dim everything else."

### Step 2 — Read the project's design language

```
get_variables()
```

Expected: an object keyed by variable name. I want to know the spacing scale, type scale, and color tokens the project actually has. The rescue collapses ad-hoc values to these tokens; if the project has `space-1..space-8` and `textSm/Base/Lg/Xl/2xl/3xl`, that's the target alphabet.

If a `design-system/` folder exists at the repo root, I'd also read `design-system/README.md` and then `tokens.md`, `layout.md`, and (if relevant) `components.md`. These files override the skill's aesthetic defaults — if `tokens.md` declares a single accent and a tight spacing scale, the rescue should converge on those, not on my generic defaults.

### Step 3 — Inventory components (the cheap one)

```
batch_get({ patterns: [{ reusable: true }], readDepth: 2 })
```

And, for each entry in `imports`:

```
batch_get({ filePath: "<library-path>", patterns: [{ reusable: true }], readDepth: 2 })
```

What I'm checking: does the open document have hand-built lookalikes of components that already exist in the library? A page with three different "button" implementations — one a real `ref`, one a frame-with-text, one a copy-pasted frame-with-text-with-icon — reads as busy because the eye registers them as three distinct things even when they're meant to behave identically. This is one of the most common busyness sources and it's invisible to a screenshot.

### Step 4 — The variance audit (the diagnostic that does most of the work)

This is the cheapest single call that tells me what's actually wrong. From the cookbook's "Token audit & cleanup" recipe:

```
search_all_unique_properties({
  parents: ["<the page or section being rescued>"],
  properties: [
    "fill", "textColor",
    "fontSize", "fontWeight", "fontFamily",
    "cornerRadius",
    "padding", "gap",
    "shadow", "stroke"
  ]
})
```

Expected response: each property mapped to a list of every distinct value present. This is the entire diagnosis in one payload. What I'd look for:

- **`fontSize` returns 9 distinct values.** That's the headline busyness — the eye can't build a hierarchy when there are 9 type sizes. A healthy small/medium screen uses 4–6 type sizes; a dense dashboard maybe 6–7. Anything above that is drift.
- **`fontWeight` returns more than 3 values.** Two or three weights is a hierarchy; four or more is noise.
- **`fill` and `textColor` show raw hex values mixed with `$variables`.** Drift from tokens. Each raw hex is a future drift point and a current "why is this slightly different" moment for the eye.
- **`shadow` returns more than two distinct values, or non-trivial shadows on more than ~20% of nodes.** Excessive elevation is a classic busyness pattern. The fix is usually "one elevation level, applied sparingly."
- **`gap` and `padding` return many close-but-not-equal values** (`12, 14, 16, 18, 20`). The spacing scale has been ignored. Snap them all to the nearest token.
- **`cornerRadius` shows three or more distinct values across roughly-equivalent surfaces** (cards, inputs, buttons all have different radii). Pick one, apply consistently.

**Decision rule.** If the `fontSize` list has more than 6 values OR the raw-hex / variable mix is high, the rescue is fundamentally a *consolidation* job, not a re-arrangement. Do step 5a first (collapse), THEN re-evaluate hierarchy (step 5b). Most of the time, just consolidating values is enough to fix the "where do I look" complaint, because once everything stops fighting for attention, the natural hierarchy reasserts itself.

### Step 5a — Consolidate (kill the variance)

For each property where the audit surfaced drift, decide the canonical set and use `replace_all_matching_properties` to collapse outliers.

Example for type:

```
replace_all_matching_properties({
  parents: ["<rescue target>"],
  properties: [
    { property: "fontSize", from: 13, to: "$textSm" },
    { property: "fontSize", from: 15, to: "$textBase" },
    { property: "fontSize", from: 17, to: "$textLg" },
    { property: "fontSize", from: 19, to: "$textXl" },
    { property: "fontSize", from: 22, to: "$text2xl" },
    { property: "fontSize", from: 30, to: "$text3xl" }
  ]
})
```

Same approach for raw colors that have a clear token equivalent, near-but-not-equal gaps that should snap to `$space-2/3/4`, and corner radii that should pick a single token.

A note from the cookbook I'd internalize: `replace_all_matching_properties` doesn't fuzzy-match — `15` only matches `15`, not `15.0`. So for each outlier value the audit surfaced, I issue an explicit mapping. I'd batch these as one call where possible.

After this call, I'd re-run the same `search_all_unique_properties` to confirm the unique-value lists shrank as expected. This is the cookbook's audit→replace→re-audit loop.

### Step 5b — Re-establish hierarchy (pick one hero)

Now that the design is no longer competing with itself for attention, I screenshot ONCE to see the current state with consolidated values:

```
get_screenshot({ nodeId: "<rescue target>" })
```

Scoped to the smallest meaningful node — never the document root if a section will do. SKILL.md is explicit: a typical task should need one or two screenshots total. This is the diagnostic-after-consolidation one.

When I scan the rendered image, I do it in the order from the verification ladder: layout integrity, spacing rhythm, type rhythm, contrast, component fidelity. For a "where do I look" rescue specifically, I add a sixth check at the top: **single hero check** — if I squint at the screenshot, can I name in one sentence what the page is for and where the primary action is? If not, the hierarchy is still wrong and step 5b proper begins.

The hierarchy fix is a small set of `U` ops, not a re-design:

- **Promote the hero.** The single most important element on the page (primary CTA, the headline, the chart that matters) gets the largest type, the strongest fill, and ideally is alone in its visual band — surrounded by negative space.
- **Demote the supporting cast.** Secondary actions become text buttons or outlined buttons; tertiary text steps down one or two sizes; secondary headings lose a weight; chrome elements (borders, dividers) move to a muted token.
- **Strip decorative elevation.** If everything has a shadow, nothing is elevated. Pull shadows off cards-of-equal-importance; reserve elevation for the actual focal layer.
- **Mute the non-essential color.** SKILL.md is direct: one accent, low saturation. If the design has three accents fighting (a brand blue button, a green "live" badge, a red error pill) and they're all at full saturation, the design feels carnival. Demote two of three to muted variants (`$primaryMuted`, `$successMuted`) and reserve the loudest one for a single role.

Each of these fixes is a `U` op. Example demotion:

```
batch_design ops:
U("secondaryCta",     { variant: "ghost", fill: "transparent", textColor: "$textMuted" })
U("liveBadge",        { fill: "$successMuted", textColor: "$success" })
U("sectionDividerA",  { stroke: { fill: "$border" } })
U("sectionDividerB",  { stroke: { fill: "$border" } })
U("heroCta",          { fontSize: "$textLg", fontWeight: "600" })
U("heroTitle",        { fontSize: "$text3xl", fontWeight: "700" })
```

(Real ids would come from `batch_get` against the rescue target with `readDepth: 3` so I know what I'm naming.)

### Step 5c — Add breathing room

A common cause of "too busy" is gap and padding values sized for the wrong density. If the audit showed that most gaps are `$space-2` (8px) but the content is text-heavy, the eye reads it as cramped. Bump section-level gaps up one notch:

```
U("pageRoot",          { gap: "$space-6" })
U("heroSection",       { padding: ["$space-8","$space-6","$space-8","$space-6"] })
U("contentSection",    { gap: "$space-5" })
```

I'd be conservative here — one step up the spacing scale, not two. Two looks like an over-correction.

### Step 6 — Verify (structural first, then one final pixel check)

Per the verification ladder, in order:

1. **`batch_design` response** — confirm ops succeeded. Free.
2. **`snapshot_layout({ parentId: "<rescue target>", maxDepth: 3 })`** — confirm the new gaps and padding landed as numbers. This is the cheap layout truth.
3. **`batch_get({ nodeIds: [<the nodes I demoted/promoted>] })`** — confirm `fill`, `textColor`, `fontSize` all resolved to variable bindings, not raw hex.
4. **`get_screenshot({ nodeId: "<rescue target>" })`** — final visual sign-off. Same scope as the diagnostic screenshot from step 5b. I scan in ladder order plus the squint test from step 5b. If the squint test now produces a clean answer ("this is the dashboard's revenue overview, the primary action is Export Report"), the rescue worked.

Total screenshots across the whole rescue: **2** — one diagnostic after consolidation, one final after re-hierarchy. Possibly only 1 if the consolidation alone solved the squint test.

### Step 7 — Hand back

One paragraph to the user: what was diagnosed (e.g. "the page had 9 distinct font sizes and 14 distinct fill colors, six of them raw hex"), what was changed at the value level ("collapsed type to 5 sizes from your `$textSm..$text3xl` scale, replaced 11 raw colors with `$primary`/`$primaryMuted`/`$success`/`$danger` bindings"), what was changed at the hierarchy level ("promoted the Export Report CTA, demoted the secondary filter buttons to ghost variants, removed shadows from the four sibling stat cards so the hero card reads as elevated"), and what I deliberately did NOT touch ("layout structure, copy, components themselves — only their instances on this page"). Stop.

## What I would not do

A few anti-reflexes worth naming, because the temptation is real on a "rescue" prompt:

- **Not screenshot before the audit.** Tempting because "too busy" sounds visual, but the audit (`search_all_unique_properties`) is cheaper, more precise, and tells me *what* to fix, not just that something is wrong. A screenshot before the audit produces a vague "yes, busy" confirmation and a lot of speculation.
- **Not redesign.** "Rescue" doesn't mean "reimagine." The user's design already has the bones they want — this protocol consolidates and re-tunes, it doesn't re-architect. If after step 5 the design still feels broken, that's the moment to surface "I can keep tuning, but at this point I think the layout itself isn't doing what you need — want me to propose a different structure?" — not before.
- **Not introduce new components.** If the inventory in step 3 surfaces a real component the page should be using instead of a hand-built lookalike, I'd swap it as part of step 5b. But I would not invent new library components mid-rescue.
- **Not mode-toggle screenshots.** SKILL.md is explicit: routine theme-aware designs (built from variables with both light/dark values) don't need a second screenshot in the alternate mode. The variable system guarantees mode parity. I'd only re-screenshot in dark mode if the consolidation in step 5a left raw hex values in place — and it shouldn't.
- **Not skip naming the atmosphere.** Before the hierarchy work in step 5b, I'd commit to a one-line vibe: e.g. "*airy, symmetric, static*" if the page is a marketing surface, or "*dense, symmetric, static*" if it's a dashboard. This forces the rescue to converge on one stance instead of oscillating.

## Confirmation

Wrote this response to `/Users/travis/Development/open-source/pencil-dev-skill/skills/pencil-design-workspace/iteration-1/eval-16-iteration-rescue-too-busy/old_skill/outputs/response.md`.
