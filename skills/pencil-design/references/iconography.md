# Iconography

Icons are the smallest typography in the product. They sit beside labels, inside buttons, in chrome, in form fields, and they read at glance speeds. Pick the family once, commit to its stroke weight and corner language, and treat every icon decision as a typographic one.

**What this file owns:** stroke weight per context, size relative to text, icon-only versus paired-with-text decisions, semantic icon conventions, decorative-versus-meaningful distinction, family consistency, custom-icon discipline, and the Pencil node types that carry icons into `.pen`.

**What this file does NOT own:** the project's chosen icon family (Phosphor, Lucide, Material Symbols, Heroicons, Tabler, SF Symbols). That commitment lives in [`assets/design-system/iconography.md`](../assets/design-system/iconography.md). Component-internal icon placement (button-internal, input-internal, list-row trailing) is in [`assets/design-system/components.md`](../assets/design-system/components.md). ARIA patterns for icon accessibility are detailed in [`accessibility.md`](accessibility.md). Optical sizing relative to text is cross-referenced in [`visual-hierarchy.md`](visual-hierarchy.md).

## When to load this file

- The design includes any icon: navigation, button, status, inline marker, empty state, illustration.
- The user names *icon*, *icon button*, *iconography*, *Phosphor*, *Lucide*, *Material Symbols*, *Heroicons*, *Tabler*, *SF Symbols*, *icon family*.
- You're auditing a screen that mixes icon families (a Phosphor calendar next to a Lucide chevron) and need to normalise.
- You're picking the icon library for a new project before any screens ship.

## Stroke weight per context

Stroke weight is the most over-looked typographic decision in icon work. The same icon at 1px, 1.5px, and 2px reads as three different products.

- **1.5px is the standard** for body-adjacent icons. List-row icons, inline status markers, navigation-rail icons, settings-row icons. Lucide ships at 2px by default, Phosphor at 1.5px (the "regular" weight); both are tunable. Pick one and hold it across the product.
- **2px for emphasis.** Button-internal icons inside primary buttons, chips with leading icons, prominent CTAs. The heavier stroke matches the optical weight of bold labels at 14–16px.
- **1px for hairline.** Tertiary inline icons (a lock next to a private-page title, a small chevron in a breadcrumb), and small chrome at 12–14px. Phosphor's "thin" weight or Lucide at custom 1px.
- **Don't deviate within a screen.** A 1.5px chevron next to a 2px arrow looks like the assets came from two libraries. If a single icon needs more weight for hierarchy, scale it up rather than re-stroke it.

When the family doesn't ship multiple weights (Heroicons ships outline at 1.5px and solid as filled, no stroke variants), you don't tune stroke; you switch between outline and filled to express weight.

## Size relative to text

Inline icons take their size from the text they sit beside. The eye reads a misaligned icon as a typo.

- **Cap-height matching for inline icons.** An icon inside a paragraph or beside a heading should match the cap-height of the surrounding text. For 16px body text (~11px cap-height), a 14px icon optically aligns; for a 24px heading, an 18–20px icon. Matching the line-height instead overshoots and produces an icon that floats too tall. Most icon libraries are designed on a 24px grid with built-in padding, so the rendered glyph occupies roughly 80% of the box; account for that when matching cap-height.
- **Line-height matching for standalone icons in chrome.** Sidebar nav icons, header-rail icons, FAB icons. The 24px icon in a 40px hit-target reads as well-proportioned because the surrounding line-height and padding carry the rhythm.
- **Common sizes.** 16px for inline icons inside body text, 20px for form-field chrome (input leading/trailing icons, dropdown carets), 24px for button chrome and primary navigation, 32px and up for empty-state illustrations and feature tiles.
- **Round to the icon grid.** Lucide and Phosphor are designed on a 24px grid; rendering at 17px or 23px produces sub-pixel artefacts on non-Retina displays. Stick to 12, 14, 16, 20, 24, 28, 32, 40, 48.

For the broader visual-hierarchy frame around icon-text balance, see [`visual-hierarchy.md`](visual-hierarchy.md) § Optical centre vs geometric centre.

## Icon-only versus paired with text

The user shouldn't have to guess what an icon means on first encounter. Pair icons with text whenever the action isn't universally understood.

- **Icon-only is fine for universally-recognised actions.** Close (✕), search (magnifier), menu (hamburger), back (chevron-left), settings (gear), trash (bin), share (arrow-up-from-square). The user has seen these in a hundred apps; they don't need a label.
- **Icon-only requires `aria-label` AND tooltip.** The `aria-label` is for screen-reader users; the tooltip is for sighted users who hover. Both. See [`accessibility.md`](accessibility.md) § Icon buttons for the exact pattern.
- **Pair with text for unfamiliar actions.** "Archive", "Move to project", "Convert to recurring", "Snooze". These don't have a universal icon; the label is doing the work and the icon is decoration.
- **Paired layout: icon then label, 8px gap.** The icon precedes the label inside primary buttons; the spacing matches the optical weight of the text. For RTL locales, the icon flips to the right; the gap stays 8px. See [`accessibility.md`](accessibility.md) § RTL.

When a button is dense with icons (a toolbar of 8 actions), each icon still needs its own tooltip. Don't ship a toolbar that requires the user to click each icon to discover what it does.

## Semantic icon conventions

Users have learned what these icons mean. Don't deviate; you'll just confuse them.

| Concept | Icon | Notes |
|---|---|---|
| Warning | Triangle with exclamation | Phosphor `warning`, Lucide `triangle-alert`, Material `warning`. |
| Error | Circle with X (or filled circle with X) | Phosphor `x-circle`, Lucide `circle-x`. |
| Success | Circle with check | Phosphor `check-circle`, Lucide `circle-check`. |
| Info | Circle with i | Phosphor `info`, Lucide `info`. |
| Lock (security/private) | Closed padlock | Open padlock means "unlocked"; the open variant is rarely the right choice for a private indicator. |
| Time/scheduled | Clock | Use a clock face. An hourglass reads as "loading" and confuses the meaning. |
| Delete | Trash bin | Universally understood; never reach for an X for delete. X means "close". |
| Edit | Pencil | The pencil is the convention; a pen icon reads as "compose new", not "edit existing". |
| Settings | Gear (cog) | Sliders are also acceptable for simple preference panels. |
| Favourite | Star | Heart implies "like" or "love"; star implies bookmarking. Pick the right verb. |

If your design language is built on illustrations and the conventional semantic icons clash, build illustrated variants that still carry the convention shape. A square with rounded corners reading as "warning" because it's amber and triangular-ish doesn't earn the user's recognition.

## Decorative versus meaningful

Every icon is either decorative or meaningful, and the markup needs to declare which.

- **Decorative icons get `aria-hidden="true"`.** Icons paired with a visible text label are decorative; the label is doing the semantic work, and the icon would be announced redundantly otherwise. A button with a pencil icon and the label "Edit" should not announce "pencil edit" to screen-reader users.
- **Meaningful icons get an accessible name.** Icon-only buttons, status icons that aren't paired with text, decorative-looking icons that actually convey state. Use `aria-label` on the icon's parent (the button or link), or `aria-labelledby` pointing at a hidden text node.
- **Icon as part of a status pattern.** A red error icon beside a field error message is decorative (the message is the announcement); a red error icon at the top of a form summarising "3 errors" is meaningful (it carries the severity). Document which in the icon's `context` so the engineer wires the markup correctly.

The full ARIA-pattern catalogue lives in [`accessibility.md`](accessibility.md) § Icon buttons and § Decorative versus meaningful.

## Family consistency

Pick one icon library and stick with it. Mixing Phosphor with Lucide with Material in the same product reads as inconsistent at a glance.

- **Stroke weight differs.** Lucide ships at 2px by default; Phosphor regular ships at 1.5px; Heroicons outline ships at 1.5px. A Lucide chevron next to a Phosphor calendar shows two different stroke weights in the same row.
- **Corner radius differs.** Phosphor uses softer rounded terminals; Lucide is squarer; Material Symbols has its own optical-size system. The corner language reads as inconsistent even when the user can't articulate why.
- **Grid differs.** Lucide and Phosphor are both designed on 24px; Material Symbols uses a 20px or 24px optical-size axis; SF Symbols renders at a typographic baseline alignment. Mixing means you're constantly fighting alignment.
- **The exception is brand marks and logos.** A product logo, a partner logo, or a payment-network mark (Visa, Mastercard) isn't part of the icon family. Treat them as imagery rather than icons; they don't need to match the family's stroke weight.

If you inherit a codebase that mixes families, normalise to one before adding new screens. Don't ship a third family on top.

## Custom icons when needed

Sometimes the chosen library doesn't have what you need: a brand-specific category icon, a product mark, an illustrated empty-state graphic.

- **Match the optical weight of the family.** If you've committed to Lucide at 2px, your custom icons render at 2px stroke. If you've committed to Phosphor regular, render custom icons at 1.5px with rounded terminals.
- **Export at 24px base.** The standard for most icon systems. Render variants at 16px and 20px from the same source to avoid sub-pixel rounding.
- **Provide variants for hover/active states if the library does.** Phosphor ships six weights including duotone and fill; if your custom icons need to express the same states, design the fill variant alongside the outline.
- **Don't custom-illustrate semantic icons.** A custom warning triangle that doesn't read as the convention warning triangle is just confusing. Use the library's warning icon and reserve custom illustration work for brand-specific categories.

## Pencil expression

Pencil represents icons via two node types:

- **`icon_font`**: an icon from a font-based icon set (Lucide, Material Symbols, Phosphor, Feather). Prefer this for any standard-library icon. Properties: `name` (the icon's identifier in its family, e.g. `chevron-right`), `weight` (when the family supports multiple weights, e.g. Phosphor's `thin` / `light` / `regular` / `bold` / `fill` / `duotone`), `size` (in px). The chosen family is documented at the project level so the renderer resolves the name correctly.
- **`icon_image`**: an icon from a custom SVG or raster source. Reserve for brand marks, custom illustrations, and anything outside the chosen library.

Document the chosen library in the project's [`assets/design-system/iconography.md`](../assets/design-system/iconography.md) so every agent that touches the file picks from the same set. Include the family name, the default size, the default weight, and any size-to-weight rules ("16px renders thin; 20px and up renders regular").

In `.pen`, an inline status icon beside text typically reads:

```
{
  "type": "frame",
  "name": "Status_Saved",
  "context": "Inline status icon plus label. Icon is decorative; label is the announcement.",
  "children": [
    { "type": "icon_font", "name": "CheckIcon", "context": "Decorative. aria-hidden=true." },
    { "type": "text", "name": "StatusLabel", "text": "Saved" }
  ]
}
```

For an icon-only button, the icon's parent button frame carries the accessible name in its `name` (e.g. `IconButton_Close`) and the icon is decorative inside it. See [`accessibility.md`](accessibility.md) § Icon buttons.

## Anti-patterns

These read as icon-blind designs and should be fixed in passing:

- **Mixing icon families.** A Phosphor calendar beside a Lucide chevron in the same row.
- **Icon-only with no `aria-label` or tooltip.** The mystery-meat icon button. Sighted users guess; screen-reader users get nothing.
- **Using X for delete.** X means "close" or "dismiss". Trash means "delete". Don't blur them.
- **Pencil for "compose new".** Pencil is "edit existing"; use a plus or a paper-with-plus for compose new.
- **Custom-illustrated semantic icons that don't read as convention.** A bespoke warning-amber-square doesn't trigger recognition.
- **Stroke weight drift.** A 1.5px icon next to a 2px icon in the same context.
- **Sub-grid rendering.** A 17px icon on a 24px grid produces blurred edges. Stick to the family's grid sizes.
- **Icons announced redundantly.** A button with an icon and the visible label "Save" announcing "save save" because the icon wasn't marked decorative.

## Sources

- **Phosphor Icons**: https://phosphoricons.com : six-weight icon library covering 1300+ icons; thin/light/regular/bold/fill/duotone.
- **Lucide**: https://lucide.dev : fork of Feather Icons, 1500+ icons at 2px default stroke, used by Linear and many modern SaaS products.
- **Material Symbols**: https://fonts.google.com/icons : Google's variable-font icon system with optical-size, weight, fill, and grade axes.
- **Heroicons**: https://heroicons.com : Tailwind Labs' set, ships outline (1.5px) and solid (filled) variants.
- **Tabler Icons**: https://tabler.io/icons : 5500+ icons designed on a 24px grid at 2px default stroke.
- **Apple SF Symbols**: documented in Apple HIG (https://developer.apple.com/design/human-interface-guidelines/sf-symbols) : the standard for Apple-platform icons, with weight and scale axes that match SF (the system font).
- **Real product exemplars**: Linear (uses Lucide), Vercel (uses Geist Icons), Stripe (uses custom icons), Apple apps (use SF Symbols).
- **WCAG 2.2 / WAI-ARIA APG**: `aria-hidden`, `aria-label`, and `aria-labelledby` patterns for icon accessibility.
- **Refactoring UI** (Schoger / Wathan): icon-text optical balance, cap-height matching principles.

## See also

- [`accessibility.md`](accessibility.md): `aria-hidden`, `aria-label`, semantic icon patterns, RTL flip for directional icons.
- [`visual-hierarchy.md`](visual-hierarchy.md): icon size relative to text, optical weight, micro-whitespace between icon and label.
- [`assets/design-system/iconography.md`](../assets/design-system/iconography.md): the project's chosen icon family, default size, default weight.
- [`assets/design-system/components.md`](../assets/design-system/components.md): component-internal icon placement (button-internal, input chrome, list-row trailing).
- [`forms.md`](forms.md): form-field leading/trailing icons, validation icons, error icon pairing.
- [`pen-schema.md`](pen-schema.md): the `icon_font` and `icon_image` node types in the `.pen` schema.
