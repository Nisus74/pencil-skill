# Components

Catalog of reusable components. The agent reads this when deciding what to instantiate. **Always reach for an existing component before inventing one.**

## How to use this file

The "Library id" column is the `id` of the `reusable: true` node in your `.lib.pen`. You instantiate it with:

```
btn=I("parent", { type: "ref", ref: "ButtonPrimary", descendants: { label: { text: "Sign in" } } })
```

If the "Library id" cell is blank, the component doesn't exist in the library yet — add it before you start using it elsewhere, or update this row to point at whatever name you used.

## Buttons & actions

| Component | What it is | When to use | Library id |
|-----------|-----------|-------------|------------|
| Primary button | Filled, brand-colored | Single primary action per view | `ButtonPrimary` |
| Secondary button | Outlined | Secondary action; pairs with a Primary | `ButtonSecondary` |
| Tertiary / Ghost | Text-only with subtle hover | Low-priority actions inside dense UI | `ButtonGhost` |
| Icon button | Icon-only, square | Toolbars, dense controls | `IconButton` |
| Link / inline link | Underlined or accent-colored text | Inline navigation, "forgot password?" style | `LinkText` |
| Destructive button | Filled, danger color | Delete, sign out, irreversible actions | `ButtonDestructive` |

## Inputs & forms

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
| Modal | Centered overlay | Focused tasks that interrupt | `Modal` |
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

## When the right component doesn't exist

Three options, in order:

1. **Compose from existing components.** Often a "card with a button and a tag" doesn't need a new component — just instantiate the three.
2. **Ask before inventing.** If you're about to build something from primitives that smells like a missing component, surface it: *"This pattern looks reusable — should I add a `<name>` to your `.lib.pen`?"* The user decides.
3. **Build, then promote.** If asked to build something one-off and it's clearly going to be reused, build it as a regular frame for now and flag it. Don't preemptively make it `reusable: true` — that's a library decision the user owns.

## Naming convention

Pascal case for component ids: `ButtonPrimary`, not `button-primary` or `button_primary`. This matches the convention most code-side component libraries use, so design and code stay in lockstep.

## Required state coverage (for every component)

Every reusable component must declare the following states before it ships into the library. Skipping focus state in particular is the #1 way to ship inaccessible UI by default.

| State | When to draw it |
|-------|-----------------|
| **Default** | Always. The resting state. |
| **Hover** | Any pointer-aware target (buttons, links, cards-as-targets). Even subtle change is fine — color shift, slight elevation. |
| **Focus** | EVERY interactive element. 2px outline using `$focusRing`. Skipping this fails WCAG. |
| **Active / Pressed** | Buttons, toggles, anything that registers a tap/click. |
| **Disabled** | Anything that can be inert. Typically muted color and cursor: `not-allowed`. |
| **Loading** | Buttons that submit, anything that fetches. Replace label with spinner, keep width. |
| **Error / Invalid** | Form inputs. Border color `$danger`, paired with an icon and a message — never red alone. |

For inputs, also draw the **filled** state (with placeholder content) and the **focused-with-error** edge case.

## Accessibility roles

When you create a component, name it after its role, not its appearance. The downstream code generator and screen readers both consume the name. Examples:

- ✅ `PrimaryAction`, `SecondaryAction`, `DestructiveAction`, `IconButton`
- ❌ `BlueButton`, `BigButton`, `RoundedButton`
