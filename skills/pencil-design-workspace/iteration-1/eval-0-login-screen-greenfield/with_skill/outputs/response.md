Happy to walk you through it before I run anything. Here's the sequence I'd follow, why each step matters, and where I'd pause for your input.

## 1. Detect the Pencil host

First call would be:

```
get_editor_state({ include_schema: false })
```

This pings the Pencil MCP server to confirm it's reachable through a host (the desktop app, an IDE extension, or `pencil interactive`). If this errors with something like `transport not connected to app: desktop`, I stop and ask you to open the Pencil desktop app or the Pencil IDE extension — every other tool fails until a host is up. I won't silently fall back to the CLI.

Assuming it succeeds, the response tells me three things I need: which `.pen` file is open (if any), what's currently selected, and which schema version the document declares.

## 2. Locate context

From that result plus a quick filesystem check, I figure out:

- Is a `.pen` file already open, or do I need to create/open one?
- Is anything selected (which would suggest you want me to work in-place)?
- Does the project root have a `design-system/` folder?

Three branches here:

- **No `.pen` open.** I'd ask whether you want me to open an existing file (give me the path) or create a new one with `open_document("new")`. I won't guess.
- **`design-system/` exists with markdown docs.** Great — I'll read it in step 3.
- **`design-system/` doesn't exist.** A login screen sounds like real project work, not a throwaway sketch, so I'd offer once to scaffold the seven template files (README, design-system, tokens, components, layout, voice, code-export). If you decline, I proceed without and won't ask again this session.
- **`design-system/` exists but contains code (e.g. `.tsx`, `package.json`).** I won't overwrite — I'd ask where to put the docs instead (`design-system/docs/`, `docs/design-system/`, `.pencil/design-system/`, or a path you pick).

## 3. Load guidelines

Two parallel sources:

- `get_guidelines()` with no arguments — the server reports which categories exist for this document. For a login screen I'd read `colors`, `typography`, and `spacing` at minimum.
- `design-system/README.md` first, then the files it points at. For this task that's almost certainly `design-system.md` (to find your `.lib.pen` path, tech stack, and icon library) and `tokens.md` (to know which color/spacing/type tokens to reach for).

I also check the open document's `imports` field. If `design-system.md` names a library like `./design/system.lib.pen` and the doc doesn't import it yet, I'll add the import via a `U` op on the document root before instantiating components. If the library file doesn't exist at the declared path, I tell you the path is stale rather than inventing one.

If a library is imported, I'd `batch_get` the reusable components (Input, Button, LinkText, etc.) so I instantiate them by id rather than rebuilding primitives.

## 4. State the plan back to you

Before any `batch_design` call, I'd give you a 2–3 sentence plan so we catch bad assumptions cheaply. For your prompt my draft plan is:

> Centered single-column login at 1440×900. A ~360px-wide form card with title ("Sign in"), short subtitle, an email Input and a password Input (instances of your library's `Input` component if present), a primary submit Button as a `ref`, and a "Forgot password?" link beneath it. Colors and spacing pull from your tokens; the library import is added if missing.

Open questions I'd flag at this point if relevant:
- Brand mark / logo above the title? (Default: no, unless `design-system/` says otherwise.)
- "Sign up" link or social-auth buttons? You didn't ask for them, so I'd leave them out.
- Layout pattern: simple centered card vs. split-screen with hero. You didn't specify, so I default to centered card — quickest, most conventional, easiest to evolve.

If you'd shown me a reference image, I'd name the layout pattern out loud first ("split-screen, hero left / form right") before planning the tree — the model produces visibly better designs when it labels the pattern explicitly.

## 4.5. Open the document if needed

If step 2 found no open `.pen`, after your go-ahead:

```
open_document("new")
```

Then re-read editor state to grab the new document root id.

## 5. First `batch_design` — skeleton + components

One call, well under 25 ops. Roughly:

1. `U(doc, { imports: { "ds": "./design/system.lib.pen" } })` — only if the import is missing.
2. `page=I(doc, { type: "frame", name: "LoginPage", layout: "vertical", justifyContent: "center", alignItems: "center", width: 1440, height: 900, fill: [{ type: "solid_color", color: "$surface" }] })`
3. `form=I(page, { type: "frame", name: "Form", layout: "vertical", gap: "$space-4", padding: "$space-6", width: 360, cornerRadius: 12, fill: [{ type: "solid_color", color: "$surfaceMuted" }], stroke: { ... } })`
4. `title=I(form, { type: "text", text: "Sign in", fontSize: "$text2xl", fontWeight: 700 })`
5. `sub=I(form, { type: "text", text: "Welcome back. Enter your details below.", fontSize: "$textBase", fill: [{ type: "solid_color", color: "$textMuted" }] })`
6. `email=I(form, { type: "ref", ref: "Input", descendants: { label: { text: "Email" }, input: { placeholder: "you@example.com" } } })`
7. `pwd=I(form, { type: "ref", ref: "Input", descendants: { label: { text: "Password" }, input: { type: "password", placeholder: "••••••••" } } })`
8. `submit=I(form, { type: "ref", ref: "ButtonPrimary", descendants: { label: { text: "Sign in" } } })`
9. `forgot=I(form, { type: "ref", ref: "LinkText", descendants: { label: { text: "Forgot password?" } } })`

Notes on grammar I'm being deliberate about:
- The `foo=I(...)` binding form so later ops can reference nodes I just created in the same call (no hardcoded ids).
- `width: { sizing: "fill_container" }` / `"fit_content"` rather than `"100%"` or `"auto"` where I want flexible sizing.
- `"$variableName"` color references (e.g. `$surface`, `$textMuted`) over raw hex, so the design respects your theme axes.
- No `/` characters in any id — the server rejects them.

If your project doesn't have a `.lib.pen` with `Input`/`ButtonPrimary`/`LinkText`, I'd build those out of primitives (frame + text + input nodes) instead of using `ref`s. I'd also note that as soon as a project has more than one `.pen`, those components belong in a `.lib.pen` — but I won't create one prematurely for a one-off.

## 6. Verify with `get_screenshot()`

The JSON tells me structure, not aesthetics — the screenshot is my eyes. After that first batch I'd scan the rendered image, in this order:

1. **Layout integrity** — is the form actually centered, on-canvas, sized as expected?
2. **Spacing rhythm** — gaps match `tokens.md`?
3. **Type rhythm** — title/subtitle/body step in the order tokens declare?
4. **Contrast** — body text passes WCAG AA (4.5:1) against the card fill; submit button passes against its own fill?
5. **Component fidelity** — inputs and button look like instances of your library, not hand-built lookalikes?

## 7. Iterate or report

If something's off, I fix it with targeted `U` (partial update) or `R` (full replace) ops on the offending node, screenshot again, move on. If the same issue won't converge after three iterations, I stop and ask you — that usually means the requirement is ambiguous.

When it's clean, I hand back a one-paragraph summary of what landed (frame name, dimensions, which library components were instantiated, which tokens were used, any iterations) and stop. I won't keep polishing past what you asked for.

---

Want me to go ahead and run step 1 to check the host, or do you want to adjust the plan first (logo? split-screen instead of centered card? brand colors I should know about)?
