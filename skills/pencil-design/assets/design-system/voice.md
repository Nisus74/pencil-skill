# Voice

How user-facing copy reads in this product. The agent reads this when generating labels, titles, error messages, empty states, and CTAs. Each major section carries an *Archetype variants* subsection showing how the same voice reshapes under different archetypes (see `assets/archetypes/` in the skill), and anti-examples calling out the AI-default phrasings to avoid.

## Tone

`<friendly-professional | playful | clinical | technical>`, pick one and write a one-sentence description.

> Example: "Friendly-professional. We're warm and direct. We trust users to be smart. We don't apologise for things that aren't problems."

### Archetype variants

- **`saas-apps/b2b/analytics-dashboard`**: confident, terse, present-tense. Frames data, doesn't editorialise it. *"MAU climbed 12%"* beats *"Monthly active users showed an increase of 12% over the period."*
- **`saas-apps/b2b/modern-pro-tool`** (Linear-style): direct, sentence-case, present-tense. *"3 issues completed today"* beats *"You have completed 3 issues today!"*. Lowercase common; exclamation marks are extremely rare.
- **`marketing-websites/conversion-focused-saas`** (Linear marketing): confident, almost prescriptive. Hero headlines make claims and let them stand. *"Issue tracking is dead"*, *"A new species of product tool"*. Section copy is one-line confident, not feature lists.
- **`marketing-websites/editorial-storytelling`**: prescriptive in the manifesto flavour (Linear Method), cinematic in the product flavour (Apple). Body copy reads as essay, not marketing.

### What generic looks like (don't ship this)

*"Welcome back!"*, *"Let's get started!"*, *"You're all set!"*, *"Oh no, something went wrong!"*. Friendly exclamations everywhere, second-person "you" doing too much work, exclamation marks on confirmations.

## Case

- **Headings, titles, page titles:** sentence case. *"Account settings"*, not *"Account Settings"*.
- **Buttons, navigation labels:** sentence case. *"Sign in"*, not *"Sign In"*.
- **Acronyms:** keep their natural case. *"Edit URL"*, *"Add API key"*.

### Archetype variants

- **`saas-apps/b2b/modern-pro-tool`**: lowercase common is acceptable for sidebar section headers (*"workspace"*, *"your teams"*) when paired with a small chevron. Page titles still use sentence case.
- **`marketing-websites/conversion-focused-saas`**: numbered section labels in monospace (`1.0`, `2.0`, `2.1`) sit beside the heading, which uses sentence case. Decimal labels are the typographic signature.
- **`marketing-websites/editorial-storytelling`**: long editorial headings can break the sentence-case rule for stylistic effect; one or two display headings per page may use Title Case if the brand calls for editorial tone.

### What generic looks like (don't ship this)

*"Welcome To Your Dashboard"*, *"Get Started Today"*, *"Manage Your Account"*, ALL CAPS section headers, Title Case Navigation Labels.

## Buttons and CTAs

- Use a **specific verb**. *"Send invitation"* beats *"Submit"*. *"Save changes"* beats *"OK"*.
- Match the verb to the noun. *"Delete project"*, not *"Delete"* sitting alone.
- One action per button. If a button does two things, split it.

### Archetype variants

- **`saas-apps/b2b/modern-pro-tool`**: button labels often pair with a keyboard-shortcut chip rendered to the right of the label (*"Create new issue C"*). The shortcut sits in a darker mono pill inside the button.
- **`saas-apps/b2b/analytics-dashboard`**: CTAs are restrained, monospace numerals appear inside button labels when the button shows a count (*"Export 248 events"*).
- **`marketing-websites/conversion-focused-saas`**: CTAs lean into confidence (*"Try the new model"*, *"Open app"*) over generic verbs (*"Get started"*, *"Sign up"*).

### What generic looks like (don't ship this)

*"Submit"*, *"Click here"*, *"Learn more"*, *"OK"*, *"Cancel"*, *"Continue"* sitting alone with no object. Three primary buttons stacked in the same view.

## Error messages

Two-part template:

> **What happened.** **What to do.**

Examples:

- ✅ *"That email is already registered. Try signing in instead."*
- ❌ *"Error 409. Email already exists."*

- ✅ *"We couldn't reach the server. Check your connection and try again."*
- ❌ *"Network error."*

Don't blame the user. *"That email isn't valid"* beats *"You entered an invalid email"*.

### Archetype variants

- **`saas-apps/b2b/analytics-dashboard`**: terse, actionable. *"Couldn't load events. Retry"*. No apology theatre.
- **`saas-apps/b2b/modern-pro-tool`**: same pattern. *"Couldn't load. Retry"*. No apology, no exclamation marks.
- **`marketing-websites/*`**: errors are rare on marketing surfaces. When they appear (form validation), keep them inline and terse.

### What generic looks like (don't ship this)

*"Oh no, something went wrong! Please try again later."*, *"Sorry, we couldn't process your request 😞"*, *"Hmm, that didn't work. Try refreshing the page."*. Sad-face emoji, blame-shifting (*"You entered..."*), apology theatre.

## Empty states

Lead with the next action, not the absence.

- ✅ *"Create your first project to get started"*
- ❌ *"No projects yet"* (this can come *under* the action as supporting text)

A good empty state has: a title (≤ 8 words), one supporting sentence, and a primary CTA. Optional: a small illustration or icon cluster.

### Archetype variants

- **`saas-apps/b2b/analytics-dashboard`**: skip the illustration. Single confident headline + next action. *"No events tracked yet. Send your first one →"*.
- **`saas-apps/b2b/modern-pro-tool`**: four small abstract icons in a 2×2 cluster above the heading (decorative-but-restrained, not illustrated mascots), bold title, descriptive paragraph, two buttons (filled accent primary + secondary outline). The Linear pattern.

### What generic looks like (don't ship this)

Big illustrated mascot scene of someone holding an empty box with the title *"It's quiet here!"*, three buttons offering Import / Create / Explore Demo, decorative confetti shapes, *"Looks like there's nothing here yet, but no worries!"*

## Microcopy lengths

- **Button labels:** 1–3 words.
- **Form field labels:** 1–4 words.
- **Helper text under a field:** 1 sentence.
- **Section titles:** 1–5 words.
- **Page titles:** 2–6 words.
- **Toast messages:** 1 sentence.

## Confirmations and destructive actions

For irreversible actions (delete, archive, sign out, cancel subscription), require a confirmation. The confirmation:

- Names the thing being destroyed: *"Delete project 'Acme Marketing'?"*
- Says what it does: *"This will permanently remove all 23 boards and cannot be undone."*
- Uses a specific verb on the destructive button: *"Delete project"*, not *"Confirm"*.

### What generic looks like (don't ship this)

*"Are you sure you want to delete this?"* with `Cancel` and `OK` buttons, no specific verb, no detail on what gets deleted, no count of dependent items.

## Forbidden / discouraged words

These read as either jargon or filler. Replace.

| Avoid | Prefer |
|-------|--------|
| *Utilize* | *Use* |
| *In order to* | *To* |
| *Please* (in product UI) | (just say what to do) |
| *Sorry* (for non-errors) | (just say what happened) |
| *Click here* | A specific link label |
| *Submit* | A specific verb |
| *Elevate* | (cut, AI cliché) |
| *Seamless* / *seamlessly* | (cut, AI cliché) |
| *Unleash* | (cut, AI cliché) |
| *Empower* | (cut, AI cliché) |
| *Next-gen* / *Next-generation* | (cut, AI cliché) |
| *Revolutionize* | (cut, AI cliché) |
| *Cutting-edge* | (cut, AI cliché) |
| *Leverage* (as verb) | *Use*, or be more specific |
| *Robust* | be specific about what's solid |
| *Foster* | *Build*, *grow*, or be specific |
| *Holistic* | (cut, AI cliché) |
| *Transformative* | (cut, AI cliché) |
| *Streamline* (without specifics) | name what's being removed |

Add product-specific bans here.

## Filler to avoid

These read as machine-generated when they appear in shipped product:

- **Hero filler:** *"Scroll to explore"*, *"Swipe down"*, animated chevrons. If a hero needs a prompt, write a real one tied to the product.
- **Placeholder names:** *John Doe*, *Acme*, *Nexus*, *Lorem Ipsum*. Use plausible context-appropriate content; for imagery use `G(node, "ai", "...")`.
- **Fabricated metrics:** invented stats, made-up testimonials, fake "system status" numbers. Either source real data or omit the section.
- **`LABEL // YEAR` formatting:** the slash-separated typographic affectation borrowed from generated portfolio sites.
- **Emojis in production UI:** acceptable only if explicitly opted into above for specific surfaces (e.g. a status pill set, a celebratory toast). Most archetypes treat emoji as an anti-cue.

## Numbers, dates, currency

- **Numbers:** group with commas above 999. *"1,234 users"*.
- **Dates:** *"Mar 5, 2026"* in body copy. ISO (`2026-03-05`) only in technical contexts.
- **Time durations:** abbreviate inline (*"3m ago"*, *"2h"*) but spell out in headings (*"3 minutes ago"*).
- **Currency:** include the symbol and code on first reference if ambiguous: *"$1,234 USD"*.

### Archetype variants

- **`saas-apps/b2b/analytics-dashboard`**: numerics use monospace so columns align. Percentages to 1 decimal (*"4.6%"*, not *"5%"* or *"4.583%"*).
- **`marketing-websites/conversion-focused-saas`**: pricing on the pricing page uses *proportional* currency notation, not monospace. Customer metrics on testimonial sections use bold numerics with surrounding context (*"3.3x faster"*, *"28% issues authored by agents"*).

## Voice diff for marketing vs product

If you ship a marketing site and a product, they often differ:

- **Marketing voice:** more aspirational, more rhetorical, more variable cadence.
- **Product voice:** terser, more imperative, more consistent.

If your project has both, note here which voice applies where. Or split this file into `voice.md` (product) and add a `voice-marketing.md` later. The archetype split helps too: pick a `marketing-websites/*` archetype for the marketing surfaces and a `saas-apps/*` archetype for the product, and the voice flows from each.
