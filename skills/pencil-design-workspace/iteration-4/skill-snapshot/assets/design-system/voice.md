# Voice

How user-facing copy reads in this product. The agent reads this when generating labels, titles, error messages, empty states, and CTAs.

## Tone

`<friendly-professional | playful | clinical | technical>` — pick one and write a one-sentence description.

> Example: "Friendly-professional. We're warm and direct. We trust users to be smart. We don't apologize for things that aren't problems."

## Case

- **Headings, titles, page titles:** sentence case. *"Account settings"*, not *"Account Settings"*.
- **Buttons, navigation labels:** sentence case. *"Sign in"*, not *"Sign In"*.
- **Acronyms:** keep their natural case. *"Edit URL"*, *"Add API key"*.

## Buttons & CTAs

- Use a **specific verb**. *"Send invitation"* > *"Submit"*. *"Save changes"* > *"OK"*.
- Match the verb to the noun. *"Delete project"*, not *"Delete"* sitting alone.
- One action per button. If a button does two things, split it.

## Error messages

Two-part template:

> **What happened.** **What to do.**

Examples:

- ✅ *"That email is already registered. Try signing in instead."*
- ❌ *"Error 409. Email already exists."*

- ✅ *"We couldn't reach the server. Check your connection and try again."*
- ❌ *"Network error."*

Don't blame the user. *"That email isn't valid"* > *"You entered an invalid email"*.

## Empty states

Lead with the next action, not the absence.

- ✅ *"Create your first project to get started"*
- ❌ *"No projects yet"* (this can come *under* the action as supporting text)

A good empty state has: a title (≤ 8 words), one supporting sentence, and a primary CTA. Optional: a small illustration.

## Microcopy lengths

- **Button labels:** 1–3 words.
- **Form field labels:** 1–4 words.
- **Helper text under a field:** 1 sentence.
- **Section titles:** 1–5 words.
- **Page titles:** 2–6 words.
- **Toast messages:** 1 sentence.

## Confirmations & destructive actions

For irreversible actions (delete, archive, sign out, cancel subscription), require a confirmation. The confirmation:

- Names the thing being destroyed: *"Delete project 'Acme Marketing'?"*
- Says what it does: *"This will permanently remove all 23 boards and cannot be undone."*
- Uses a specific verb on the destructive button: *"Delete project"*, not *"Confirm"*.

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
| *Elevate* | (cut — AI cliché) |
| *Seamless* / *seamlessly* | (cut — AI cliché) |
| *Unleash* | (cut — AI cliché) |
| *Empower* | (cut — AI cliché) |
| *Next-gen* / *Next-generation* | (cut — AI cliché) |
| *Revolutionize* | (cut — AI cliché) |
| *Cutting-edge* | (cut — AI cliché) |

Add product-specific bans here.

## Filler to avoid

These read as machine-generated when they appear in shipped product:

- **Hero filler:** *"Scroll to explore"*, *"Swipe down"*, animated chevrons. If a hero needs a prompt, write a real one tied to the product.
- **Placeholder names:** *John Doe*, *Acme*, *Nexus*, *Lorem Ipsum*. Use plausible context-appropriate content; for imagery use `G(node, "ai", "...")`.
- **Fabricated metrics:** invented stats, made-up testimonials, fake "system status" numbers. Either source real data or omit the section.
- **`LABEL // YEAR` formatting:** the slash-separated typographic affectation borrowed from generated portfolio sites.
- **Emojis in production UI:** acceptable only if explicitly opted into above for specific surfaces (e.g. a status pill set, a celebratory toast).

## Numbers, dates, currency

- **Numbers:** group with commas above 999. *"1,234 users"*.
- **Dates:** *"Mar 5, 2026"* in body copy. ISO (`2026-03-05`) only in technical contexts.
- **Time durations:** abbreviate inline (*"3m ago"*, *"2h"*) but spell out in headings (*"3 minutes ago"*).
- **Currency:** include the symbol and code on first reference if ambiguous: *"$1,234 USD"*.

## Voice diff for marketing vs. product

If you ship a marketing site and a product, they often differ:

- **Marketing voice:** more aspirational, more rhetorical, more variable cadence.
- **Product voice:** terser, more imperative, more consistent.

If your project has both, note here which voice applies where. Or split this file into `voice.md` (product) and add a `voice-marketing.md` later.
