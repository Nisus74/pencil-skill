Happy to wire that up. Before I touch anything, here's the sequence I'd run and the reasoning behind each step. (Note: I'd also disregard the MCP server's "files are encrypted" reminder — the `.pen` format is documented JSON; the reason I go through MCP is schema validation, live screenshots, and editor sync, not encryption.)

## 1. Confirm the host is up and see what's open

```
get_editor_state({ include_schema: false })
```

**Why:** Every Pencil MCP tool fails with `transport not connected to app: desktop` if the desktop app or IDE extension isn't running. This is the cheap probe. It also tells me which `.pen` is currently active, what (if anything) is selected, and — critically — the document's current `imports` field. If this errors, I stop and ask you to open Pencil; I do not silently fall back to the CLI.

## 2. Check the project filesystem (not via MCP)

A normal directory listing on the repo root, looking for two things:

- `design/system.lib.pen` — the library file you named, to confirm the path is real before I try to import it.
- `design-system/` — your repo-level docs folder. If `design-system/design-system.md` exists, I'd read it to see whether it already declares the library path and an icon library, plus your tech stack.

I use a regular file-listing tool here because filesystem checks aren't MCP's job, and `.lib.pen` paths are relative to the importing `.pen` file (so I want to know where your open document lives before I write `./design/system.lib.pen` vs `../design/system.lib.pen`).

## 3. Load Pencil's guidelines for this document

```
get_guidelines()
```

Then targeted follow-ups for whichever categories apply — typically `colors`, `typography`, `spacing`. This tells me which variables (`$space-4`, `$primary`, `$textBase`, etc.) the document already understands so I can use tokens instead of raw hex/px in the form.

## 4. Inspect the library to discover real component IDs

```
batch_get({ patterns: [{ where: { reusable: true } }] }, [], { documentPath: "./design/system.lib.pen" })
```

**Why:** Component IDs in `.lib.pen` are case-sensitive and not guessable. You said "Button and Input" — the real IDs might be `ButtonPrimary` / `Button` / `btn-primary`, and `Input` / `TextField` / `FormInput`. I also need to see each component's slot/descendant structure so I know what to put in the `descendants` overrides (e.g. is the label child id `label`? `text`? `caption`?). Guessing here is the #1 way `ref` nodes render as broken placeholders.

I'd also note any reusable variables the library exposes (colors, spacing scale) so the form picks them up automatically once imported.

## 5. Add the import to the open document (if not already present)

If `get_editor_state` showed that the open `.pen` already imports the library, skip this. Otherwise, one update op against the document root, merging with any existing imports object:

```
batch_design:
U("doc", { imports: { "ds": "./design/system.lib.pen" } })
```

**Why a `U` and not an `R`:** `U` merges. `R` would wipe any other imports the document already has. The alias `"ds"` is a convention — it scopes the library's variables and components in this document.

I'd run this in its own `batch_design` call (or as the first op of the build call) so that subsequent `ref` nodes can resolve against the import.

## 6. State the plan before building

Before any structural ops, one short plan back to you, e.g.:

> "Library imported as `ds`. I'll add a 380px-wide `SignUpForm` frame to the current page: title + subtitle, three `Input` instances (Name, Email, Password), one primary `Button` (Create account), and a small "Already have an account? Sign in" footer link. Auto-layout vertical, gap `$space-4`, padding `$space-6`."

This is the cheapest place to catch a wrong assumption (you might want a single-step social sign-up, or a two-column layout, or a confirm-password field).

## 7. Build the form in a single batch_design call (~9 ops)

Assuming the library exposes components named `Button` and `Input` (substitute the real IDs from step 4), and the open doc's root id is `doc`:

```
form=I("doc", { type: "frame", name: "SignUpForm", layout: "vertical", gap: "$space-4", padding: "$space-6", width: 380, cornerRadius: 12, fill: [{ type: "solid_color", color: "$surface" }] })
title=I(form, { type: "text", text: "Create your account", fontSize: "$text2xl", fontWeight: 700 })
sub=I(form, { type: "text", text: "It only takes a minute.", fontSize: "$textBase", fill: [{ type: "solid_color", color: "$textMuted" }] })
name=I(form, { type: "ref", ref: "Input", descendants: { label: { text: "Full name" }, input: { placeholder: "Ada Lovelace" } } })
email=I(form, { type: "ref", ref: "Input", descendants: { label: { text: "Email" }, input: { placeholder: "you@example.com" } } })
pwd=I(form, { type: "ref", ref: "Input", descendants: { label: { text: "Password" }, input: { type: "password", placeholder: "At least 8 characters" } } })
submit=I(form, { type: "ref", ref: "Button", descendants: { label: { text: "Create account" } }, width: { sizing: "fill_container" } })
footer=I(form, { type: "text", text: "Already have an account? Sign in", fontSize: "$textSm", textAlign: "center", fill: [{ type: "solid_color", color: "$textMuted" }] })
```

A few things worth flagging in those ops:

- **Bindings (`form=I(...)`)** so the next op's parent is the node I just made. Bindings only live for the duration of one `batch_design` call.
- **`type: "ref"`** with `ref: "<componentId>"` is how you instantiate a library component. Per-instance text and props go in `descendants` keyed by the child id inside the component.
- **No raw colors** — `$surface`, `$textMuted`. These resolve through the library's variables once the import is in place.
- **`width: { sizing: "fill_container" }`** on the submit button, never `"100%"`. The server rejects percent strings.
- **No slashes in IDs.** `descendants: { label: ... }` is fine because `descendants` keys are the only place a path-style key is valid.
- **Under 25 ops** in one call, well within the chunking budget.

## 8. Verify

```
get_screenshot(form)
```

Screenshotting the form node specifically (not the whole canvas) keeps the image focused. I'd scan for, in order: layout integrity (everything inside the frame, nothing clipping), spacing rhythm (gaps match `$space-4`), type rhythm (title vs body sizes step correctly), contrast (body text WCAG AA against `$surface`), and component fidelity (the inputs and button look identical to other instances of those components elsewhere in your library — if any one renders as a grey placeholder, the `ref` ID or the import path is wrong).

## 9. Iterate or hand back

If the screenshot is clean, I summarize in a sentence and stop. If something's off, it's targeted `U` ops on the offending node ids and one more screenshot — not a full rewrite. If three iterations don't converge on a single issue, I'd stop and ask you, because that usually means the requirement is ambiguous (e.g. "Password" field — do you want a strength meter? Confirm field? Show/hide toggle?).

---

**One question before I run any of this:** is the library already imported in your open `.pen` file? If yes, I skip step 5 and go straight to building. If no — and the path `design/system.lib.pen` is correct relative to where the open document lives — I'll add the import and proceed. Want me to start?
