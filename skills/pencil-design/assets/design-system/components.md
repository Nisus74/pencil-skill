# Components

Catalog of reusable components. The agent reads this when deciding what to instantiate. **Always reach for an existing component before inventing one.**

## How to use this file

The "Library id" column is the `id` of the `reusable: true` node in your `.lib.pen`. You instantiate it with:

```
btn=I("parent", { type: "ref", ref: "ButtonPrimary", descendants: { label: { text: "Sign in" } } })
```

If the "Library id" cell is blank, the component doesn't exist in the library yet, add it before you start using it elsewhere, or update this row to point at whatever name you used.

## Buttons and actions

| Component | What it is | When to use | Library id |
|-----------|-----------|-------------|------------|
| Primary button | Filled, brand-coloured | Single primary action per view | `ButtonPrimary` |
| Secondary button | Outlined | Secondary action; pairs with a Primary | `ButtonSecondary` |
| Tertiary / Ghost | Text-only with subtle hover | Low-priority actions inside dense UI | `ButtonGhost` |
| Icon button | Icon-only, square | Toolbars, dense controls | `IconButton` |
| Link / inline link | Underlined or accent-coloured text | Inline navigation, "forgot password?" style | `LinkText` |
| Destructive button | Filled, danger colour | Delete, sign out, irreversible actions | `ButtonDestructive` |

## Inputs and forms

| Component | What it is | When to use | Library id |
|-----------|-----------|-------------|------------|
| Input | Single-line text input with label | Default for any form field | `Input` |
| Textarea | Multi-line input | Comments, longer freeform text | `Textarea` |
| Select | Dropdown | One-of-N choices, > 4 options | `Select` |
| Checkbox | Boolean toggle | Standalone yes/no, multi-select lists | `Checkbox` |
| Radio group | Mutually-exclusive choices | One-of-N, ≤ 4 options | `RadioGroup` |
| Toggle / Switch | On-off | Settings; immediate side-effect | `Toggle` |
| Slider | Range / numeric | Continuous values | `Slider` |

## Surfaces

| Component | What it is | When to use | Library id |
|-----------|-----------|-------------|------------|
| Card | Padded, rounded surface | Grouping related content | `Card` |
| Modal | Centred overlay | Focused tasks that interrupt | `Modal` |
| Drawer / Sheet | Edge-anchored panel | Longer-form side tasks | `Drawer` |
| Popover | Small floating panel | Inline help, contextual actions | `Popover` |
| Tooltip | Tiny hover hint | Single-sentence explanations | `Tooltip` |

## Feedback

| Component | What it is | When to use | Library id |
|-----------|-----------|-------------|------------|
| Toast | Transient notification | Confirm an async action | `Toast` |
| Alert / Banner | Persistent notification | Important state at the top of a region | `Alert` |
| Empty state | Illustration + copy + CTA | When a list / view has nothing in it | `EmptyState` |
| Loading skeleton | Placeholder shape | While data is loading | `Skeleton` |

## Display

| Component | What it is | When to use | Library id |
|-----------|-----------|-------------|------------|
| Badge | Small status label | Counts, statuses, tags | `Badge` |
| Avatar | Circular user/identity image | Inline references to people | `Avatar` |
| Tag / Chip | Removable pill | Filter selections, multi-value inputs | `Tag` |

## Navigation

| Component | What it is | When to use | Library id |
|-----------|-----------|-------------|------------|
| Top nav | App-level navigation bar | App shell | `TopNav` |
| Side nav | Vertical primary nav | App shell with many sections | `SideNav` |
| Tabs | Switch between peer views | 2–6 sibling views | `Tabs` |
| Breadcrumb | Hierarchical trail | When users can be deep in a tree | `Breadcrumb` |

## Component variants by archetype

The same component reshapes meaningfully under different archetypes. The catalogue above defines *what* exists; the variants below define *how it looks* once you've committed to an archetype. See `assets/archetypes/` for the full archetype definitions.

### Button (Primary)

- **`saas-apps/b2b/analytics-dashboard`**: filled accent, rounded-rectangle (radius 6–10), sharp typography, often paired with a count (*"Export 248 events"*) using monospace numerals.
- **`saas-apps/b2b/modern-pro-tool`** (Linear): filled accent, rounded rectangle (radius 6–8), keyboard-shortcut chip embedded on the right edge of the button (e.g. `C` in a darker mono pill).
- **`marketing-websites/conversion-focused-saas`**: filled brand accent on a hero, slightly larger (height 48), no gradient, no decorative shadow. CTA copy is confident (*"Try the new model"*) not generic (*"Get started"*).

**What generic looks like:** violet-to-blue gradient fill, soft drop shadow, label *"Get Started"* in title case, slight scale-up on hover with a glow.

### Card

- **`saas-apps/b2b/analytics-dashboard`**: hairline border (1px `$border`), no shadow, corner radius 6–10, three-level surface hierarchy (`$bg` > `$surface` > `$surfaceMuted`).
- **`saas-apps/b2b/modern-pro-tool`**: same. Hairline border, no shadow. Cards rarely appear at all on the home view; dense list rows replace them.
- **`marketing-websites/editorial-storytelling`**: cards almost don't exist. Content sits directly on the page background, separated by whitespace and section transitions, not chrome.

**What generic looks like:** medium soft shadow, corner radius 12–16, white background even in dark mode, hover state lifts the card with a stronger shadow.

### Sidebar / SideNav

- **`saas-apps/b2b/modern-pro-tool`** (Linear): pale-grey background (`$surfaceMuted`), section headers in sentence-case lowercase with a small chevron (*"workspace ▼"*, *"your teams ▼"*), active item is `$surfaceMuted` filled background (one shade darker), 6–8px vertical padding per item, dense.
- **`saas-apps/b2b/analytics-dashboard`**: white sidebar (`$surface`), 2px left accent bar marks the active item (not a coloured pill), hairline right border separating from main content.
- **`saas-apps/b2c/consumer-media`** (when populated): dark sidebar by default, larger cover-art tiles, less hierarchical text-first nav.

**What generic looks like:** sidebar with a violet gradient logo, six nav items each with a Lucide icon and an active state that's a soft-violet pill, no section grouping, equally-spaced 12px padding throughout.

### Empty state

- **`saas-apps/b2b/analytics-dashboard`**: skip the illustration, single confident headline naming what's missing and the next action (*"No events tracked yet. Send your first one →"*).
- **`saas-apps/b2b/modern-pro-tool`**: four small abstract icons in a 2×2 cluster above the heading, bold title, descriptive paragraph, two buttons (filled accent primary + secondary outline with subtle border).

**What generic looks like:** big illustrated mascot scene of someone holding an empty box, title *"It's quiet here!"*, three buttons offering Import / Create / Explore Demo, decorative confetti shapes around the edges.

### Status pill / Badge

- **`saas-apps/b2b/modern-pro-tool`**: small filled circle of status colour beside short text. Compact. No card background. Inline with title.
- **`saas-apps/b2b/analytics-dashboard`**: same minimalist treatment. Plan badges sometimes become single-letter monogram chips (P / F / T) instead of word badges.

**What generic looks like:** rounded rectangle with a strong colour fill (red / yellow / green), text in white, small drop shadow, sometimes paired with an icon.

### Avatar

- All app archetypes: circular, `$accentSoft` background, initial in `$accent` text. Small (24–32px) inline; medium (40–48px) in user lists; large (80px+) on profile pages.

**What generic looks like:** circular gradient placeholder, generic person silhouette icon, *"JD"* (John Doe) initials.

## When the right component doesn't exist

Three options, in order:

1. **Compose from existing components.** Often a "card with a button and a tag" doesn't need a new component, just instantiate the three.
2. **Ask before inventing.** If you're about to build something from primitives that smells like a missing component, surface it: *"This pattern looks reusable, should I add a `<name>` to your `.lib.pen`?"* The user decides.
3. **Build, then promote.** If asked to build something one-off and it's clearly going to be reused, build it as a regular frame for now and flag it. Don't preemptively make it `reusable: true`, that's a library decision the user owns.

## Naming convention

PascalCase for component ids: `ButtonPrimary`, not `button-primary` or `button_primary`. This matches the convention most code-side component libraries use, so design and code stay in lockstep.

## Required state coverage (for every component)

Every reusable component must declare the following states before it ships into the library. Skipping focus state in particular is the #1 way to ship inaccessible UI by default.

| State | When to draw it |
|-------|-----------------|
| **Default** | Always. The resting state. |
| **Hover** | Any pointer-aware target (buttons, links, cards-as-targets). Even subtle change is fine, colour shift, slight elevation. |
| **Focus** | EVERY interactive element. 2px outline using `$focusRing`. Skipping this fails WCAG. |
| **Active / Pressed** | Buttons, toggles, anything that registers a tap/click. |
| **Disabled** | Anything that can be inert. Typically muted colour and cursor: `not-allowed`. |
| **Loading** | Buttons that submit, anything that fetches. Replace label with spinner, keep width. |
| **Error / Invalid** | Form inputs. Border colour `$danger`, paired with an icon and a message, never red alone. |

For inputs, also draw the **filled** state (with placeholder content) and the **focused-with-error** edge case.

## Accessibility roles

When you create a component, name it after its role, not its appearance. The downstream code generator and screen readers both consume the name. Examples:

- ✅ `PrimaryAction`, `SecondaryAction`, `DestructiveAction`, `IconButton`
- ❌ `BlueButton`, `BigButton`, `RoundedButton`
