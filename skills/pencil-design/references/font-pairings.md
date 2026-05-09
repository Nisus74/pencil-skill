# Font pairings

A library of 30+ typography *recipe pairings* the agent picks from when starting greenfield. Each entry names the fonts (and their source: Google Fonts, Vercel Geist, GitHub Mona Sans, or commercial foundries) and the weights to ship. The agent picks once, commits the choice to `assets/design-system/tokens.md` and the `.pen` file's `variables`, then references font tokens (`$fontBody`, `$fontMono`) in every subsequent design.

**What this file owns:** named font-pairing recipes with mood, industry fit, anti-pattern, real-world exemplar, weights to ship, and licensing/source notes.

**What this file does NOT own:** the project's *committed* type scale. That lives in `assets/design-system/tokens.md` (project-owned, version-controlled) and in the `.pen` file's `variables` section (the live design's typography). Typography rules (tabular numerics, text-wrap balance, optical sizing) are in `SKILL.md` § Aesthetic defaults: Typography. Letter-spacing and tracking discipline is in [`iteration-patterns.md`](iteration-patterns.md) § Failure mode: doesn't feel premium.

## When to load this file

- The agent is starting a greenfield design and the project has no committed type pairing yet.
- The user names a typeface ('use Söhne', 'something like Linear's type') or a mood ('editorial', 'developer-tool feel').
- The agent is following [`example-style-selection.md`](../assets/examples/example-style-selection.md) (Phase 4) and needs to pick the font half of the style + palette + font triple.
- The user wants alternatives to a specific font that's commercial-only.

## How this catalogue works (architecture)

Three layers; the catalogue sits at the top.

1. **This file (`references/font-pairings.md`)** is a *menu of starting recipes*. Each recipe names a font pairing with weights and sources. The recipes don't hold the project's typography; they're the starting point.
2. **The source services** ship the actual font files. Google Fonts (https://fonts.google.com), Vercel Geist (https://vercel.com/font), GitHub Mona Sans (https://github.com/mona-sans), and the commercial foundries listed per recipe.
3. **`assets/design-system/tokens.md`** records the project's *committed* type scale. The agent records the chosen pairing here as semantic tokens (`$fontDisplay`, `$fontBody`, `$fontMono`, plus weight, size, and line-height scales). This file is project-owned; the user can edit it.
4. **The `.pen` file's `variables` section** is the live design's typography. The agent calls `set_variables` MCP to populate the variables from the project's `tokens.md`. Designs reference `$fontBody`, `$fontMono`, never literal font names.

The rule: **the agent reads this catalogue once at the start of a project, then never again.** Subsequent designs reference the project's variables. If the user wants to change typography, they edit `tokens.md` and the `.pen` variables; this catalogue stays untouched.

## Workflow (greenfield)

1. Identify the project's mood and industry from the brief, or ask the user.
2. Cross-check with the chosen style from [`style-catalogue.md`](style-catalogue.md). A Brutalist project doesn't get Editorial Serif; a Swiss / International project doesn't get Memphis-style display fonts.
3. Pick a pairing from the matching family below.
4. Lift the font URLs from the source service (Google Fonts CDN or self-host) into the project's HTML head.
5. Populate `assets/design-system/tokens.md` with the chosen pairing as semantic tokens (`$fontDisplay`, `$fontBody`, `$fontMono`) plus the weight scale.
6. Call `set_variables` MCP to mirror the type tokens into the `.pen` file's `variables` section.
7. Record the chosen pairing recipe name in `assets/design-system/visual-style.md`.
8. From this point onward, design with `$fontBody`, `$fontMono`, etc. Never hard-code font names in `batch_design`.

## Pairing entries

Each entry covers: **Pairing** / **Mood** / **Heading + body weights** / **When to use** / **Anti-pattern** / **Exemplar** / **Source**.

## Sans + Mono (developer tools, technical SaaS)

The dominant family for B2B SaaS in 2025/2026. The mono is for code blocks, IDs, kbd shortcuts, tabular numerics.

| Pairing | Mood | Recommended weights | When to use | Anti-pattern | Exemplar | Source |
|---|---|---|---|---|---|---|
| **Inter + JetBrains Mono** | Calm, neutral, modern | Inter 400/500/600/700; JetBrains Mono 400/500 | Default modern SaaS, developer tools, productivity | The 'safe choice' tell. Add a display font or unusual accent if the design feels generic | Linear, Vercel (in places) | Google Fonts (both free) |
| **Inter + Inter** | Utility, restrained | Inter 400/500/600/700/900 | When a single typeface keeps things quiet; or when budget for fonts is one | Headings without enough weight contrast vs body | Notion, Cron (now Notion Calendar) | Google Fonts |
| **Geist + Geist Mono** | Modern, dev-tool, sharp | Geist 400/500/600/700; Geist Mono 400/500 | Developer tools shipping on Vercel; modern dev-adjacent SaaS | Reading too much like Vercel-clone. Pair with a distinctive accent | Vercel, several modern dev tools | Vercel (free, https://vercel.com/font) |
| **IBM Plex Sans + IBM Plex Mono** | Technical, slightly editorial, established | Plex Sans 400/500/600/700; Plex Mono 400/500 | Enterprise developer tools, technical documentation, IBM-adjacent ecosystems | Very recognisable; can read as 'corporate IBM' | IBM products, several tech publications | Google Fonts, also https://www.ibm.com/plex |
| **Mona Sans + Hubot Sans** | Modern, friendly, GitHub | Mona Sans 400/500/600/700; Hubot Sans for display | Developer tools, code-adjacent products, GitHub ecosystem | Reading as GitHub-clone | GitHub, GitHub Copilot marketing | GitHub (free, https://github.com/mona-sans) |
| **Söhne + Söhne Mono** | Premium, modern, restrained | Söhne 400/500/600/700; Söhne Mono 400/500 | Premium SaaS where licensing budget exists | Commercial; budget barrier | Stripe, ChatGPT/OpenAI, Cosmos | Klim Type Foundry (commercial, https://klim.co.nz/buy/sohne/). Free alternative: Inter or Mona Sans |
| **Berkeley Mono + Inter** | Programmer-aesthetic, mono-led | Berkeley Mono 400/700; Inter 400/600 for prose | Indie developer tools, programmer-as-audience products | Mono-only display can be hard to read at very small sizes | several indie dev tools, Berkeley Mono in editorial use | Berkeley Graphics (commercial, https://berkeleygraphics.com/typefaces/berkeley-mono/). Free alternative: JetBrains Mono |

## Sans + Sans (modern utility)

When the design wants quiet, modern, type-as-system.

| Pairing | Mood | Recommended weights | When to use | Anti-pattern | Exemplar | Source |
|---|---|---|---|---|---|---|
| **DM Sans + DM Sans** | Modern, friendly, geometric | 400/500/700 | Consumer-leaning SaaS, friendly products | Lacks distinctiveness when used at default settings | several modern marketing sites | Google Fonts |
| **Manrope + Manrope** | Geometric, modern, slightly playful | 400/500/600/700/800 | Modern SaaS that wants warmth without going serif | Heavy weights can feel chunky | several startup marketing sites | Google Fonts |
| **Plus Jakarta Sans + Plus Jakarta Sans** | Modern, slightly humanist | 400/500/600/700/800 | Default sans alternative to Inter when wanting more personality | Reads slightly Indonesian-design-adjacent (its origin) | several modern SaaS sites | Google Fonts |
| **Outfit + Outfit** | Modern geometric, friendly | 300/400/500/600/700 | Marketing pages wanting friendly modern feel | Display sizes need optical fixes (kerning) | Outfit's own site, several marketing pages | Google Fonts |
| **Sora + Sora** | Modern grotesque, technical-friendly | 300/400/500/600/700 | Technical SaaS wanting subtle personality | Less character at body sizes | several modern SaaS | Google Fonts |

## Serif + Sans (editorial, premium)

When the heading wants gravitas; the body stays clean.

| Pairing | Mood | Recommended weights | When to use | Anti-pattern | Exemplar | Source |
|---|---|---|---|---|---|---|
| **Source Serif + Source Sans** | Editorial, considered | Source Serif 400/600/700; Source Sans 400/600 | Long-form publishing, knowledge bases, premium SaaS marketing | Reads slightly Adobe-corporate at body sizes | several knowledge bases, Adobe products | Google Fonts |
| **Fraunces + Manrope** | Warm-modern, editorial-friendly | Fraunces 400/600/900 (variable); Manrope 400/600 | Premium SaaS wanting warmth; editorial-leaning marketing | Fraunces' SOFT settings can read as twee | Pitch (pitch.com), several premium SaaS sites | Google Fonts |
| **DM Serif Display + DM Sans** | Editorial-modern, slightly playful | DM Serif Display 400; DM Sans 400/500/700 | Marketing pages wanting display-serif heroes | DM Serif Display only ships in one weight; restricts hierarchy | several modern marketing sites | Google Fonts |
| **Recoleta + Inter** | Warm-editorial, premium | Recoleta 300/400/500/600/700; Inter 400/500/600 | Premium SaaS, high-end consumer | Recoleta is commercial; Fraunces is the closest free alternative | Substack, several premium SaaS marketing sites | Recoleta (commercial, https://djr.com/notes/recoleta-introduction). Free alternative: Fraunces |
| **GT Sectra + Inter** | Premium editorial, considered | GT Sectra 400/700; Inter 400/500/600 | Premium publications, editorial SaaS, high-end consumer | Commercial; budget barrier | several editorial sites, Medium-style products | Grilli Type (commercial, https://www.grillitype.com/typeface/gt-sectra). Free alternative: Fraunces or Source Serif |
| **Playfair Display + Inter** | Classic-editorial, decorative | Playfair Display 400/700/900; Inter 400/500 | Wedding sites, vintage-leaning publications, Italianate brands | Overused; reads as default 'fancy' if not handled deliberately | many wedding/lifestyle sites | Google Fonts |
| **Cormorant Garamond + Inter** | Premium-classical, considered | Cormorant Garamond 400/600; Inter 400/500/600 | High-end consumer, fashion, hospitality | Cormorant's italics need care at small sizes | several fashion and hospitality sites | Google Fonts |
| **Crimson Pro + Inter** | Academic, scholarly, considered | Crimson Pro 400/600/700; Inter 400/500/600 | Academic publishing, research platforms, long-form journalism | Reads slightly old-fashioned without modern accent | several academic sites | Google Fonts |
| **Lora + Inter** | Calm-editorial, contemporary | Lora 400/500/600; Inter 400/500 | Blogs, modern publications, contemporary editorial | Less distinctive than Fraunces; safer | Many Medium-style blogs | Google Fonts |
| **Spectral + Inter** | Editorial-modern, slightly tech | Spectral 400/600; Inter 400/500/600 | Modern publications, hybrid editorial-tech products | Less recognisable; emerging | Google's editorial sites in places | Google Fonts |

## Display + Sans (premium marketing)

When the hero needs to shout. The body retains restraint.

| Pairing | Mood | Recommended weights | When to use | Anti-pattern | Exemplar | Source |
|---|---|---|---|---|---|---|
| **Bricolage Grotesque + Inter** | Modern-editorial, sharp | Bricolage 400/700/900 (variable); Inter 400/500 | Marketing pages wanting bold modern grotesque | Variable axis settings can read as gimmicky | Vercel marketing in places, several startup sites | Google Fonts |
| **Migra + Inter** | Editorial-modern, premium display | Migra 400/700; Inter 400/500/600 | Premium consumer, fashion-adjacent SaaS | Commercial; alternatives less premium | several premium consumer brands | Pangram Pangram (commercial, https://pangrampangram.com). Free alternative: Fraunces 144 weight |
| **Alpino + Inter** | Modern-display, geometric | Alpino 400/700/800; Inter 400/500 | Modern startup marketing, tech-adjacent consumer | Commercial; budget barrier | several modern brand identities | Pangram Pangram (commercial). Free alternative: Outfit display weight |
| **Editorial New + Inter** | Premium display-serif, editorial | Editorial New 400/700; Inter 400/500 | Premium consumer, magazine-style products | Commercial; alternatives less premium | several premium consumer brands | Pangram Pangram (commercial). Free alternative: Fraunces 9pt optical size |

## Modern grotesque (futurist, technical)

When the design wants to read as 'made for screens, not pages'.

| Pairing | Mood | Recommended weights | When to use | Anti-pattern | Exemplar | Source |
|---|---|---|---|---|---|---|
| **Space Grotesk + Space Mono** | Futurist, sharp, slightly playful | Space Grotesk 400/500/700; Space Mono 400/700 | Modern dev tools, design tools, futurist marketing | Recognisable; reads as 'startup-marketing' | Linear marketing pages, several design tools | Google Fonts |
| **Karla + Karla** | Modern grotesque, single-typeface | 400/500/700/800 | When wanting modern utility with one font | Less distinctive than Inter | several startup marketing sites | Google Fonts |
| **Public Sans + Public Sans** | Government-modern, neutral | 400/500/600/700 | Civic tech, government products, plain-language documentation | Reads slightly bureaucratic | US Web Design System, several government sites | Google Fonts (US Web Design System) |
| **Geist Mono + Geist Mono** | Mono-only, terminal-aesthetic | Geist Mono 400/500/700 | Terminal-style products, code-as-brand | Mono at body sizes is harder to read | several Vercel-adjacent dev tools | Vercel (free) |

## Serif + Serif (editorial premium)

For publications where typography is the brand.

| Pairing | Mood | Recommended weights | When to use | Anti-pattern | Exemplar | Source |
|---|---|---|---|---|---|---|
| **Fraunces + Fraunces** | Editorial, warm, single family | Fraunces 144 display + 9pt body (variable optical sizing) | Long-form publications, premium editorial SaaS | Body settings need explicit optical sizing | several premium publications | Google Fonts |
| **PT Serif + PT Serif** | Classic editorial, accessible | 400/700 | Government publications, accessible long-form, literary sites | Less distinctive than newer alternatives | Russian government sites, several accessible-first publications | Google Fonts |
| **Source Serif + Source Serif** | Editorial, considered, technical-friendly | 400/600/700 | Knowledge bases, technical books, scholarly journals | Less personality than Fraunces | several knowledge bases | Google Fonts |

## Casual / hand-drawn (specific use cases only)

For products where personality is the brand.

| Pairing | Mood | Recommended weights | When to use | Anti-pattern | Exemplar | Source |
|---|---|---|---|---|---|---|
| **Caveat + Inter** | Casual, hand-drawn, friendly | Caveat 400/700; Inter 400/500 | Notes apps, casual collaboration tools, kids' products | Caveat at body sizes is unreadable; restrict to short labels | several note-taking and collaboration tools | Google Fonts |
| **Patrick Hand + DM Sans** | Hand-drawn, friendly, kids-adjacent | Patrick Hand 400; DM Sans 400/500/700 | Kids' products, education, casual tools | Patrick Hand at body sizes is exhausting | several kids' education products | Google Fonts |

## Pairing recommendations by industry

| Industry | Recommended pairing | Backup |
|---|---|---|
| Modern SaaS (default) | Inter + JetBrains Mono | Geist + Geist Mono |
| Developer tools | Geist + Geist Mono | Inter + JetBrains Mono |
| Editorial / publishing | Fraunces + Manrope | Source Serif + Source Sans |
| Premium consumer | Recoleta + Inter (or free: Fraunces + Inter) | DM Serif Display + DM Sans |
| Marketing site (any SaaS) | Bricolage Grotesque + Inter | Inter + Inter (if budget for one) |
| Fintech | Inter + Inter | IBM Plex Sans + IBM Plex Mono |
| Healthcare (patient) | DM Sans + DM Sans | Manrope + Manrope |
| Healthcare (clinical) | Inter + JetBrains Mono | IBM Plex Sans + IBM Plex Mono |
| E-commerce DTC fashion | Cormorant Garamond + Inter | Fraunces + Manrope |
| Code editor | Geist Mono + Geist | Berkeley Mono + Inter |
| Long-form blog | Lora + Inter | Fraunces + Inter |
| Government / civic | Public Sans + Public Sans | Inter + Inter |
| Kids / education | Patrick Hand + DM Sans (display only) | Caveat + Inter (display only) |

## Picking a pairing

A few decision shortcuts:

- **Don't know? Default to Inter + JetBrains Mono.** It's the safe choice; if the design needs more personality later, swap the heading typeface and keep the body.
- **The brand has personality.** Pick from Display + Sans, Serif + Sans, or one of the casual/hand-drawn pairings.
- **The product is for developers.** Lean toward Geist or IBM Plex; keep mono visible.
- **The brand budget supports commercial fonts.** Söhne, Recoleta, GT Sectra, Migra, Alpino, Editorial New are top-tier choices that meaningfully shift the design.
- **The brand budget is zero.** Stay in Google Fonts. Inter, Geist, Fraunces, Söhne alternatives (Mona Sans), and IBM Plex cover most needs.

When the agent isn't sure, surface 2 to 3 candidate pairings. *'I think Inter + JetBrains Mono (default modern), Fraunces + Manrope (more editorial), or Geist + Geist Mono (more dev-tool). Which feels closer?'*

## Loading fonts (performance-aware)

Per [`performance-design.md`](performance-design.md) § Font loading:

- Preload critical fonts: `<link rel="preload" as="font" type="font/woff2" crossorigin>`.
- Use `font-display: swap` for non-critical.
- Subset to the actual character range (latin or latin-ext for English; smaller subsets save 30%+).
- Self-host where possible. Google Fonts' CSS file is render-blocking by default.

A typical project ships 2 to 4 weights total per typeface (e.g., Inter 400, 500, 600, 700). Variable fonts collapse this to one file.

## Pencil expression

A chosen pairing maps to the project's `tokens.md` type scale and the document's `themes.font` axis. Example:

1. Agent picks 'Inter + JetBrains Mono' from the SaaS section.
2. Agent calls `set_variables` to populate the project's type tokens:
   - `$fontDisplay`: 'Inter', sans-serif
   - `$fontBody`: 'Inter', sans-serif
   - `$fontMono`: 'JetBrains Mono', monospace
   - `$fontWeightRegular`: 400
   - `$fontWeightMedium`: 500
   - `$fontWeightSemiBold`: 600
   - `$fontWeightBold`: 700
3. Agent records the chosen pairing in `assets/design-system/visual-style.md`: *'Type pairing: Inter + JetBrains Mono. Source: Google Fonts. Weights: 400, 500, 600, 700 for Inter; 400, 500 for JetBrains Mono.'*
4. Agent records the type scale in `assets/design-system/tokens.md`: text size scale with line-heights and weight defaults per scale step.

For the worked example, see [`example-style-selection.md`](../assets/examples/example-style-selection.md) (Phase 4).

## Anti-patterns

- **Hard-coding font names from this catalogue into `batch_design`.** This file is a menu of recipes, not a source of values. Font names belong in `assets/design-system/tokens.md` and the `.pen` file's `variables` (as `$fontBody`, `$fontMono`, `$fontDisplay`). Designs reference tokens.
- **Three or more typefaces in one design.** A serif heading + sans body + display accent + mono code is on the edge. A fifth typeface tips into chaos. Stick to a maximum of three (heading + body + mono).
- **Display fonts at body sizes.** Display fonts have wide x-heights, dramatic curves, and tight defaults. They're exhausting to read at 16px. Restrict display fonts to headings.
- **Mono fonts at body sizes.** Same problem in the opposite direction. Mono is slow to read. Restrict to code blocks, IDs, and tabular numerics.
- **Inter on every site.** Inter is the safest choice and the AI default. If the design needs personality, swap the heading font (keep Inter for body) or swap the whole pairing.
- **Commercial fonts shipped without licensing.** Söhne, Recoleta, GT Sectra, Migra are commercial. Verify the licence before shipping; or use the suggested free alternatives.
- **Variable font axis settings as decoration.** Using Bricolage's optical-size axis just because it's available reads as gimmicky. The axis settings should serve a purpose (display sizes get larger optical-size; body gets the default).

## Sources

- **Google Fonts**: https://fonts.google.com. Most pairings in this catalogue use Google Fonts (free, OFL-licensed). Inter, Geist, Fraunces, Source Serif/Sans, Manrope, DM Sans/Serif, Plus Jakarta Sans, Outfit, Sora, Bricolage Grotesque, Space Grotesk/Mono, Karla, Public Sans, Caveat, Patrick Hand, Lora, Spectral, Crimson Pro, Cormorant Garamond, Playfair Display, IBM Plex Sans/Mono, Mona Sans/Hubot Sans (via GitHub).
- **Vercel Geist + Geist Mono**: https://vercel.com/font (free, MIT-licensed).
- **GitHub Mona Sans + Hubot Sans**: https://github.com/mona-sans (free, OFL-licensed).
- **Klim Type Foundry**: https://klim.co.nz. Söhne, Söhne Mono (commercial; the canonical premium grotesque pairing).
- **Pangram Pangram Foundry**: https://pangrampangram.com. Migra, Alpino, Editorial New (commercial; modern display fonts).
- **Grilli Type**: https://grillitype.com. GT Sectra, GT America (commercial; premium editorial and grotesque).
- **DJR**: https://djr.com. Recoleta (commercial; warm display serif).
- **Berkeley Graphics**: https://berkeleygraphics.com/typefaces/berkeley-mono. Berkeley Mono (commercial; modern monospace).
- **Real product exemplars (accessed 2025/2026)**: Linear, Vercel, Stripe, Notion, GitHub, Substack, Pitch, ChatGPT/OpenAI, Cosmos.
- **Refactoring UI** (Adam Wathan, Steve Schoger): typography hierarchy and pairing principles underlying the catalogue.
- **Apple Human Interface Guidelines: Typography**: optical sizing, weight contrast, dynamic type principles applied to the variable-font recommendations.

## See also

- [`style-catalogue.md`](style-catalogue.md): the named UI styles that constrain font choice.
- [`colour-palettes.md`](colour-palettes.md): palettes to pair with the chosen typography.
- [`industry-patterns.md`](industry-patterns.md): per-industry typography recommendations.
- [`performance-design.md`](performance-design.md) § Font loading: preload, subset, self-host guidance.
- [`accessibility.md`](accessibility.md): dynamic type, font-size baselines, readability.
- [`assets/design-system/tokens.md`](../assets/design-system/tokens.md): where the chosen pairing gets recorded as project type tokens.
- [`example-style-selection.md`](../assets/examples/example-style-selection.md): worked sequence of catalogue → MCP variable population → starter components (Phase 4).
