# Microcopy

The words on the buttons matter more than the colours behind them. A 'Continue' button asks the user to do work; 'Save changes' tells them what'll happen. A 'Something went wrong' error blames a faceless system; 'We couldn't reach the server. Try again in a minute.' tells them what to do next. Microcopy is where design decisions become language decisions.

**What this file owns:** the shapes of microcopy across UI surfaces (headlines, CTAs, errors, empty states, success messages, confirmations, system status, loading copy), the voice and tone framework, and the localisation considerations.

**What this file does NOT own:** marketing copy or long-form content. That's the project's content team. The visual treatment of the copy (typography, colour, hierarchy) is in [`visual-hierarchy.md`](visual-hierarchy.md) and [`assets/design-system/tokens.md`](../assets/design-system/tokens.md). Where the copy lives in components (default text vs slot fill) is in [`composition-patterns.md`](composition-patterns.md).

## When to load this file

- The agent is writing button labels, error messages, empty state text, headlines, or any UI copy.
- The user reports the copy 'sounds robotic' or 'doesn't match the brand'.
- The project has a populated `assets/design-system/voice.md` and the agent needs to align with it (this file is the principles; voice.md is the project's commitments).
- The design includes states (error, empty, loading, success) and the placeholder copy needs replacing.

## Voice & tone framework

Voice is the constant. Tone shifts with the situation. A confident, friendly voice adapts its volume to the situation while keeping the personality steady. The brand sounds like itself across every state.

Three axes to calibrate per project:

- **Formal ↔ casual.** Formal: 'Your account has been updated.' Casual: 'Saved.' Calibrate to the audience's professional register.
- **Serious ↔ playful.** Serious: 'Payment processed successfully.' Playful: 'You're all set.' Match the stakes of the action; payment confirmations don't need jokes.
- **Calm ↔ energetic.** Calm: 'Your changes are saved.' Energetic: 'Saved! Looking good.' Calm wears better in a tool the user spends hours in.

Most B2B SaaS lives at the centre of all three: friendly, serious, calm. Consumer apps tend toward casual, playful, and energetic. Pick a position and hold it across surfaces. Voice that drifts (formal in error, casual in success) reads as inconsistent.

For the project's specific voice commitments, see `assets/design-system/voice.md`: the project's calibration of these principles.

## Headlines

A headline does one job: convince the user to keep reading. The headline that works is verb-led, benefit-focused, and specific. Generic feature lists don't pull weight.

- **Verb-led.** 'Cut your build time by 40%' beats 'Faster builds'. The verb implies the user takes action.
- **Benefit-focused.** Lead with what the user gets. 'Build apps without writing code' beats 'Visual app builder'.
- **Specific.** Numbers, named outcomes, concrete examples. 'Save 4 hours per week on reports' beats 'Save time on reports'.

Test: cover the headline. Read the supporting paragraph. Could the user infer the headline from the paragraph? If yes, the headline is generic. If the paragraph could pair with any of three different headlines, the headline isn't specific enough.

## Buttons / CTAs

The button label is a contract. It tells the user what'll happen when they click. Generic labels break the contract.

- **Action-specific verbs.** 'Save changes', 'Delete project', 'Send invitation', 'Publish article'. The verb plus the noun tells the user the consequence.
- **Never 'Continue', 'Submit', 'OK' for first-party actions.** These are dialogue-box defaults from 1995. They tell the user nothing. The exception: secondary cancellation buttons can use 'Cancel' (every user knows what Cancel means).
- **Match button labels to the action's stakes.** The confirmation label for deleting 12 items should restate the action and the count. A bare 'Yes' loses the consequence and invites slip-clicks.
- **First-person vs second-person.** 'Save my changes' speaks in the user's voice and reads as friendlier. 'Save changes' is imperative and reads as more direct. Pick one and stay consistent.

Stripe's pattern is worth stealing: every button label includes the verb and the object. 'Create payment link', 'View customer', 'Refund charge'. The user always knows what they're about to do.

## Error messages

Three things every error message has to do: state what happened, hint why, and tell the user what to do next.

- **What happened.** Specific to the failure. 'We couldn't load your projects' tells the user the operation that failed. Generic phrases like 'Something went wrong' tell them nothing.
- **Why.** When the cause is recoverable by the user, name it: 'Your network connection dropped.' When the cause is server-side, say so without blaming the user. 'Our server is temporarily slow to respond' acknowledges the issue without finger-pointing.
- **What to do next.** A retry button, a path forward, or a clear next step. 'Try again in a minute' is better than nothing. 'Check your connection and retry' tells the user where to look.

Don't blame the user. 'You entered an invalid email' makes the user feel stupid. 'Use a valid email address (like name@domain.com)' is the better shape because it shows the user what to type.

Don't surface technical detail. 'NetworkError: ECONNREFUSED at handleRequest()' is debugger output. The user sees: 'We couldn't reach the server. Try again in a minute.' The technical detail goes to the support team via the error code in the footer.

For the visual treatment of error states, see [`states.md`](states.md). For form-specific error display (inline next to field, focus first error on submit), see [`forms.md`](forms.md).

## Empty state copy

Empty states are an opportunity. The user is here for the first time, or the page is genuinely empty after a clean-up. The copy should encourage and guide.

- **Show what's possible.** 'Create your first project to get started' frames the empty state as a beginning. 'No projects yet' frames the same situation as a deficit.
- **Lead with the action.** 'Add your first contact' is the empty state's headline. The supporting copy explains what contacts unlock. The CTA repeats the verb.
- **One CTA.** A first-use empty state with three competing actions ('Create', 'Import', 'Explore demo') paralyses the user. Pick the one most users do first; demote the rest to text links.
- **Filtered-empty differs from first-use empty.** When a filter returned nothing, the copy names the filter: 'No projects match 'archived''. The CTA clears the filter or refines the search. Don't treat 'no results from a filter' the same as 'never created anything'.

For the empty-state taxonomy (first-use, no-results, no-permission, post-action) and visual lockup, see [`states.md`](states.md) § Empty state taxonomy.

## Success copy

Success is the cheapest place to overdo it. A celebratory toast on every save trains the user to ignore the toast. Calibrate the celebration to the stakes:

- **Routine save.** Quiet feedback. A 'Saved 2 minutes ago' indicator next to the field, no toast.
- **Significant action.** A toast, briefly. 'Project created.' Five seconds, dismiss-on-click.
- **High-stakes completion.** A modal or full-screen confirmation with a clear next step. 'Welcome to <product>! Here's what to do next.' Reserve for sign-up completion, payment success, account creation.

Don't over-celebrate. 'Awesome! Your changes are saved!' for routine work reads as condescending. The user did normal work; treat it as normal.

Tell the user what happens next. 'Project created. Add your first board.' The success message is also a prompt for the next action.

## Confirmation copy

When the user is about to do something destructive or irreversible, the confirmation modal carries the weight.

- **State the consequence.** 'This will delete 12 items permanently.' Number the items. Name the action. Don't soften ('Are you sure?').
- **Label the action button with the action.** 'Delete 12 items' is the destructive label, paired with 'Cancel' on the safe option. Never use 'Confirm' (the user can't tell what they're confirming).
- **Position destructive on the right, safe on the left.** Convention puts the primary action on the right; for destructive confirmations, the destructive action is the primary in this context (the user is here to confirm). Pair with a destructive colour treatment so the visual weight matches the consequence.
- **Reserve typed confirmation for the most consequential.** 'Type 'delete acme' to confirm' is right for deleting an org or production data. It's overkill for deleting a comment.

For the modal vs toast confirmation decision (hard vs soft), see [`flows.md`](flows.md) § Confirmations & undo.

## System status

The user wants to know whether the system is doing what they asked. Status copy should be specific and current.

- **Specific.** 'Saved 2 minutes ago' beats 'Up to date' because it names the time. Reassuring fluff doesn't help the user check whether their work is safe.
- **Current.** Update in real time as state changes. A 'Saved' indicator that lingers for an hour after the last save is misleading.
- **Quiet.** Status is ambient. Small text, muted colour, near the affected content. Banners are too loud for ongoing status.

Connection status is a special case: surface it explicitly when the user goes offline, and let the absence of an indicator stand for normal connectivity.

## Loading copy

Loading is dead time. Fill it with information. 'Fetching your projects' tells the user what's happening. 'Loading...' just says the system is busy without naming the operation.

- **Name what's loading.** 'Fetching your projects', 'Processing your image', 'Verifying your account'. The user knows the operation, which makes the wait feel intentional.
- **Vary the copy across loads.** A product where every loading state says 'Loading...' reads as templated. Different operations get different copy.
- **Use ellipsis to signal in-progress states ('Saving...') or that a button opens a follow-up dialog ('Rename...').** A button that triggers an immediate action stays plain: 'Save' without the ellipsis. See [`interactions.md`](interactions.md) § Ellipsis conventions.

For the timing rules around loading states (show-delay, min-visible-time), see [`interactions.md`](interactions.md) § Loading states.

## Localisation considerations

Microcopy that's hard to translate is harder to maintain. Three considerations to bake in from the start:

- **Avoid metaphors that don't travel.** 'Hit the road' makes no sense in languages without that idiom. Generic verbs like 'Get started' carry across languages without losing meaning.
- **Leave room for longer translations.** German compound nouns can be 30% to 50% longer than English; Russian sentences run longer too. Button widths sized to fit the English label exactly will break in German. Leave breathing room.
- **Don't bake plurals into single strings.** A copy template like 'You have {count} items' breaks in languages with multiple plural forms (Russian, Polish, Arabic). Use the platform's pluralisation system (ICU MessageFormat, i18next plurals) and write the copy with all forms in mind.

For the project's specific localisation strategy, see `assets/design-system/voice.md` § Localisation (when populated).

## Pencil expression

Microcopy lives in two places in `.pen`:

- **Default text in component children.** The `text` value on a node is the default copy. For reusable components, this is the placeholder copy that appears when no slot override is provided.
- **Slot fill on instances.** When a component is instantiated via `ref`, the consumer can override the slot's text via `descendants`. The component definition documents the expected copy shape ('Action verb + noun', 'Single-line summary, < 60 characters').

Document the copy shape in the component's `context`: *'Slot expects an action-specific verb + noun, e.g. 'Save changes', 'Send invitation'. Avoid generic verbs (Continue, Submit).'* The next agent reading the component knows the constraint.

For copy that crosses many components (error message templates, empty state lockups), define a small set of reusable copy patterns in `assets/design-system/voice.md` (when the project has one) and reference them by name in component `context`.

## Anti-patterns

These read as copy-blind designs and should be fixed in passing:

- **Generic CTAs.** 'Continue', 'Submit', 'OK', 'Get started' (when not a sign-up button), 'Learn more' (without naming what). Replace with action-specific verbs.
- **Error messages that blame the user.** 'You entered an invalid email.' Rewrite to guide: 'Use a valid email address.'
- **Loading copy that's just 'Loading...'.** Vary by operation. Name what's loading.
- **Confirmation buttons labelled 'Confirm' or 'Yes'.** Restate the action. The user should be able to read just the button label and know what they're doing.
- **Over-celebratory success copy.** 'Awesome!' on routine work. Calibrate to stakes.
- **Status copy that's stale.** 'Up to date' that hasn't updated in an hour. Either make it real-time or remove it.
- **Lorem ipsum shipped to design review.** Replace with plausible content matching the surface (see [`flows.md`](flows.md) § Plausible content).
- **Identical loading copy across the product.** A tell that the copy was an afterthought.

## Sources

- **Microcopy: The Complete Guide** (Kinneret Yifrah, 2nd edition): the canonical reference for the patterns in this file. Voice and tone, error messaging, and confirmation copy come directly from there.
- **Mailchimp Content Style Guide** (styleguide.mailchimp.com): voice and tone framework, conversational microcopy patterns.
- **Shopify Polaris voice and tone**: confidence-without-arrogance principles for B2B microcopy.
- **Atlassian Design System voice**: collaboration-focused microcopy patterns.
- **Apple HIG: Writing**: succinct, direct copy guidance for iOS/macOS conventions.
- **Google Developer Documentation Style Guide**: technical microcopy patterns, plain language guidance.
- **Stripe Style Guide**: action-specific button label patterns ('Create payment link', 'Refund charge').
- **Nielsen Norman Group**: research on error message effectiveness, button label specificity, empty state effectiveness.
- **ICU MessageFormat / i18next**: pluralisation guidance for the localisation section.

## See also

- `assets/design-system/voice.md`: the project's specific voice commitments (when populated). This file is the principles; voice.md is the project's calibration.
- [`states.md`](states.md): empty state taxonomy and screen-level fault state copy.
- [`flows.md`](flows.md): confirmation patterns (modal vs toast), plausible content guidance.
- [`forms.md`](forms.md): form-specific error display and validation copy.
- [`interactions.md`](interactions.md): ellipsis conventions, loading state timing.
- [`accessibility.md`](accessibility.md): screen reader announcement patterns for errors and status.
- [`layout-patterns.md`](layout-patterns.md): where copy fits in marketing pages, dashboards, settings.
