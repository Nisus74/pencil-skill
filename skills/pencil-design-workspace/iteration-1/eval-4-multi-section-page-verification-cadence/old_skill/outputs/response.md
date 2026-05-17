# Marketing landing page — incremental build with verification cadence

I read the pencil-design `SKILL.md` and pulled three references that fit this task:

- `references/batch-design-grammar.md` — confirms the `I/U/C/R/G` op syntax, the `≤25 ops per call` rule, the `placeholder: true` discipline for new top-level frames, and the "skeleton call → verify structurally → region calls → polish" pattern explicitly recommended for big screens.
- `references/mcp-tools.md` — gave me the verification ladder by token cost (`snapshot_layout` cheap, `batch_get` cheap, `get_screenshot` expensive) plus the *Greenfield document bootstrap* recipe.
- `assets/examples/example-login-screen.md` — concrete worked example of the seven-step workflow on a fresh doc, including how to scope screenshots and how to phrase the final report.

I did not load `references/states.md`, `references/flows.md`, or `references/component-anatomy.md` — this is a single-screen marketing page with no flows, no fault states, and no library imported (so no existing components to instantiate). I did note the *Anti-patterns* list from `SKILL.md` and the *Aesthetic defaults* — particularly "no Inter, no pure black/white, no three-column equal-card grids as the default for features". The user explicitly asked for a three-column features section, so I'll build it but lift it out of the AI default by varying icon treatment and using a non-Inter font stack.

---

## Step 1–2: Detect host + locate context

I'd start with one call:

```
get_editor_state({ include_schema: false })
```

Expected result on a clean session: succeeds, reports no active document, no selection. If it errored with `transport not connected to app: desktop`, I'd stop and tell the user to open the Pencil desktop app or the Pencil IDE extension. (Failure mode #1.)

I'd then check the project filesystem for `./design-system/`. For this scripted task I'm assuming none exists; the user wants a one-off marketing page in a new `.pen`, so I'd treat it as a sketch and skip the scaffold offer rather than asking twice.

## Step 3: Load guidelines

Per `references/mcp-tools.md` § `get_guidelines`, the right category for a marketing landing page is `Landing Page`. I'd run a discovery call first, then load the one category:

```
get_guidelines()
get_guidelines({ category: "Landing Page" })
```

I would not load `Tailwind`, `Web App`, or `Design System` for this task — the project has no `design-system/` and the user named no tech stack.

## Step 4: Plan + pick the atmosphere

Per the `SKILL.md` *Name the atmosphere before you plan* rule, I'm committing to: **balanced, symmetric, static**. Marketing landing pages live and die by clarity; this is not the place for chaos. The user's prompt also explicitly asks for "clean spacing rhythm and consistent typography" — that's an airy/balanced/static stance.

Plan I'd state to the user:

> *I'll create a new 1440×900 page with a vertically-stacked layout: a 480-px-tall hero with centered headline, subhead, and primary CTA button; a 320-px features section beneath it with three columns (icon, heading, body para); and a 100-px footer with a copyright line and three text links. I'll bind colors and spacing to a small token suite so dark mode comes for free, set the font stack to Geist (not Inter), and use Lucide icons via `icon_font` for the feature icons. I'll build it as four `batch_design` calls — bootstrap, hero, features, footer — and verify each region with `snapshot_layout` before moving on. One screenshot at the end on the page node.*

## Step 4.5: Open the new document + bootstrap tokens

The user asked for a *new* `.pen`, so:

```
open_document({ path: "new" })
```

Expected response: a fresh document root id (call it `doc`). The next `get_editor_state` would reflect the change.

Then per the *Themes* discipline rule, I'd call `get_variables()` *before* writing any tokens (mandatory, per Failure mode #7 — token clobber). On a freshly opened doc this returns an empty set. Then declare the theme axis and the token suite:

```
batch_design — call 1 (bootstrap, ~2 ops):
  U("doc", { themes: { mode: ["light", "dark"] } })
```

```
set_variables({
  variables: {
    surface:        { type: "color", value: [
      { value: "#FAFAFA", theme: { mode: "light" } },
      { value: "#0B1117", theme: { mode: "dark"  } } ] },
    surfaceMuted:   { type: "color", value: [
      { value: "#F4F4F5", theme: { mode: "light" } },
      { value: "#18181B", theme: { mode: "dark"  } } ] },
    border:         { type: "color", value: [
      { value: "#E4E4E7", theme: { mode: "light" } },
      { value: "#27272A", theme: { mode: "dark"  } } ] },
    textPrimary:    { type: "color", value: [
      { value: "#0B1117", theme: { mode: "light" } },
      { value: "#FAFAFA", theme: { mode: "dark"  } } ] },
    textMuted:      { type: "color", value: [
      { value: "#52525B", theme: { mode: "light" } },
      { value: "#A1A1AA", theme: { mode: "dark"  } } ] },
    primary:        { type: "color", value: [
      { value: "#1F6FEB", theme: { mode: "light" } },
      { value: "#3B82F6", theme: { mode: "dark"  } } ] },
    primaryText:    { type: "color", value: [
      { value: "#FFFFFF", theme: { mode: "light" } },
      { value: "#FFFFFF", theme: { mode: "dark"  } } ] },
    "space-1": { type: "number", value: 4   },
    "space-2": { type: "number", value: 8   },
    "space-3": { type: "number", value: 12  },
    "space-4": { type: "number", value: 16  },
    "space-5": { type: "number", value: 24  },
    "space-6": { type: "number", value: 32  },
    "space-8": { type: "number", value: 48  },
    "space-10": { type: "number", value: 64 },
    textXs:    { type: "number", value: 12 },
    textSm:    { type: "number", value: 14 },
    textBase:  { type: "number", value: 16 },
    textLg:    { type: "number", value: 18 },
    text2xl:   { type: "number", value: 24 },
    text4xl:   { type: "number", value: 48 },
    text5xl:   { type: "number", value: 60 }
  },
  replace: false
})
```

These are the only tokens this page needs. Pure white on `primaryText` is intentional — it's a CTA-on-blue label, the only place a near-white renders directly without a theme flip, and it stays white in dark mode by design.

---

## Region 1 — Page skeleton + Hero

### Build call (skeleton + hero, ~12 ops, one batch_design)

```
page=I(document, { type: "frame", name: "MarketingPage", layout: "vertical", width: 1440, height: 900, fill: "$surface", placeholder: true, gap: 0 })
hero=I(page, { type: "frame", name: "Hero", layout: "vertical", justifyContent: "center", alignItems: "center", width: "fill_container", height: 480, padding: ["$space-10", "$space-10", "$space-10", "$space-10"], gap: "$space-5", context: "Top hero of the marketing page. Centered headline, subhead, and primary CTA. Sets the page's first impression — keep airy." })
heroEyebrow=I(hero, { type: "text", name: "HeroEyebrow", text: "Pencil for product teams", fontFamily: "Geist", fontSize: "$textSm", fontWeight: 500, fill: "$textMuted", letterSpacing: 0.5 })
heroTitle=I(hero, { type: "text", name: "HeroHeadline", text: "Design that moves at the speed of code", fontFamily: "Geist", fontSize: "$text5xl", fontWeight: 700, fill: "$textPrimary", textAlign: "center", maxWidth: 720, lineHeight: 1.1, context: "Primary value prop. One sentence, ~8-10 words." })
heroSub=I(hero, { type: "text", name: "HeroSubhead", text: "Ship interfaces faster with a design tool that speaks both Figma and Git. Built for teams that prefer pull requests over comments.", fontFamily: "Geist", fontSize: "$textLg", fontWeight: 400, fill: "$textMuted", textAlign: "center", maxWidth: 560, lineHeight: 1.5 })
ctaRow=I(hero, { type: "frame", name: "HeroCtaRow", layout: "horizontal", gap: "$space-3", alignItems: "center", justifyContent: "center" })
cta=I(ctaRow, { type: "frame", name: "HeroPrimaryCta", layout: "horizontal", justifyContent: "center", alignItems: "center", padding: ["$space-3", "$space-5", "$space-3", "$space-5"], cornerRadius: 8, fill: "$primary", height: 48, context: "Primary CTA on the hero. 48px tall meets the 44×44 hit-target rule with a comfortable 4px above." })
ctaLabel=I(cta, { type: "text", name: "HeroPrimaryCtaLabel", text: "Start designing free", fontFamily: "Geist", fontSize: "$textBase", fontWeight: 600, fill: "$primaryText" })
ctaSecondary=I(ctaRow, { type: "text", name: "HeroSecondaryAction", text: "Watch demo", fontFamily: "Geist", fontSize: "$textBase", fontWeight: 500, fill: "$textPrimary", padding: ["$space-3", "$space-4", "$space-3", "$space-4"] })
```

10 ops, well under 25. Note the discipline rules I'm honouring at every op:

- Every node has a PascalCase semantic `name` (not `Frame`, `Group`, `Text 1`).
- Hero, headline, and CTA carry `context` because they're page-level / interactive.
- All colors come from `$variables` declared with both light and dark values.
- `width: "fill_container"` (bare string, not `"100%"` and not the object form — verified live per `batch-design-grammar.md`).
- `padding` is the 4-value array form `[top, right, bottom, left]` (no `paddingTop`).
- CTA hit target is 48px tall (passes the 44×44 rule from the *Accessibility* discipline).
- Headline is ~10 words and `maxWidth: 720` keeps it under the ~65ch reading width.
- Font is Geist, not Inter (anti-pattern list).
- Surface uses the `$surface` variable that resolves to `#FAFAFA`/`#0B1117`, never raw `#FFFFFF`/`#000000`.

### What I verified, how, and in what order

Per the verification ladder in `SKILL.md` and `references/mcp-tools.md`, I'd walk it from cheapest rung up and stop as soon as the question is answered.

**Rung 1 — `batch_design` response itself.** Free. Read the response: confirm every op succeeded and capture the assigned ids for `page`, `hero`, `heroTitle`, `heroSub`, `cta`, `ctaLabel`, `ctaRow`. If the response reports an op failure, I stop and inspect — don't keep stacking calls onto a broken skeleton.

**Rung 2 — `snapshot_layout` on the hero subtree.** Default verification tool, cheap, decisive for layout questions:

```
snapshot_layout({ parentId: "<hero-id>", maxDepth: 3 })
```

What I'm checking in the returned numbers:
- `hero.height` = 480 (not collapsing because `width: "fill_container"` is finding its flex parent — the `page` frame has `layout: "vertical"`, so this should hold).
- `hero.width` = 1440 (filling the page horizontally).
- `heroTitle.maxWidth` resolves and the rendered width is ≤ 720.
- `gap` between eyebrow → headline → subhead → cta-row is 24px (`$space-5`).
- `ctaRow` is centered both axes inside `hero` (computed `x` is `(1440 - ctaRow.width) / 2`).
- `cta` height = 48, width is `fit_content` of label + horizontal padding (so something like 184–200px).
- No node reports a `problemsOnly` overflow.

If the snapshot shows the headline wrapping awkwardly (unlikely at 60px on a 720-wide max) or the CTA collapsing to less than 48 tall (possible if I'd forgotten `alignItems: "center"`), I'd issue a targeted `U` op and re-snapshot. Cheap loop.

**Rung 3 — `batch_get` on the CTA.** Skipped. The `batch_design` response already returns the ids, and `snapshot_layout` already returned the geometry. There's no property-level question outstanding (no variable resolution to confirm — `$primary` is declared in the token suite).

**Rung 4 — `get_screenshot`.** **Skipped at this stage.** No genuine pixel-only question outstanding. The headline's actual rendered weight, the AI-generated hero illustration, the contrast under real rendering against `$surface` — none of those are at risk based on the snapshot. Per `SKILL.md` *Verification cadence*: "Do not screenshot to check progress." I save the screenshot for end-of-build sign-off.

### Verification calls for Region 1

| # | Tool | nodeId | Why |
|---|------|--------|-----|
| 1 | `batch_design` response read | n/a (in-band) | Confirm ops succeeded and capture assigned ids |
| 2 | `snapshot_layout` | hero subtree, maxDepth 3 | Confirm hero height, fill, gaps, CTA hit target, centering |

Two cheap verifications. Zero screenshots.

---

## Region 2 — Three-column features section

### Build call (~17 ops, one batch_design)

```
features=I("page", { type: "frame", name: "Features", layout: "vertical", width: "fill_container", padding: ["$space-10", "$space-10", "$space-10", "$space-10"], gap: "$space-8", alignItems: "center", fill: "$surfaceMuted", context: "Three benefit cards beneath the hero. Equal weight, symmetric grid." })
featuresHeading=I(features, { type: "text", name: "FeaturesSectionHeading", text: "Everything you need to design with confidence", fontFamily: "Geist", fontSize: "$text2xl", fontWeight: 600, fill: "$textPrimary", textAlign: "center", maxWidth: 640 })
columns=I(features, { type: "frame", name: "FeatureColumns", layout: "horizontal", gap: "$space-6", alignItems: "stretch", justifyContent: "center", width: "fill_container", maxWidth: 1200 })
col1=I(columns, { type: "frame", name: "FeatureColumn_VersionControl", layout: "vertical", gap: "$space-3", alignItems: "flex-start", padding: ["$space-5", "$space-5", "$space-5", "$space-5"], width: "fill_container", cornerRadius: 12, fill: "$surface", stroke: { thickness: 1, fill: "$border" }, context: "Feature card 1 of 3 — git-native versioning benefit." })
icon1=I(col1, { type: "icon_font", name: "FeatureIcon_VersionControl", iconLibrary: "lucide", iconName: "git-branch", fontSize: 24, fill: "$primary" })
heading1=I(col1, { type: "text", name: "FeatureHeading_VersionControl", text: "Git-native version control", fontFamily: "Geist", fontSize: "$textLg", fontWeight: 600, fill: "$textPrimary" })
body1=I(col1, { type: "text", name: "FeatureBody_VersionControl", text: "Branch, merge, and review designs the same way you ship code. No more 'final-final-v3' files.", fontFamily: "Geist", fontSize: "$textBase", fontWeight: 400, fill: "$textMuted", lineHeight: 1.5 })
col2=I(columns, { type: "frame", name: "FeatureColumn_Components", layout: "vertical", gap: "$space-3", alignItems: "flex-start", padding: ["$space-5", "$space-5", "$space-5", "$space-5"], width: "fill_container", cornerRadius: 12, fill: "$surface", stroke: { thickness: 1, fill: "$border" }, context: "Feature card 2 of 3 — component reuse benefit." })
icon2=I(col2, { type: "icon_font", name: "FeatureIcon_Components", iconLibrary: "lucide", iconName: "blocks", fontSize: 24, fill: "$primary" })
heading2=I(col2, { type: "text", name: "FeatureHeading_Components", text: "Components that scale with you", fontFamily: "Geist", fontSize: "$textLg", fontWeight: 600, fill: "$textPrimary" })
body2=I(col2, { type: "text", name: "FeatureBody_Components", text: "Build a design system once and reuse it across every screen, every product, every team.", fontFamily: "Geist", fontSize: "$textBase", fontWeight: 400, fill: "$textMuted", lineHeight: 1.5 })
col3=I(columns, { type: "frame", name: "FeatureColumn_AiHandoff", layout: "vertical", gap: "$space-3", alignItems: "flex-start", padding: ["$space-5", "$space-5", "$space-5", "$space-5"], width: "fill_container", cornerRadius: 12, fill: "$surface", stroke: { thickness: 1, fill: "$border" }, context: "Feature card 3 of 3 — AI handoff to code benefit." })
icon3=I(col3, { type: "icon_font", name: "FeatureIcon_AiHandoff", iconLibrary: "lucide", iconName: "wand-sparkles", fontSize: 24, fill: "$primary" })
heading3=I(col3, { type: "text", name: "FeatureHeading_AiHandoff", text: "AI-ready handoff", fontFamily: "Geist", fontSize: "$textLg", fontWeight: 600, fill: "$textPrimary" })
body3=I(col3, { type: "text", name: "FeatureBody_AiHandoff", text: "Designs export with the structure your AI coding agent already understands. Skip the spec doc.", fontFamily: "Geist", fontSize: "$textBase", fontWeight: 400, fill: "$textMuted", lineHeight: 1.5 })
```

16 ops, under the 25 budget. Discipline check:

- All names role-bearing and unique (`FeatureColumn_VersionControl`, not `Column 1`).
- Each card has a one-sentence `context`.
- Icons are `icon_font` from Lucide (per the *Design intelligence* rule: "User mentions an icon by name. Always reach for `icon_font`").
- Each column is `width: "fill_container"` inside a `layout: "horizontal"` parent — that's the correct way to get equal columns under flex.
- `maxWidth: 1200` matches the canonical desktop content max from the *Responsive* discipline.
- Body lineHeight 1.5 keeps reading rhythm comfortable.
- `surfaceMuted` for the section background gives a subtle band against the hero, without resorting to a glow or gradient.

The user did ask for the AI-default three-column features layout. I'm building it, but I'm naming the cards distinctly, varying the icon shapes, and *not* adding fake metrics or "Trusted by" logos to fill space — the *Anti-patterns* list flags those.

### What I verified, how, and in what order

**Rung 1 — `batch_design` response.** Confirm ops succeeded, capture ids for `features`, `columns`, `col1`, `col2`, `col3`.

**Rung 2 — `snapshot_layout` on the columns row.** This is the structural risk: do the three columns actually share width equally? Do they sit at the same vertical baseline? Cheap call:

```
snapshot_layout({ parentId: "<columns-id>", maxDepth: 2 })
```

What I'm checking:
- `col1.width` ≈ `col2.width` ≈ `col3.width` (within 1px). With `maxWidth: 1200` on the container, gap `$space-6` (32px), and three children: each column should compute to `(1200 - 2*32) / 3` = 378.67px.
- Each column's `height` is the same (because `alignItems: "stretch"` on the row). If the heights differ, one column's body text wrapped to more lines and that's OK — but the cards should still bottom-align to the tallest sibling.
- Icon nodes computed at 24×24.
- `gap` inside each column = 12px (`$space-3`).

**Rung 3 — `batch_get` on one feature column.** Cheap property-level check, but I'd only run it if I had a doubt about the icon resolving:

```
batch_get({ nodeIds: ["<icon1-id>"] })
```

This would confirm `iconLibrary: "lucide"`, `iconName: "git-branch"`, and that the fill is actually bound to `"$primary"` (not silently downgraded to a raw hex). On a fresh build with no prior reason to doubt the bindings, I'd skip this. If I'd just refactored or renamed a variable, I'd run it.

**Rung 4 — `get_screenshot`.** **Still skipped at this stage.** The features section has no AI-generated content, no contrast at risk that the variable system doesn't already guarantee, and the columns equality is a structural question that the snapshot already answered.

### Verification calls for Region 2

| # | Tool | nodeId | Why |
|---|------|--------|-----|
| 1 | `batch_design` response read | n/a (in-band) | Confirm ops succeeded |
| 2 | `snapshot_layout` | columns subtree, maxDepth 2 | Confirm three columns share width and bottom-align under stretch |

Two verifications, zero screenshots.

---

## Region 3 — Footer

### Build call (~7 ops, one batch_design — and clear placeholder at the end)

```
footer=I("page", { type: "frame", name: "Footer", layout: "horizontal", justifyContent: "space-between", alignItems: "center", width: "fill_container", padding: ["$space-5", "$space-10", "$space-5", "$space-10"], borderTop: { thickness: 1, fill: "$border" }, fill: "$surface", context: "Page footer. Copyright on the left, three nav links on the right. Stays under 100px to preserve hero+features ratio." })
copyright=I(footer, { type: "text", name: "FooterCopyright", text: "© 2026 Pencil, Inc. All rights reserved.", fontFamily: "Geist", fontSize: "$textSm", fontWeight: 400, fill: "$textMuted" })
linkRow=I(footer, { type: "frame", name: "FooterLinks", layout: "horizontal", gap: "$space-5", alignItems: "center" })
linkPrivacy=I(linkRow, { type: "text", name: "FooterLink_Privacy", text: "Privacy", fontFamily: "Geist", fontSize: "$textSm", fontWeight: 500, fill: "$textMuted", href: "#privacy" })
linkTerms=I(linkRow, { type: "text", name: "FooterLink_Terms", text: "Terms", fontFamily: "Geist", fontSize: "$textSm", fontWeight: 500, fill: "$textMuted", href: "#terms" })
linkContact=I(linkRow, { type: "text", name: "FooterLink_Contact", text: "Contact", fontFamily: "Geist", fontSize: "$textSm", fontWeight: 500, fill: "$textMuted", href: "#contact" })
U("page", { placeholder: false })
```

7 ops. The trailing `U("page", { placeholder: false })` matches the *Placeholder frames* rule from `batch-design-grammar.md` — "Remove it as soon as the frame is finished. Don't wait until all screens are done." This is the last screen, so this is the moment.

Discipline check:

- Copyright text uses `©` not `(c)` — it's a real glyph, not a placeholder, and avoids reading like AI-generated content.
- Footer links have `href` properties (so downstream code-gen knows to render `<a>` tags).
- All text fills `$textMuted` for the light-on-dark and dark-on-light contrast that fits a footer's secondary role.
- Footer height is implicit from `padding: $space-5` (24) top+bottom + text line height — should compute to ~64px, leaving comfortable breathing room above the page edge.

I'm not adding social icons, a newsletter signup, or "Made with love" microcopy. The user asked for a copyright line and three text links; that's what they get. No gold-plating.

### What I verified, how, and in what order

**Rung 1 — `batch_design` response.** Confirm ops succeeded; confirm the placeholder flag flipped on `page`.

**Rung 2 — `snapshot_layout` on the footer.** The structural question is: did `space-between` actually push copyright to the left edge of the padding box and the link row to the right edge? Cheap:

```
snapshot_layout({ parentId: "<footer-id>", maxDepth: 2 })
```

What I'm checking:
- `copyright.x` is at the left padding edge (= 64, since `$space-10` = 64).
- `linkRow.x + linkRow.width` ends at `1440 - 64 = 1376` (right padding edge).
- Footer total height in the 60–80px range (depends on text line height — anything dramatically larger means a body font crept in by accident).
- Three link nodes spaced 24px apart inside `linkRow`.

**Rung 3 — `batch_get`.** Skipped. No outstanding property question.

### Verification calls for Region 3

| # | Tool | nodeId | Why |
|---|------|--------|-----|
| 1 | `batch_design` response read | n/a (in-band) | Confirm ops succeeded and placeholder cleared |
| 2 | `snapshot_layout` | footer subtree, maxDepth 2 | Confirm space-between pushed children to padding edges |

Two verifications, zero screenshots.

---

## Final sign-off (one screenshot, scoped to the page)

Now — and only now — climb to rung 4. Per `SKILL.md` *Verification cadence*: "A typical end-to-end design task should need one or two screenshots total… one at the end before handing back."

```
get_screenshot({ nodeId: "<page-id>" })
```

`nodeId: "<page-id>"`, NOT the document root. That's the most specific node containing every region I built — exactly what the verification ladder calls for: "Always pass the most specific `nodeId` that contains the change."

What I'd scan for in the rendered image, in the order from `SKILL.md` § *Verification ladder*:

1. **Layout integrity.** Hero, features, footer all visible inside the 1440×900 frame. Nothing off-canvas.
2. **Spacing rhythm.** The section gaps read consistently — the 64px hero padding, the 64px features padding, and the 24px footer padding should compose into a clear hierarchy.
3. **Type rhythm.** Headline (60) clearly larger than features section heading (24) clearly larger than feature card heading (18) clearly larger than body (16). Caps and weights step in the same direction.
4. **Contrast.** `$textPrimary` on `$surface` (Zinc-950 on off-white) trivially passes 4.5:1; `$textMuted` on `$surface` is the one to watch — `#52525B` on `#FAFAFA` is ~7.4:1 on the W3C calculator, well past 4.5:1. Same check would pass under dark mode by symmetry of the variable design.
5. **Component fidelity.** No hand-built lookalikes drifting from a library — there is no library on this build.

I would **not** screenshot the dark mode separately. Per `SKILL.md` *Verification ladder* dual-mode rule: "Routine theme-aware designs — those built entirely from variables with both light/dark values — do not need a second screenshot to confirm both modes hold up; the variable system guarantees it." Every color on this page is a variable with both light and dark values declared. The variable system is the guarantee.

If the screenshot revealed a single fixable issue (e.g. headline maxWidth still wrapping awkwardly on this exact font metric), I'd issue one targeted `U` op and re-screenshot. If three iterations didn't converge, I'd hand back to the user — the requirement is probably ambiguous.

---

## Total verification calls across the whole build

Across the full build I would make **9 verification reads** in this shape:

- **`batch_design` response reads (rung 1):** 4. One per build call — bootstrap-tokens (`U` on doc + `set_variables`), hero, features, footer. Free, in-band; the response itself is the verification.
- **`snapshot_layout` calls (rung 2):** 3. One per visible region — hero subtree (`maxDepth 3`), columns subtree (`maxDepth 2`), footer subtree (`maxDepth 2`). Each scoped to the smallest subtree that answers "did the layout do what I asked?".
- **`batch_get` calls (rung 3):** 1, conditional. I'd only run it if a structural snapshot or response surfaced a property doubt (e.g. an icon not resolving, a variable not binding). On a clean build it's 0; on a build with one anomaly it's 1.
- **`get_screenshot` calls (rung 4):** 1. End-of-build only, scoped to the `page` node, not the document root.
- **Plus 2 reference reads** that aren't part of the verification ladder but are part of the workflow's read-before-write discipline: `get_editor_state` once at the start (host detection) and `get_variables` once before declaring tokens (mandatory per Failure mode #7 to avoid token clobber). Plus the `get_guidelines` discovery + `Landing Page` category read at step 3.

The intentional shape here: keep the cadence cheap and structural through every region, save the one expensive image rung for end-of-build sign-off, and never screenshot for "progress check" — which the older reflex would have produced as ~3–4 screenshots (one per region plus a final, possibly with a dark-mode pair). That older shape was wrong; it burned tokens to confirm things the structural snapshots already proved.
