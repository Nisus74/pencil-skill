# Project tracker microcopy — four states

Before the copy, a quick note on what I leaned on and what I assumed.

## References consulted

- `references/microcopy.md` — primary. Owns the shape of every state below: voice and tone framework, action-specific CTA pattern, the three-part error message anatomy (what happened / why / what to do), the empty-state "show what's possible, lead with the action, one CTA" rule, the success-copy stakes calibration, and the loading-copy "name what's loading, vary across loads" rule.
- `references/states.md` — secondary. Owns the empty-state taxonomy (this is a *first-use* empty, not a *no-results* empty — different copy lead, different CTA), the success-copy stakes ladder (archive is a "significant action" → quiet toast, not a celebration), and the loading taxonomy (skeleton vs spinner vs progress vs none — fetching a list is the textbook skeleton case, with copy attached only if the skeleton needs it).
- `assets/design-system/voice.md` (template, since I had no project copy of it to read) — confirmed the two-part error template (*what happened. what to do.*), sentence case for buttons and titles, the forbidden-words list (`Submit`, `Please`, `Sorry` for non-errors), and length budgets (button labels 1–3 words, toast 1 sentence, empty state title ≤ 8 words).

## Assumptions

The prompt didn't name the product, the audience, or a tone. Real session, I'd check `design-system/voice.md` first. With no project to defer to, I'm assuming a friendly-professional B2B SaaS register (the centre of the three voice axes in microcopy.md — friendly, serious, calm) and sentence case throughout, since that's the template default. If your `voice.md` calibrates differently — playful consumer, clinical enterprise, or title case for buttons — swap the wording but keep the structure.

I'd also normally call `mcp__pencil__get_editor_state({ include_schema: false })` first to confirm the MCP host is connected, then `mcp__pencil__batch_get` against the open `.pen` to see the existing component instances these strings are filling (slot copy lives in `descendants` overrides on `ref` nodes; default copy lives on the component children themselves). For pure copy, I don't need the screenshot; I'd verify by reading the updated nodes back via `batch_get`.

---

## (a) Error: project name already taken

This is form-validation copy that fires inline, next to the field, on submit (or on blur if you validate then). Per microcopy.md § Error messages, the message has to do three things: state what happened, hint why if non-obvious, and tell the user what to do next. Per voice.md, it's a two-part template — *what happened. what to do.* Don't blame the user; show them the path forward.

**Primary (inline field error):**

> A project named "Atlas Migration" already exists. Try a different name, or open the existing one.

The name is quoted back at the user so they don't have to scan the field to remember what they typed. Two paths forward — rename, or jump to the existing project — because in practice the second one is what they actually want about half the time (they forgot they'd already started it). If your form doesn't link to the existing project, drop the second clause.

**Shorter variant (if space is tight, e.g. mobile inline):**

> "Atlas Migration" is already taken. Try another name.

**Avoid:**

- *"Error: project name must be unique."* — system-speaking-to-itself, no path forward.
- *"You entered a duplicate name."* — blames the user.
- *"Something went wrong."* — generic; tells the user nothing.
- *"Please choose a different name."* — `Please` is on voice.md's forbidden list for product UI. Just say what to do.

**Visual treatment** (out of scope for this prompt, but noted so the copy lands right): icon + colour, never colour alone (states.md § Component states). Border `$danger`, `alert-circle` icon, helper text in `$danger` below the field. The focus ring wins if the field is also focused.

---

## (b) Empty state: user has no projects yet

This is a *first-use* empty state per states.md § Empty state taxonomy — the user has never created a project, the system is genuinely empty for them. Different copy and CTA from a *no-results* empty (filter returned nothing) or *post-action* empty (they archived everything).

Per microcopy.md § Empty state copy: show what's possible, lead with the action, one CTA. Per states.md, the lockup is illustration/icon → title (≤ 8 words) → 1–2 line description → primary CTA.

**Title (≤ 8 words, imperative):**

> Start your first project

**Description (1–2 sentences, what projects unlock):**

> Projects are where your team plans work, tracks progress, and shares updates. Create one to bring everything together.

**Primary CTA:**

> New project

**Optional secondary** (only if you have a strong import path — e.g. CSV from another tracker, JSON export from Trello/Asana/Linear):

> Or import from another tool

That goes as a text link below the primary, not a second equal-weight button. States.md is explicit: don't stack three competing CTAs in a first-use empty.

**Avoid:**

- *"No projects yet."* — frames the empty as a deficit. Make it a beginning.
- *"Get started by creating your first project! Projects help you organise your work and..."* — lectures. Cut to the action.
- *"You don't have any projects."* — same problem; passive and a little glum.
- Three buttons (*Create*, *Import*, *Explore demo*). Pick the one most users do first; demote the rest.

---

## (c) Success: project archived

Archive is a *significant* action per microcopy.md § Success copy — not routine (no toast needed for a save), not high-stakes (no full-screen confirmation needed). Significant gets a brief toast, dismiss-on-click, with an undo affordance because archive is recoverable and people misclick.

The voice stays calm, not celebratory. *"Archived"* is normal product work; *"Awesome! Project archived!"* reads as condescending.

**Primary toast:**

> "Atlas Migration" archived. **Undo**

The project name is quoted back so the user knows which one (matters when they archive several in a row). `Undo` is the action — placed inline, not as a second toast — and stays clickable for ~5 seconds before the toast dismisses.

**If your toast component doesn't support inline actions:**

> "Atlas Migration" archived. You can restore it from Archived projects.

Tells the user where the project went, so they don't think they've lost it.

**Optional follow-up** (microcopy.md § Success copy: tell the user what happens next — relevant when archive empties their list):

> All projects archived. Start a new one when you're ready.

That's the *post-action* empty state copy from states.md § Empty state taxonomy — acknowledging, not pushing for more work.

**Avoid:**

- *"Awesome! Your project has been successfully archived!"* — over-celebration, three problems in one sentence.
- *"Project archived."* — fine, but loses the project name and the undo path.
- *"Successfully archived."* — `Successfully` is filler; the absence of an error is the success signal.
- A modal confirmation after the action. The confirmation goes *before* the action, not after.

---

## (d) Loading: fetching projects

Per states.md § Loading taxonomy, fetching a list of known shape is the textbook skeleton case — not a spinner. The skeleton placeholder approximates the rows so the layout doesn't jump when the data arrives. A skeleton on a list almost always carries no copy at all; the silhouette does the work.

**Primary recommendation: skeleton, no copy.**

The skeleton is the message. A spinner sitting on top of a skeleton is the doubled-up loading state states.md flags as wrong.

**If your skeleton needs an accessible label** (screen-reader announcement while the region is busy — `aria-busy="true"` paired with `aria-live="polite"`):

> Loading your projects

That string is read once, then the screen reader reads the list when it appears. Keep it visually hidden (`sr-only`); the sighted user gets the skeleton.

**If your team has decided against skeletons and wants a spinner with copy** (states.md § Loading taxonomy: spinners are for inline actions of unknown shape, not for known-shape lists — but if you've made the call):

> Fetching your projects

Per microcopy.md § Loading copy: name what's loading, don't ship `Loading...` as the global default. *"Fetching your projects"* tells the user the operation; *"Loading..."* tells them nothing.

**Vary the copy across loading surfaces in the product**, per microcopy.md anti-patterns. If every async region in your tracker says `Loading...`, that's a tell the copy was an afterthought. Examples:

- Project list: *Fetching your projects*
- Project detail: *Opening "Atlas Migration"*
- Search: *Searching projects*
- Settings: *Loading workspace settings*

**Timing rules** (out of scope for this prompt but the copy lands wrong without them — see `references/interactions.md` § Loading states): don't show the spinner before 150–300ms; once shown, keep it visible 300–500ms minimum or it flashes and reads as broken.

**Avoid:**

- *"Loading..."* — the AI default. Vary by operation.
- *"Please wait while we load your projects..."* — `Please` and `wait` are both filler. Cut both.
- A full-page spinner over content the user can already see (e.g. the page chrome). Skeleton the empty region only.
- A spinner *and* a skeleton at the same time. Pick one.

---

## Summary

| State | Pattern | Key principle |
|-------|---------|---------------|
| Error: name taken | Inline field error, two parts | What happened (named) + path forward (rename or open existing). Quote the name back. Don't blame. |
| Empty: no projects | First-use empty lockup | Imperative title, one description sentence, one CTA. Show what's possible, not what's missing. |
| Success: archived | Brief toast with undo | Significant-action calibration. Calm voice. Name the project. Surface the recovery path. |
| Loading: fetching | Skeleton, copy optional | Right shape for known-shape lists. If copy is needed, name the operation. Vary across the product. |

Written file confirmed at `/Users/travis/Development/open-source/pencil-dev-skill/skills/pencil-design-workspace/iteration-1/eval-13-microcopy-quality/with_skill/outputs/response.md`.
