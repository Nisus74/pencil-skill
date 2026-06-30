# Search

How search behaves in this product. The agent reads this file when designing search inputs, results pages, suggestion dropdowns, and command palettes. Without it, every search surface gets reinvented. The project ends up with three different debounce values across surfaces, plus a command palette that doesn't agree with the header search.

This file is a single project commitment: one search shape, one entry point in the chrome, plus an agreed set of keyboard shortcuts and URL conventions.

## Search shape

The project commits to: `<instant search | submit-driven search | hybrid (instant suggestions + submit results page)>`.

`hybrid` is the modern default for products with both known-item lookups and exploratory browsing. Pick `instant` only for small catalogues (under ~10k items) where every result fits in a dropdown without pagination. If results need server-side filtering or sorting from the first interaction, go submit-driven.

## Entry point

Where search lives in the chrome:

- `<header search bar | command palette (⌘+K) | dedicated search page | inline filters per surface>`

For a command palette pattern, the keyboard shortcut is `<⌘+K | Ctrl+K | / | other>`. Document the same shortcut in `accessibility.md` § Keyboard shortcuts so it doesn't drift.

## Instant search

If the project ships instant search:

- **Debounce:** `<150ms | 200ms | 300ms>`. Longer windows reduce server load at the cost of perceived snappiness. 200ms is a sensible middle for most products.
- **Minimum query length:** `<1 | 2 | 3 characters>` before the request fires. Single-character search is rarely worth the cost.
- **Results panel placement:** dropdown below the input, side panel, or full-screen takeover on mobile.
- **Result count:** `<top 5 | top 10 | top 20>` per category. Pagination only on the full results page.
- **Loading indicator:** subtle spinner inside the search input while the request is in flight. Don't block the rest of the page or shift layout.
- **Empty results state:** see `empty-states.md` § Search results.

## Submit-driven search

If the project ships submit-driven search:

- **Trigger:** Enter key, search button click, or both.
- **Results page URL:** `/search?q=<query>&filter=<filter>`. Query and filters live in the URL so the page survives refresh and stays shareable.
- **Loading state:** skeleton with placeholder result rows while fetching. No spinner-only states.
- **Result count:** display the total above results: *'About 1,234 results'*.

## Suggestions vs results

Suggestions are what the system predicts the user means as they type, shown instantly in a dropdown. Results show what the system actually found after a submission, with broader matching and pagination. The two can coexist:

- Suggestions appear in the dropdown while typing.
- Pressing Enter takes the user to the full results page with broader matches.

For this project's specific behaviour: `<suggestions only | results only | both>`.

## Suggestion categories

When the project shows suggestions, group them by category. Common groups:

- **Recent searches:** the user's last `<5 | 10>` searches.
- **Suggested searches:** product-driven suggestions based on context.
- **Top results:** top 3-5 actual matches across all entities.
- **Entity-specific:** Projects, People, Documents, Settings, Help articles. Each as a labelled group.

Customise per project. Order matters; put the most likely category first. Don't show empty groups.

## Filters

If the project's search supports filters:

- Filter chips sit above or below the search input.
- Active filters are reflected in the URL alongside the query.
- A clear-all affordance is always visible when any filter is active.
- Filter combinations use AND by default. OR is explicit (a chip group with an *'Any of'* label).

## Keyboard shortcuts

- `<⌘+K | Ctrl+K | / | other>`: open search.
- `↑ ↓`: navigate suggestions or results.
- `Enter`: submit, or open the selected suggestion.
- `Esc`: close search.
- `⌘+Enter` (command palette): open the selected result in a new tab or window.

Document these in `accessibility.md` § Keyboard shortcuts so the project has one source of truth.

## URL state

Search query, active filters, and pagination belong in the URL. That way:

- Refresh restores the same search.
- The user can share or bookmark a search.
- Browser back and forward navigate through search states.

What doesn't belong in the URL:

- Which result the user has hovered.
- Whether the suggestion panel is open.
- The selected suggestion before navigation happens.

## Empty results

When search returns nothing, the empty state should:

- Name the query: *'No results for ''<query>'''*.
- Suggest a refinement: *'Try a broader search or check the spelling.'*
- Offer a fallback action: *'Browse all'*, *'Contact support'*.

See `empty-states.md` § Search results for the full copy template.

## Performance

- First paint of the search panel under 100ms after the trigger.
- Debounced query fires after the debounce window (150-300ms).
- Each request carries an idempotency token. Cancel in-flight requests when the user types more so stale results can't overwrite fresh ones.

## Accessibility

- Search input has an accessible label (`Search` or contextual: `Search projects`).
- Suggestion list announces its count to screen readers via `aria-live='polite'`.
- The selected suggestion is announced as the user arrows through.
- A submit button is keyboard-accessible if it's visible. Enter always submits regardless.

## See also

- `patterns.md`: where search lives within the page lockup (header, sidebar, modal).
- `accessibility.md`: keyboard shortcut documentation, screen reader announcement patterns.
- `empty-states.md`: search result empty states.
- `voice.md`: search-related microcopy (placeholder text, empty results, suggestion category labels).
- `references/flows.md` (in the pencil-design skill): § Search flows (instant vs submit, results vs suggestions, URL state).
- `references/layout-patterns.md` (in the pencil-design skill): § Settings pages (search-driven variant) and dashboard layouts.
- `references/microcopy.md` (in the pencil-design skill): § Empty state copy.
