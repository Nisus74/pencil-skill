# Reference ingestion

How the skill handles user-supplied references, screenshots, URLs, named brands, hand-written notes, and synthesises them into an *ephemeral archetype* that overrides the shipped library for the current session.

This is the contract for step 1 of the new SKILL.md flow when the user has supplied direction.

## Precedence rule (the most important sentence on this page)

**Per-session references always override shipped archetypes.** If the user has provided any direction, a screenshot, a brand name, a URL, a description, that direction is the source of truth. The shipped archetype library exists for the case when the user is silent.

When in doubt: do what the user said, not what the closest shipped archetype says.

## Triggers

The skill runs the ingestion flow when the user does any of the following at any point in a session:

- **Pastes an image into chat** that depicts UI (a product screenshot, a Figma export, a Dribbble shot, a competitor screen).
- **Names a product** as the design target (*"build it like Linear"*, *"make it feel like Stripe"*, *"Notion-style"*).
- **Pastes a URL** to a product or design page (the skill cannot fetch URLs but can ask the user to screenshot or paste content).
- **Describes an aesthetic in prose** (*"refined, generous whitespace, mono numerals"*, *"brutalist with aggressive type"*).
- **References an existing design file** they've shared in the conversation.

If two or more of these arrive together (a screenshot AND a brand name), treat them as complementary inputs to a single ephemeral archetype.

## What to extract from each input type

### Screenshot of UI

Look for and name out loud what you see, in this order:

1. **Surface category.** Is this a dashboard, a marketing site, a mobile app, a settings page? This determines the candidate shipped archetypes to compare against.
2. **Light or dark mode.** Which is canonical? Is the design only shown in one mode?
3. **Type pairing.** Display font (if visible character shapes are distinctive, geometric sans, humanist sans, serif, mono). Body font. Numeral treatment (mono or proportional).
4. **Density mode.** Airy, balanced, dense. Look at row padding, card padding, line-height.
5. **Accent strategy.** What's the accent colour? Where does it appear (CTA only, active states, charts, multiple places)? Is it saturated or muted?
6. **Surface treatment.** Borders or shadows? Corner radii, sharp, medium, fully rounded? How many surface levels (page > card > muted)?
7. **Layout grammar.** Sidebar + main? Top bar + columns? Centred narrative? Card grid? Notice the structural choices.
8. **Signature moves.** Anything specific that isn't generic, keyboard-shortcut chips, status pills with dots, decimal section labels, specific empty-state pattern.
9. **Microcopy hints.** Any visible text, headlines, labels, button copy. Is it terse, lowercase, sentence-case, ALL CAPS?

Output a written archetype description (short, under 100 lines) following the standard archetype template. Save it to the session's design spec under "Aesthetic commitment".

### Named product (no screenshot)

Match against the shipped archetypes first, many products have known archetype mappings:

| Named product | Closest shipped archetype |
|---|---|
| Linear (app) | `saas-apps/b2b/modern-pro-tool` |
| Linear (marketing) | `marketing-websites/conversion-focused-saas` |
| Mixpanel / Amplitude / PostHog | `saas-apps/b2b/analytics-dashboard` |
| Notion (personal) | `saas-apps/b2c/consumer-productivity` (when populated) |
| Notion (business) | `saas-apps/b2b/modern-pro-tool` |
| Stripe (marketing) | `marketing-websites/conversion-focused-saas` |
| Apple product pages | `marketing-websites/editorial-storytelling` |
| Linear Method page | `marketing-websites/editorial-storytelling` |
| Claude / ChatGPT | `ai-products/conversation-chat` (when populated) |

If the named product matches a shipped archetype directly, use that archetype as the source of truth and inform the user: *"`<product>` matches the `<archetype>` archetype in the library. Loading that as the source of truth."*

If the named product doesn't match a shipped archetype but you have public knowledge of it, draft an ephemeral archetype from inference and explicitly flag *"this is from public knowledge of `<product>`; if you have screenshots they'll improve the result."*

If the named product is unknown to you, ask for screenshots.

### URL (no screenshot)

The skill cannot fetch external URLs. Respond:

> *"I can't fetch URLs directly. Can you paste a screenshot of `<URL>`, or summarise the moves you want me to capture from it? If it's a public, well-known product I can also work from public knowledge if you confirm."*

Don't make up content for a URL you can't see.

### Prose description

Treat the description as authoritative for the dimensions it covers. If the user says *"refined, generous whitespace, mono numerals on data"*, lock those three moves and infer the rest from context, the surface category, the user's domain, related shipped archetypes.

If the description is sparse (one or two adjectives), ask one clarifying question before locking the ephemeral. *"Refined and minimal, should I assume light surfaces with hairline borders, or are you thinking of a darker, monumental kind of minimal?"*

### Existing design file

If the user shares a `.pen` file or a Figma file, treat the existing design as the strongest possible reference:

1. `batch_get` the existing design's structure.
2. `get_screenshot` the most representative frame.
3. Extract the same dimensions as a screenshot ingestion (typography, density, accent, surface, etc.).
4. Apply the extracted ephemeral archetype to anything new you build, so the new work matches the existing design's grammar.

## Synthesising the ephemeral archetype

Once the inputs are extracted:

1. **Name it.** Pick a kebab-case name that reflects the dominant moves. Pattern: `<dominant-mood>-<flavour>`. Examples: `linear-pro-dense`, `editorial-warm-serif`, `brutal-mono-statement`. The name is for this session only; it doesn't go into the shipped library.
2. **Write it as an archetype-shaped block** in the design spec under "Aesthetic commitment". Use the same 11-section template as shipped archetypes; sections that the references don't speak to can be marked *"inherit from `<closest-shipped-archetype>`"*.
3. **Announce it to the user.** Output: *"Synthesising ephemeral archetype `<name>` from your reference. This overrides any shipped archetype for this session. Tell me to revise if I've misread anything."*
4. **Wait for confirmation or correction.** Don't start `batch_design` until the user has either approved or revised the synthesis.

## Promotion path (per-session → shipped)

If a per-session ephemeral keeps producing strong work across multiple projects, it's a candidate to graduate into the shipped library. The path:

1. User opens a PR against this repo's `assets/archetypes/<category>/<name>.md`.
2. The PR uses the same 11-section template as existing shipped archetypes.
3. Description in our own words; cite real exemplars; no third-party screenshots committed.
4. The PR adds the new archetype to the relevant category README's "Picking between them" table.
5. Bump the skill MINOR version (new archetype = new capability).

Promotion is opt-in. A per-session ephemeral that worked once doesn't have to graduate; many will stay session-local.

## Anti-patterns

- **Ignoring the user's reference because it doesn't match a shipped archetype perfectly.** The reference wins. Synthesise an ephemeral; don't force-fit.
- **Asking 4 clarifying questions before doing anything.** One is fine; four reads as obstruction. If the reference is ambiguous, draft something and ask the user to correct it.
- **Treating a screenshot as decorative.** Read it. Extract the moves. Otherwise the user just sent you noise.
- **Synthesising silently.** Always announce the ephemeral and what it overrides, so the user can correct course before you commit time.
- **Fabricating moves the reference doesn't show.** If the screenshot shows light mode and the user said nothing about dark mode, don't invent a dark variant. Ask.
- **Loading multiple shipped archetypes "to be safe" when the user gave a clear reference.** One source of truth per session.
