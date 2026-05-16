# Rewrite

Rewrite is the UX-copy pass. Labels, error messages, button text, empty-state copy, microcopy, instructions, helper text. Bad copy reads as machine-generated faster than bad colour or layout; the right pixel-level design with the wrong words still gives the surface away.

Rewrite isn't [pare.md](pare.md). Pare removes; rewrite replaces. Often they run in sequence: pare cuts the redundant CTAs and filler sections; rewrite then sharpens what's left so each remaining string earns its presence.

Use this reference when the design is functionally complete but the copy reads as placeholder, when the labels were AI-generated and never revisited, when *"Submit"* is on a button that does something more specific, when error messages say *"Something went wrong"* and nothing else.

## Register

On brand surfaces, the voice is part of the brand expression. Warmer, more opinionated copy is allowed and often required. *"Saved. Your edits are live."* beats *"Save successful."* in almost every brand context. The copy carries character; the rewrite pass is where the character lands.

On product surfaces, the voice is neutral, outcome-named, specific. Form labels are nouns; button labels are verbs naming the action's effect; error messages are diagnostic. Character has a place (empty states, recovery moments, signature toasts) but the default register is functional. *"Send invoice"* not *"Submit"*; *"That email is already in use"* not *"Invalid input."*

Both registers refuse the AI cliché list from [ux-writing.md](ux-writing.md). Brand can be warm; product can be neutral; neither can be *"Elevate your workflow with seamless automation."*

For the per-register depth, see [brand.md](brand.md) and [product.md](product.md).

## Assess current state

Run `search_all_unique_properties({ property: "content" })` (or walk the design tree) to list every text node on the surface. For each one, rate it:

- **Specific.** The string couldn't have been generated for a different product; it names something the user can act on in this context.
- **Generic.** The string would work on three other products without modification. *"Welcome"*, *"Overview"*, *"Get started"*, *"Submit"*, *"Continue"*, *"Done"*.
- **Cliché.** The string is on the AI slop list. *"Elevate"*, *"Seamless"*, *"Unleash"*, *"Next-Gen"*, *"Revolutionize"*, *"Empower"*, *"Unlock"*, *"Transform"*.

Generic and cliché both rewrite. Specific stays unless it's wrong (which is rare; specific strings usually got that way deliberately).

For error states specifically, ask: *"does this string say what went wrong, why, and how to fix?"* Many error messages clear *"specific"* on the rating above but still fail the what-why-how-to-fix test.

## Plan

Decide which strings get character and which stay neutral.

- **Brand surfaces:** most copy can lean character. Hero copy, CTAs, empty states, error messages, success toasts. The exception: legal and compliance copy (terms, privacy, payment confirmations) stay sober.
- **Product surfaces:** most copy stays neutral. Form labels, button labels on critical actions, error messages on data-loss-adjacent operations. The exception: empty states, onboarding copy, recovery moments, and the occasional signature toast can carry warmth.
- **Cross-cutting:** dates, numbers, counts, statuses (*"Active"*, *"Pending"*, *"Failed"*) stay neutral in both registers. The character isn't in the state label; it's in the longer copy around it.

Output of the plan is a per-string disposition. *"Rewrite the hero headline for specificity; keep the form labels neutral; warm up the empty state; rewrite the error message to include what / why / how-to-fix."*

## Apply across copy categories

### Button labels

Outcome-named, never generic.

| Generic | Specific |
|---|---|
| *"Submit"* | *"Send invoice"* / *"Create account"* / *"Save changes"* |
| *"Continue"* | *"Continue to payment"* / *"Continue to step 3"* |
| *"OK"* | *"Got it"* / *"Sounds good"* on confirmation; verb-named on action |
| *"Done"* | *"Save and close"* / *"Finish setup"* |
| *"Cancel"* | *"Discard changes"* / *"Keep editing"* (one option, named) |

Destructive actions get the destructive verb. *"Delete account"* not *"Confirm"*; *"Remove member"* not *"Continue"*. The user should know what the button will do before pressing it.

### Error messages

Three required parts, in order: what went wrong, why, how to fix.

| Generic | What / why / how-to-fix |
|---|---|
| *"An error occurred."* | *"Invoice 4521 didn't send: Stripe rejected the card. Try a different payment method."* |
| *"Network error."* | *"Couldn't load jobs: the connection timed out. Retry, or check status.example.com."* |
| *"Invalid email."* | *"That email is already in use. Try signing in instead, or use a different email."* |
| *"Permission denied."* | *"This workspace is locked to owners. Ask Aiko for access."* |
| *"Something went wrong."* | (Never. Find the specific cause and name it.) |

For the deeper error-message register and the technical-error-versus-user-error distinction, see [ux-writing.md](ux-writing.md).

### Empty states

Specific, warm, with a forward path.

| Generic | Specific |
|---|---|
| *"No items."* | *"No invoices yet. When you bill a customer, they'll show up here."* |
| *"No results."* | *"Nothing matches *'overdue and unpaid'*. Try fewer filters?"* |
| *"You don't have access."* | *"This one's locked. Ask Aiko (the workspace owner) for access."* |
| *"Loading..."* | *"Wrangling the data..."* (brand) or *"Loading invoices..."* (product) |

The forward path matters most. An empty state without a *"here's what to do next"* affordance is a dead end.

### Form labels

Noun-named, no colons, no asterisks.

- *"Email"*, not *"Email:"* or *"Email *"*
- *"Company name"*, not *"What's your company name?"*
- *"Workspace owner"*, not *"Select workspace owner"*
- Helper text for *"required"* goes below or alongside the field; the label itself stays clean.

### Helper text and placeholders

Real examples, not *"e.g."*.

- Placeholder: *"aiko@example.com"* not *"e.g. john@example.com"* and never *"Enter email"* (that's a worse label, not a placeholder).
- Helper text below the field: *"We'll send a confirmation here. Use a personal address if you prefer."* not *"Required."*

### Headings

Specific, never generic-by-reflex.

- *"Welcome"* / *"Overview"* / *"Dashboard"* are reserved for cases where the user can't be told more. If the page is about their billing, the heading is *"Your billing"* or *"Billing overview"*, not *"Overview"*.
- Section headings inside a page can be utilitarian (*"Account"*, *"Notifications"*) when the rest of the page carries the context.
- Marketing headings sit on the brand side; cross-link [brand.md](brand.md) for the hero-anatomy guidance.

### AI cliché strikes

Replace every instance of the slop list with plain language or specific alternatives.

| Cliché | Plain |
|---|---|
| *"Elevate your workflow"* | *"Send invoices in two clicks"* (or whatever the surface actually does) |
| *"Seamless integration"* | *"Connect in 30 seconds"* / *"One-click setup"* |
| *"Unleash creativity"* | *"Sketch faster"* / *"Open the canvas"* |
| *"Next-generation platform"* | *"Built in 2025"* / *"Rebuilt from scratch"* |
| *"Revolutionize your team"* | (Replace with the actual outcome the user gets.) |
| *"Empower"* | *"Help"* / *"Let"* / *"Enable"* (verbs that don't lie about effort) |
| *"Transform"* | (Specific verb naming what changes.) |
| *"Unlock"* | (Specific verb naming what becomes possible.) |

The full slop list and the per-register tone calibration live in [ux-writing.md](ux-writing.md). This is the rewrite-pass shortlist; the deeper register guidance is upstream.

## Never

- **Never use Lorem Ipsum.** Placeholder text obscures the absence of thought; the design ships against realistic copy or it isn't ready.
- **Never put *"Submit"* on a button that does something specific.** Name the action.
- **Never describe a destructive action with neutral language.** *"Delete"* not *"Continue"*; *"Discard"* not *"Done"*.
- **Never use a heading the user can't act on.** *"Welcome"* without context is filler; cut it or make it specific.
- **Never write copy that would survive being copy-pasted into a different product.** That's the AI slop test for copy.
- **Never leave AI cliché words in place.** Strike, replace, or delete; the user can tell.
- **Never combine a placeholder and a label saying the same thing.** *"Email"* label with *"Enter your email"* placeholder is redundant; the placeholder shows an example or it's empty.
- **Never write error messages without what / why / how-to-fix.** Single-sentence errors that omit any of the three are bad design.

## Verify

After the rewrite pass, walk the surface and run these checks:

- **Every button names its outcome.** No *"Submit"*, no *"OK"* on action buttons, no generic *"Continue"* where a specific verb would clarify.
- **Every error has what / why / how-to-fix.** No *"An error occurred"* generic copy remains; each error is diagnostic.
- **No AI clichés.** None of the Severity 1 slop words appear; the Severity 2 words are at most one per surface.
- **Empty states have a forward path.** Every empty-state copy block tells the user what to do next.
- **Headings are specific.** The user can name what each section is about from the heading alone.
- **The copy reads like a specific person wrote it.** A stranger reading the surface should recognise the brand's voice from the copy alone; the copy is one of the brand's signals.

When the result feels right, hand off to [finalise.md](finalise.md) for the alignment, spacing, and token-consistency pass.
