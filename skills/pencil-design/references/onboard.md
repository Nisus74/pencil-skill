# Onboarding

The first session is the user's whole impression of the product. The onboarding flow decides whether they reach the activation moment (the first use that delivers value) or bounce. Most generated onboarding flows pile on tutorials, modals, and tooltips that delay activation rather than accelerate it. This reference covers the patterns that actually work.

This sits next to [states.md](states.md) (which covers the four empty-state types in taxonomy) and the first-use guidance in [product.md](product.md). Use it when designing any first-run experience, an empty-but-not-empty state, or any flow whose job is to get a new user to value.

## What onboarding is for

One thing: getting the user to the activation moment. The activation moment is the specific action that turns a new user into a using user.

| Product | Activation moment |
|---|---|
| A design tool | First design saved |
| A communication tool | First message sent |
| A workflow tool | First task completed |
| A note-taking app | Fifth note created |
| An analytics tool | First chart connected to real data |
| A team product | Second teammate invited and joins |

If the design doesn't know the activation moment, find out before designing. Onboarding without a target is decoration.

## Three onboarding shapes

Pick one per product; mixing produces conflicting signals.

### Just start
The user lands in the product and starts using it. No tour, no tutorial, no setup wizard. The product is self-explanatory enough that exploration teaches.

Works for: tools with a low conceptual barrier (a notes app, a search tool, a calendar). Doesn't work for: tools with significant model complexity (a workflow engine, a CRM, an analytics platform).

### Guided first action
The user lands and the product walks them through one specific first action. Not a tour; a single guided do-the-thing. *"Let's create your first project."* The user does it; the product is now non-empty; activation is closer.

Works for: tools where the first action is meaningful and creates state the user will keep. Most product UIs benefit from this shape.

### Setup flow
The user does meaningful configuration before the product can be useful. Workspace name, team members, connected accounts, payment method. The product can't operate without these inputs.

Works for: tools that genuinely need configuration (a payments platform, a CI system, an integration product). Doesn't work for: tools that don't need it (most B2B SaaS forces this shape unnecessarily).

## What onboarding should not do

- **Show a feature tour.** Modals walking the user through every menu item. The user forgets all of it the moment they close the tour.
- **Surface every preference.** The user doesn't know what their preferences are yet. Set sensible defaults; let them adjust later.
- **Use the first session to upsell.** The user is evaluating the product; pushing them to upgrade before they've activated kills both activation AND upgrade.
- **Force account creation before value.** Let the user touch the product first; gate the save / share / sync behind signup once they've felt the value.
- **Block on email confirmation.** Send the email, but let the user keep going. Confirm later.
- **Show a video tutorial as the first interaction.** Most users skip; the ones who don't, hit the back button.

## Components of a strong onboarding

### The first screen
The first surface should communicate one thing only. *"Welcome, here's what's next."* Not a feature list. Not a video. Not three CTAs. One.

Specifically:
- One concrete next action (a primary CTA).
- One sentence of context about what the action does.
- One escape hatch (a skip link or a non-primary "explore on my own" path) for users who hate being led.

### Empty states as onboarding moments
A first-use empty state IS onboarding for that surface. The user lands on the dashboard for the first time; the dashboard is empty; the empty state's job is to point at the activation moment.

Pattern: *"You'll see [thing] here once you [action]. [Specific CTA that takes them to do the action]."*

Bad: *"No items yet."*
Good: *"You'll see invoices here once you bill a customer. Send your first invoice →"*

See the empty-state-copy patterns in [ux-writing.md](ux-writing.md).

### Progressive disclosure
The product surface has more capability than the user will encounter on day one. Hide what they don't need yet; surface it when they're ready.

Practical patterns:
- The full settings page exists but the new user's first-session settings UI shows only 3–4 essential options.
- Advanced features are reachable but not foregrounded; users discover them as their use deepens.
- Power-user keyboard shortcuts and bulk actions are present from day one (they don't hurt new users) but their existence is communicated only after the user has demonstrated familiarity (clicked the same area 10 times in a row, say).

### The contextual nudge
A first-use nudge that surfaces at the moment a feature becomes relevant. *"Tip: Press Cmd-K to jump to any project."* Shown the first time the user navigates between three or more projects in a session. Not on first login, when it's noise.

Discipline: nudges have an explicit "got it" dismiss; nudges don't repeat once dismissed; nudges never have a skip-tour option that resets to showing all of them again. Recognise that nudges are interruptions even when subtle; a flow with five contextual nudges feels micromanaged.

### The activation moment hand-off
When the user reaches the activation moment, *say so*. *"You just sent your first message. That's the hardest part."* The acknowledgement closes the onboarding loop and signals that the product worked.

Most products skip this and treat the activation moment as just-another-action. The user does the thing; the product moves on. The user doesn't realise they crossed the threshold.

## Empty states by user state

A surface's empty state changes meaning depending on where the user is in their journey.

### First-use (the user has never used this surface)
Onboarding-shaped. Explain what populated looks like, point at the first action.

### Returning-empty (the user has used this surface before, but it's currently empty)
Acknowledgement-shaped. *"You're caught up."* / *"Inbox zero."* / *"Nothing new since your last visit."* Don't re-onboard.

### Result-empty (a query returned nothing)
Specific to the query. *"No invoices match these filters. Clear filters →"* Don't generalise; the user just did a specific thing.

### Permission-empty (the user can't see content here)
Explain what they're missing and the path to access. *"Only workspace admins see billing. Ask your admin if you need access."*

All four are covered in the empty-state taxonomy in [states.md](states.md) and the copy patterns in [ux-writing.md](ux-writing.md). The onboarding-specific dimension is first-use vs returning-empty: they look different even when the data is identically absent.

## Sample data and seeded content

For products where activation requires non-trivial input from the user, consider seeded content for the first session: a sample project, an example board, a demo team. The user can poke at it, see what the product looks like populated, and either replace it or set it aside.

Discipline:
- Seeded content is visibly seeded (a *"Sample"* badge or similar) so the user doesn't confuse it with their own.
- Seeded content is deletable in one click after the user has their own content.
- Seeded content uses plausible names from the product's domain, not *"Lorem"* / *"John Doe"* / *"Project Alpha"*. See [ux-writing.md](ux-writing.md) on placeholder discipline.

## Per-register considerations

### Brand
Brand onboarding (the marketing landing → signup → first session arc) is shaped by the landing's promise. The first session should pay off the landing's pitch immediately. If the landing said *"Generate UI in 30 seconds"*, the first session shows the generation working, not a configuration wizard.

### Product
Product onboarding lives in the product surface itself. It's the first-session empty states, the guided first action, the contextual nudges as the user explores. It rarely benefits from a separate onboarding *"flow"*; the onboarding IS the product's first-use behaviour.

## Pencil-specific

### Designing the first-use frame as a sibling
For product surfaces, build the first-use state as a sibling frame next to the populated state. The two frames share components but have different content shapes. Name them clearly: `Dashboard_FirstUse`, `Dashboard_Populated`. The handoff to engineering then has both states visible.

### `EmptyState` component variants
Build the four empty-state types (first-use, returning-empty, no-results, no-permission) as variants of an `EmptyState` reusable component in `.lib.pen`. The first-use variant carries onboarding-shaped copy and a primary CTA pointing at the activation action; the others are quieter.

### Onboarding flow as a sequence of frames
For products where onboarding is a guided multi-step flow (workspace setup, integration wizard, etc.), build each step as a sibling frame: `Onboarding_Step1`, `Onboarding_Step2`. Use the multi-step pattern from [flows.md](flows.md) (validation timing, back-stack, persistence between steps).

### Annotate the activation moment in `context`
On whatever frame represents the activation moment in the design, write the intent into `context`: *"Activation moment: first task created. Trigger the activation toast (`ActivationToast` component) on successful creation."* This tells the engineer not to treat the moment as just-another-action.

### Verify against first-time-user eyes
The most common Pencil onboarding failure: designing it with full product knowledge in mind. The agent has the schema, the product spec, the brand brief; the user has none of these. Test the onboarding by walking it with no prior context: *"If I just landed here, would I know what to do?"* Most generated onboarding fails this test.
