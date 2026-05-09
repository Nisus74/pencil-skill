# Visual style

The project's chosen style identity. The agent reads this file at the start of every design pass to constrain output to the chosen direction. Without it, the agent picks a style each time and the product loses coherence between sessions.

This file is a single project commitment: one style, one palette recipe, one font pairing. It complements `tokens.md` (which holds the actual colour and type tokens) and `visual-style.md` is the *narrative* of why those tokens are what they are.

## Chosen style

**Style:** `<name from references/style-catalogue.md>` (e.g. *Swiss / International*, *Editorial*, *Bento*, *Brutalist*, *Dark-mode-first*).

**Style family:** `<modernist | expressive | technical | retro | atmospheric | hand-crafted>`.

**Why this style:** `<one or two sentences linking the style to the audience and brand>`.

**Sample component cues** (lift these to constrain every design):

- `<e.g. flat backgrounds, single-line dividers, generous whitespace>`
- `<e.g. tight letter-spacing on headings (-0.02em)>`
- `<e.g. layered shadows (ambient + direct, two layers minimum)>`
- `<e.g. one accent only; never multiple competing hues>`

**Anti-patterns specific to this style** (from style-catalogue):

- `<e.g. so restrained it reads as cold; counter with one warm accent>`
- `<e.g. so minimal the user can't find affordances; chrome stays obvious>`

## Chosen palette

**Palette recipe:** `<name from references/colour-palettes.md>` (e.g. *Indigo Calm*, *Cursor Dark*, *Patient Warm Teal*).

**Source:** `<which scale system; e.g. Tailwind v4 (Indigo + Slate scales), or Radix Mauve + Iris>`.

**Why this palette:** `<one sentence linking the palette to the chosen style and the audience>`.

**Mode coverage:** `<light only | dark only | both>`.

**The actual hex values live in `tokens.md`** (`$accent`, `$bg`, `$surface`, `$textPrimary`, etc.). This file holds the recipe name and source so the next agent (or designer) knows where to look the values up if they need to extend the scale.

**APCA contrast verified:** `<yes | no; flag any pairs that fall below Lc 75 for body text>`.

**Colour-blind safety:** `<verified Stark / Sim Daltonism / Chrome DevTools | not yet verified>`. State coding pairs colour with `<shape | position | text label>` per `references/data-viz.md`.

## Chosen typography

**Font pairing recipe:** `<name from references/font-pairings.md>` (e.g. *Inter + JetBrains Mono*, *Fraunces + Manrope*, *Geist + Geist Mono*).

**Source:** `<Google Fonts | Vercel Geist | GitHub Mona Sans | commercial foundry name>`.

**Weights to ship:** `<e.g. Inter 400, 500, 600, 700; JetBrains Mono 400, 500>`.

**The actual font tokens live in `tokens.md`** (`$fontDisplay`, `$fontBody`, `$fontMono`, plus weight scale). This file holds the pairing name and source.

**Why this pairing:** `<one sentence linking the typography to the chosen style and the audience>`.

## Deviations from the catalogue

Where the project's choices break from the catalogue defaults, document the deviation and the reason here. The next agent reads this section to understand what's intentional vs accidental.

- `<e.g. Used Indigo 700 instead of Indigo 600 as the primary accent; the brand colour was already darker and the lighter step looked washed-out next to existing assets>`
- `<e.g. Kept the Söhne-style heading even though we're using Inter for body; Söhne is licenced via Klim and the brand has the budget>`
- `<e.g. Three accents instead of one (brand requires it); compensated by tightening neutral usage>`

If there are no deviations, say so explicitly: *'No deviations from the catalogue.'*

## Style enforcement (for the agent)

When designing a new screen, the agent:

1. Reads this file first to recall the chosen style + palette + fonts.
2. Constrains every design choice to those commitments. A Brutalist project doesn't get glassmorphic modals; a Swiss project doesn't get Memphis-style dividers.
3. References the tokens (`$accent`, `$fontBody`, etc.) via `batch_design`. Never types literal hex or font names directly.
4. Cross-references `references/iteration-patterns.md` § Failure mode: too generic if a design feels off; the rescue may be to commit harder to the chosen style rather than swap it.

If the user asks for a screen that's stylistically incompatible (e.g. a brutalist hero on a Swiss / International project), the agent surfaces the conflict: *'This screen leans brutalist, but the project's chosen style is Swiss / International. Should we (a) keep this screen consistent with the project, (b) make a one-off exception and document it as a deviation, or (c) change the project-wide style?'*

## Updates to this file

When the project's style changes, update this file *first*, then update `tokens.md` to match, then re-run designs against the new style.

History (optional; useful when looking back at why a style shifted):

- `<YYYY-MM-DD>` Initial commitment: `<style + palette + fonts>`.
- `<YYYY-MM-DD>` `<deviation noted, e.g. switched accent to Indigo 700>`.
- `<YYYY-MM-DD>` `<significant change, e.g. moved from Editorial to Swiss / International for v2>`.

## See also

- `references/style-catalogue.md`: the menu this project picked from.
- `references/colour-palettes.md`: the palette recipe menu.
- `references/font-pairings.md`: the typography pairing menu.
- `tokens.md`: the actual colour, type, and spacing tokens (the values).
- `references/iteration-patterns.md`: the rescues when a design isn't landing the chosen style.
- `references/industry-patterns.md`: the per-industry conventions that shaped this project's style.
