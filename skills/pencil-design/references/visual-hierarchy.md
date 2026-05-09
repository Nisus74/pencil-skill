# Visual hierarchy

What makes a design *land*. The pattern of which elements lead, which support, which fade, and how the eye travels between them. Most designs that read as generic, AI-generated, or "balanced and forgettable" fail here. They don't fail at the token level.

**What this file owns:** the six levers (size, weight, colour, position, spacing, motion), primary/secondary/tertiary order, eye-flow patterns (F / Z / Gutenberg / centre), reading order discipline, whitespace as a tool, composition principles (rule of thirds, golden ratio, optical centre, visual weight balance), symmetry vs asymmetry strategy, density calibration.

**What this file does NOT own:** specific layout archetypes (hero variations, feature sections, dashboard layouts). That's `layout-patterns.md` (when scaffolded). The token system that backs the type and colour hierarchies. That's [`assets/design-system/tokens.md`](../assets/design-system/tokens.md). The mechanics of an element gaining contrast on hover. That's [`interactions.md`](interactions.md).

## When to load this file

- The design feels generic and you can't say why.
- The user names *hierarchy*, *visual weight*, *composition*, *whitespace*, *eye flow*, *contrast*, *balance*, *focus*, *density*, *busy*, *sparse*.
- You're auditing a design and the eye doesn't know where to go.
- A page passes every accessibility check, every design-system check, and still reads as flat or forgettable.

## The six levers

You have six tools to make one element dominate another. Use them deliberately.

| Lever | High-impact use | Low-impact use |
|-------|-----------------|----------------|
| **Size** | A 48px headline next to 16px body. The size ratio carries 80% of the hierarchy work. | Two body sizes that differ by 2px. Invisible. |
| **Weight** | Bold (700) heading next to regular (400) body. Or regular heading next to thin (300) body for a softer voice. | Semibold (600) vs regular (400) at the same size. Audible only at scale. |
| **Colour** | A saturated CTA against a muted neutral page. The eye lands on the CTA before any other element. | Two muted neutrals 5% apart. Separates them, but doesn't rank them. |
| **Position** | Top-left for primary nav, top-right for account/settings. Centre for a single focal action (sign-up). | Anything in a corner the user wouldn't think to look. |
| **Spacing** | 80px above a section heading sets it apart from the prior section. | 8px between two cards. They look related, but no hierarchy. |
| **Motion** | A primary CTA with a subtle hover lift. The user knows it's clickable. | Animating everything. The hierarchy collapses because nothing stands out. |

**Use the strongest lever you can afford.** Reach for size and colour before weight and motion; size and colour do more work with less complexity. Weight is for tone (bold reads confident; thin reads elegant), and isn't a hierarchy lever on its own.

**One element wins per layer.** Within a section (a card, a sidebar, a hero), one element dominates. Trying to make two things equally important at the same hierarchy level produces tension that reads as confusion. If two things are *actually* equally important, demote both and promote a third (a heading above them) so the layout reads "two equal items grouped under this category."

## Primary, secondary, tertiary

Every viewport has a hierarchy. State it before you design.

- **Primary.** What the user came here to do or see. There's one primary per view. *"Sign up", "Read the article", "Compare these two products", "See today's revenue."*
- **Secondary.** Supporting information or alternate paths. There can be 2–4 of these. *"Sign in instead", "Filter the article list", "Add to wishlist", "Last week's comparison."*
- **Tertiary.** Context, navigation, account chrome, footer. Important to have, never important to look at first. *"Help link", "Logo", "Notifications icon."*

Primary gets the strongest visual treatment your hierarchy allows: largest size *or* most-saturated colour *or* most-prominent position *or* a combination. Secondary gets visible-but-quieter treatment: same size as primary but lower contrast, or smaller and darker. Tertiary recedes. Small, low-contrast, edge-positioned.

**Common failure mode.** Two elements competing for primary status. A primary CTA and a secondary CTA at the same colour saturation. A page with three "main" headlines. A dashboard where every KPI card is identically prominent. The fix: pick one to win, demote the rest. If you can't choose, you haven't decided what the page is *for*.

## Eye-flow patterns

Where the eye lands first and how it moves. Choose the pattern that matches your content.

**F-pattern.** Reading-heavy pages (articles, blog posts, search results, long-form content). The eye reads the first line in full, scans down the left edge, and dips briefly into the middle of subsequent lines.

- Strong opening sentence / headline at the top.
- Sub-headings every 200–400 words to give the scanning eye anchors.
- Bullet lists and code blocks break the F because they reset the rhythm. Use them deliberately.

**Z-pattern.** Marketing pages, landing pages, low-density content. The eye traces a Z across the screen: top-left → top-right → diagonal down → bottom-right.

- Logo / brand top-left, primary nav top-right.
- Hero headline lands across the top.
- Hero CTA at the right end of the diagonal (where the eye finishes).
- Secondary CTA / scroll affordance at bottom-right.

**Gutenberg pattern.** Symmetric layouts, posters, single-purpose pages (an error page, a confirmation page, a hero with one focal point). The eye starts top-left (primary optical area), moves to bottom-right (terminal area), and pays less attention to top-right (strong fallow) and bottom-left (weak fallow).

- Use for centred, single-focus layouts.
- Don't use when the content has structure that demands F or Z reading.

**Centre-out (focused).** Modal-style content. The eye lands on whatever is centred and moves outward.

- Use for confirmation dialogs, focused tasks, hero sign-ups.
- Don't use for content lists or navigation.

In Pencil, name the eye-flow pattern in your atmosphere statement during step 4 (Plan): *"Dense dashboard, symmetric, static. F-pattern reading flow, left-aligned KPI rail, scannable."*

## Reading order = DOM order = focus order

The order children appear in a frame's children-array determines the order they're rendered, the order they receive focus, and the order screen readers announce them. The eye reads the *visual* order. If the visual order disagrees with the children-array order, you've created a tab-order trap and a screen-reader bug.

Rules:

- **Top-to-bottom, left-to-right by default.** Vertical-layout frames produce this naturally.
- **`layout: "none"` is a focus-order trap.** When children are absolutely positioned, the visual order can diverge from children-array order. The code generator follows the array, not the eyeballs. Either lay out with auto-layout, or explicitly state focus order in the parent's `context` for downstream to honour.
- **Don't visually reorder for stylistic reasons.** A primary CTA visually positioned top-right (because the design "looks better") but DOM-ordered after secondary content reads as a screen-reader bug. Fix the DOM order; let CSS / flex-order handle visual positioning if absolutely required.

This is also a SKILL.md § Naming consequence: nodes named in their reading order reinforce the hierarchy. A `LoginCard` containing children `EmailField → PasswordField → SubmitButton → ForgotPasswordLink` reads correctly. The same children in a different order would still render the same visual layout but feel wrong to the keyboard user.

## Whitespace as a tool

Whitespace is structural, even when it looks empty. The amount of space *around* an element determines how the element reads.

Three scales of whitespace:

- **Macro whitespace** between sections. 80–160px on marketing pages, 40–80px on app pages. This is the single most powerful "feels expensive" lever in design. Cramped sections read cheap; airy sections read premium. Most designs that "feel AI-generated" under-use macro whitespace.
- **Micro whitespace** between elements within a section. 16–32px between cards, 8–16px between text elements, 4–8px between adjacent UI primitives (icon + label, label + value).
- **Padding within elements.** 12–24px on cards, 8–16px on buttons, 16–32px on modals. Too little padding makes content read crowded inside its container; too much makes the container float.

**Use whitespace to group.** Elements close together read as related. Elements far apart read as unrelated. The most common hierarchy bug: a section heading floating equidistant between the section above and the section below, where neither section claims it.

**Use whitespace to rest the eye.** A page with no breathing room is exhausting. The eye needs places to land that aren't asking for attention. A blank quarter of the canvas is a feature, not waste.

**Calibrate density per audience.**

- A *consumer marketing site* runs airy (lots of macro whitespace, big type, restrained content density). The user is browsing, not working.
- A *power-user dashboard* runs dense (less macro whitespace, smaller type, more information per screen). The user is working, and the visit is repeated.
- *Mid-density product UI* sits between: enough whitespace to feel calm, enough density that the user doesn't scroll to find what they need.

When density is "dense", the rules above scale down. Macro whitespace at 24–40px, micro whitespace at 8–12px, padding at 8–16px. Don't apply marketing-page whitespace to a 200-row table; you'll just push everything offscreen.

## Composition principles

Centuries of design and art history boil down to a few rules that still hold.

**Rule of thirds.** Divide the canvas into a 3×3 grid. Place focal elements on the intersections (two-thirds points), not at centre. A hero image with the subject at 1/3 from left reads more dynamically than centred. A pricing card with the recommended tier at the visual centre but slightly offset right reads more deliberate.

**Golden ratio (1:1.618).** Body-copy column at 65 characters wide → headline column at ~105 characters. Card width 320 → card width 520. Sidebar 280 → main 720 (2.57 ratio is close enough to feel natural). Used quietly; never measured visibly.

**Visual weight balance.** Heavy elements (large, dark, saturated) on one side need balancing on the other. Use another heavy element, a cluster of smaller elements, or deliberate negative space. A page with all the weight on the left and nothing on the right feels like it's tipping over.

**Optical centre vs geometric centre.** The eye reads "centred" as slightly above the geometric middle. A modal positioned at exactly 50% from top *feels* low; position at ~42–45% to read as centred. Same for hero text, single-focus icons, isolated quotes. The optical centre is where the eye expects the focal point to be.

**Symmetry vs asymmetry.**

- *Symmetric* layouts read as formal and authoritative. Banks, government, healthcare, anywhere "trustworthy" matters. Easier to design well; harder to make memorable.
- *Asymmetric* layouts read as energetic and intentional, with a modern edge. Marketing, creative tools, anywhere "this product has taste" matters. Harder to design well; more memorable when it lands.

The default mistake is symmetric-by-accident. Every section is centred, every grid is 3 equal columns, every card is the same size. This reads as no decision was made. Either commit to symmetric (and use whitespace and type to give it life) or commit to asymmetric (and let the off-centre lines feel deliberate). Don't middle-ground.

**Tension and resolution.** Good composition has tension somewhere. An off-centre element, an oversized headline, a colour block that breaks the grid. Resolution somewhere else: the rest of the layout calmly accommodating the tension. All-tension is exhausting. All-resolution is forgettable, but in a quieter way. The classic move: one big tension at the hero, calm resolution through the body sections, a small tension at the closing CTA.

## Density strategy

Calibrate per page, per audience, per task.

**When to go airy:**
- Marketing pages, landing pages, sign-up flows.
- First-time-user surfaces (onboarding, empty states).
- Mobile (always less density than desktop).
- Tasks that benefit from focus (single-question forms, confirmations).

**When to go dense:**
- Power-user dashboards (the user is here daily).
- Data tables, lists with > 50 items.
- Side-by-side comparison views.
- Settings panels with > 20 controls.
- Any surface where scrolling cost > scanning cost.

**The density slider is a continuum, not an on/off switch.** Within a page, different regions can have different densities. An airy hero atop a dense data table is a valid composition. The whole page doesn't need one density.

**Test density at content-extremes.** Design at "expected content": 5 items in a list, average-length text. Then test at 0 items (does the empty state hold?), at 50 items (does it scroll smoothly?), and at one item with 4× the average text (does it overflow gracefully?). Density that works only at the average is fragile.

## Working with what you have

Often the layout is constrained by what already exists. A header you can't redesign, a sidebar pattern from the design system, content the user demands. The hierarchy work is then about making the *new* element fit the existing visual rhythm. It isn't about resetting the whole composition.

When auditing an existing design that feels generic, look for the layout's *one* missing tension: a section that's too symmetric, a hierarchy that's too flat, or a whitespace pattern that's too even. Adding one deliberate break often fixes the whole page.

## Pencil expression

The hierarchy disciplines above translate to specific Pencil patterns:

- **Frame structure.** A section's children-array order matches reading order. Use vertical/horizontal auto-layout to enforce this; use `layout: "none"` only when absolutely required (and document the focus order in `context`).
- **Spacing tokens.** Use `$space-*` tokens consistently per scale (macro/micro/padding). Mixing raw pixel values with tokens creates a hierarchy bug. The page reads inconsistent without the user knowing why.
- **Type tokens.** Headings step in the order `tokens.md` declares; never use heading sizes for non-heading text. The type hierarchy matches the visual hierarchy. See `tokens.md` for the project's scale.
- **Colour tokens.** Primary CTAs use the saturated accent token (`$accent`); secondary CTAs use the muted variant (`$accentMuted`); tertiary actions use a neutral (`$textMuted`). Don't pick raw colours for CTAs. The hierarchy collapses on theme change.
- **Atmosphere statement at step 4.** When you state your atmosphere ("dense dashboard, symmetric, static"), you're committing to a density and a composition rule for the whole design. Honour it.

## Verification checklist

Before declaring a design's hierarchy done:

1. **Squint test.** Squint at the design (or scale it down to 25%). Does the primary element still dominate? Are sections still distinguishable?
2. **Where does the eye go first?** Trace it. Match what you intended?
3. **Two-second test.** Show the design to a fresh viewer (or imagine doing so) for two seconds. Can they say what the page is for? If not, the hierarchy is unclear.
4. **Whitespace audit.** Is macro whitespace consistent (every section break the same scale)? Is micro whitespace consistent within sections? Are there places where the eye can rest?
5. **Hierarchy crowding.** Are there 2+ elements competing for primary status? Demote one.
6. **Reading order.** Tab through the design (mentally or actually). Does the order match the visual reading order?
7. **Density calibration.** Is the density right for the audience and task? Test at content extremes (empty / sparse / dense).
8. **Symmetric vs asymmetric.** Is one direction committed to? Or did it default to symmetric-by-accident?

Fix what fails. Don't ship a design with broken hierarchy and call it "balanced."

## See also

- SKILL.md § Aesthetic defaults. Atmosphere axes (density / variance / motion), colour and typography defaults that back the hierarchy.
- SKILL.md § Aesthetic defaults § Optical precision. ±1–2px adjustments, optical centre, icon-text contrast balance.
- SKILL.md § Aesthetic defaults § Self-critique gate. The 4-question gate that catches hierarchy bugs.
- [`interactions.md`](interactions.md). Interactions increase contrast (hover/focus carry *more* contrast than rest).
- [`modern-patterns.md`](modern-patterns.md). Modern hierarchy patterns (bento grids, asymmetric layouts, command palette as anchor).
- [`assets/design-system/layout.md`](../assets/design-system/layout.md). Project's spacing scale, grid, breakpoints.
- [`assets/design-system/tokens.md`](../assets/design-system/tokens.md). Type scale, colour tokens.
- [`assets/design-system/components.md`](../assets/design-system/components.md). Visual treatment of primary / secondary / tertiary actions.
