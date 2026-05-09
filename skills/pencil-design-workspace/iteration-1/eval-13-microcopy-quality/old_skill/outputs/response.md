# Project tracker microcopy

I treated this as a copy task, not a canvas task — you didn't ask me to lay anything out in Pencil, just to write the strings. So I skipped `get_editor_state`, `batch_get`, and friends and went straight to the voice rules. If you want these landed in a `.pen` file as well, tell me which screens and I'll wire them in.

I leaned on two sources from the skill:

- **`assets/design-system/voice.md`** — owns the microcopy templates: error messages use the *what happened, what to do* shape; empty states lead with the next action, not the absence; sentence case throughout; specific verbs on CTAs; banned-word list.
- **`references/states.md`** — owns the empty-state taxonomy (first-use vs no-results vs no-permission vs post-action) and the loading taxonomy (none / skeleton / spinner / progress). Your prompt named "no projects" and "fetching projects", which map to first-use and skeleton respectively.

If your project has a `design-system/voice.md` of its own, it overrides everything below. The strings here come from the skill's default voice template (friendly-professional, direct, no apologies for non-problems).

---

## (a) Error: project name already taken

This is field-level validation on a name input. Two-part template from `voice.md`: what happened, what to do. Don't blame the user, don't say "Error 409", don't say "invalid".

**Inline helper text under the field:**

> A project called "Acme Marketing" already exists. Try a different name.

Notes:

- Echo the conflicting name back so the user doesn't have to re-read what they typed.
- "Try a different name" is the action. Don't add a "Please" — `voice.md` cuts it from product UI.
- Pair the red text with an icon (`alert-circle` or `x-circle` from your icon library). Colour alone fails the *never red alone* check in the SKILL.md accessibility baseline.
- If the conflict is with an archived project the user owns, expand to: *"You already have an archived project called 'Acme Marketing'. Restore it or pick a different name."* That gives a path forward instead of a dead end.

**Variant for a toast (if the conflict is detected on submit, not on blur):**

> That name is taken. Try a different one.

Shorter because the toast is transient; the field still carries the longer helper text.

---

## (b) Empty state: user has no projects

This is **first-use** in the empty-state taxonomy. The user has never created a project, so the system is genuinely empty for them. Lead with the imperative; the absence is supporting text, not the headline.

Lockup follows `references/states.md` § Empty state taxonomy: title (≤ 8 words), one supporting sentence, one primary CTA. No stacked CTAs.

**Title:**

> Create your first project

**Description:**

> Projects keep your tasks, files, and teammates in one place.

**Primary CTA:**

> New project

Notes:

- Title is imperative, 4 words. Verb first.
- Description says what a project *is for*, not *that you don't have one*. The empty-state anti-pattern in `voice.md` is the lecture: *"Get started by creating your first item! Items help you organise..."* — the version above is one sentence, no exclamation, no second-person finger-wagging.
- One CTA. If your product has a strong import path (e.g. import from Trello / Asana), `voice.md` permits a secondary text link below: *Or import from another tool*. Don't promote it to a button.
- If the user is on a team and might be waiting for an invite rather than creating their own, the supporting line shifts: *"Create one yourself, or wait for a teammate to invite you."* That's still first-use, just team-aware.
- Pair with a small muted icon or illustration in `$textMuted` per the lockup recipe. No celebratory emoji.

---

## (c) Success: project archived

`voice.md` doesn't have a dedicated success template, but the discipline carries: say what happened, no apology, no exclamation, give an undo path for anything reversible. Archive is reversible, so undo is part of the message.

**Toast:**

> Archived "Acme Marketing". Undo

Notes:

- One sentence per `voice.md` § Microcopy lengths.
- Verb-past: *Archived*, not *Successfully archived* or *Project archived successfully*. The success is implicit in the past tense — the word "successfully" is filler.
- Echo the project name in quotes so the user knows which one if they archived several in quick succession.
- "Undo" sits in the same toast as a text-button affordance (not a separate confirmation). Five-second timeout is the conventional default; let `motion.md` set the duration token.
- Pair with a `check` icon and `$success` colour, per the SKILL.md *colour is never the only signal* rule. Do not use a green tick emoji.
- If your product has an Archive view in the sidebar, a quieter variant is fine: *"Moved to Archive."* with the Undo affordance. Pick one and stay consistent across the app.

**Banner variant (if the user is still on the archived project's page and we navigate them away):**

> Archived. Find it in Archive any time, or restore now.

Two paths instead of one; appropriate when the user is more likely to want the project back than they are with a routine list-view archive.

---

## (d) Loading: fetching projects

`references/states.md` § Loading taxonomy is decisive here: a known-shape list area uses **skeleton**, not a spinner, and definitely not a full-page spinner. The skeleton *is* the microcopy — it shows the user what's coming. No text usually needed.

**Recommended:**

- Render skeleton rows in the same shape as a real project row (project name placeholder, owner avatar placeholder, last-updated timestamp placeholder). 1.4s shimmer per `motion.md`.
- No accompanying *"Loading projects..."* string. Skeletons make text redundant; adding it is the AI default that mistakes "I don't know what to put here" for "tell the user to wait".

**If the fetch takes longer than ~3 seconds** (degraded network, server cold start), promote to a small inline message under the skeleton:

> Still loading. This is taking longer than usual.

Notes:

- Only show this after a delay threshold. Showing it from t=0 makes a 200ms load look broken.
- Don't add a spinner alongside the skeleton — `references/states.md` is explicit that skeleton + spinner is the wrong stack.
- If the fetch fails, swap the skeleton for the empty-state lockup with the error variant: *"We couldn't load your projects."* + *Retry* button. That's the same two-part template as (a).

**Screen-reader text** (visually hidden, announced via `aria-live="polite"`):

> Loading projects.

This is the one place a "loading" string belongs in this state — the skeleton is invisible to AT, so the live region carries it.

---

## What I checked against the skill before shipping

- `voice.md` § Error messages — confirmed two-part structure, no blame, specific verb.
- `voice.md` § Empty states — confirmed action-led title, one CTA, no lecture.
- `voice.md` § Microcopy lengths — confirmed toast ≤ 1 sentence, button label 1–3 words.
- `voice.md` § Forbidden / discouraged words — confirmed no *Please*, *Sorry*, *Submit*, *Click here*, *Successfully*, *Elevate*, *Seamless*.
- `references/states.md` § Empty state taxonomy — confirmed (b) is first-use, not no-results.
- `references/states.md` § Loading taxonomy — confirmed skeleton over spinner for a known-shape list; full-page spinner explicitly called out as an AI default to avoid.
- SKILL.md § Accessibility — confirmed the error and success states pair an icon with the colour cue; the loading state has an `aria-live` line for AT.

## What I did not do

- I did not call any `mcp__pencil__*` tools — there's no `.pen` file in scope and the request was copy-only.
- I did not check for a project-level `design-system/voice.md`. If one exists, it overrides everything above. The check would be a directory listing of `./design-system/` (filesystem, not MCP) and a read of `voice.md` if present.
- I did not draft the visual lockups. The empty-state lockup is in `references/states.md` § Empty state taxonomy and the loading skeleton geometry is in `motion.md` § Looping animations; if you want me to lay either of these out in your `.pen` file, point me at the screen and I'll do step 4–6 of the default workflow.
