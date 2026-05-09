# Login screen in Pencil — my walkthrough before touching tools

Good prompt. Before I open anything, here's the seven-step plan I'd run, the tools I'd call, the args I'd pass, and what I'd be checking for at each rung. I worked from the `pencil-design` SKILL.md (default workflow + discipline rules + form notes), pulled `references/forms.md` for input mechanics and `assets/examples/example-login-screen.md` as a structural template, and skimmed `references/mcp-tools.md` for the exact call shapes.

---

## Step 1 — Detect host

First call, every task:

```
get_editor_state({ include_schema: false })
```

What I expect back: an object naming the active document path (or `null`), the current selection, and the schema version of whatever is open. If it errors with `transport not connected to app: desktop` I stop immediately and tell you to open the Pencil desktop app or the IDE extension. I do not silently fall back to the CLI — that's policy, not preference.

If it succeeds I note three things from the response: (a) is a `.pen` open, (b) is anything selected, (c) what's the schema version. For a greenfield login this almost always returns "no active document" — that's not an error, it's a branch.

## Step 2 — Locate context

I check three things in parallel:

1. From `get_editor_state`: any document open? Anything selected? Most likely no, since you said "design a login screen" rather than "edit this".
2. From the project filesystem (regular `ls`, not the MCP): does `./design-system/` exist? If yes I'll read it next; if not I'll offer once to scaffold it (12 core templates plus optional ones for mobile, data-viz, brand, imagery — your call). On a "no" I proceed without and don't ask again this session.
3. Whether there's a `.lib.pen` library mentioned anywhere — usually named in `design-system/design-system.md`.

These three facts shape every decision after. A login screen with a populated `design-system/` and a library is a very different task from a login screen on a blank repo.

## Step 3 — Load guidelines and inventory components

Two parallel reads.

**Guidelines.** First I call `get_guidelines()` with no args to see which categories the server reports for this document. Then I load whichever fit — for an auth screen that's typically `Web App` (form on a product surface) and `Tailwind` if your stack matches. I'd skip `Landing Page` and `Mobile App` unless you tell me this login lives on a marketing site or a native target.

```
get_guidelines()
get_guidelines({ category: "Web App" })
```

**Local docs.** If `design-system/README.md` exists I read it first, then `design-system.md` (for stack, library path, icon library) and `tokens.md` (for spacing/type tokens I'll bind against). These authoritatively beat my defaults.

**Component inventory.** This is the components-first discipline rule — I never build a button from primitives if a Button component exists. I scan the open document and any imported library:

```
batch_get({ patterns: [{ reusable: true }], readDepth: 2 })
batch_get({ filePath: "./design/system.lib.pen", patterns: [{ reusable: true }], readDepth: 2 })
```

I'm specifically hunting for `Input`, `ButtonPrimary` (or `Button` with a primary variant), and `LinkText` (or whatever the project calls them). The response gives me each component's `id`, `type`, top-level `children` (those become valid `descendants` keys), `slot` markers, and `theme` axes (the component's state matrix).

If I find an unfamiliar component I'd inspect deeper before instantiating:

```
batch_get({ nodeIds: ["Input"], readDepth: 4 })
```

That tells me which children I can override per instance — typically a `label` text node and an `input` field where `placeholder`, `type`, and `inputmode` live.

If you have no library, I build the inputs and button inline as primitives and surface a question at the end: *"This button pattern is reusable — want me to extract it to a `.lib.pen`?"* I do not invent a library on your behalf without asking.

## Step 4 — Plan, out loud, before any write op

Before any `batch_design` call I commit to a plan and an atmosphere in 2–3 sentences. For a login screen my default would be something like:

> *"Centred single-column login screen at desktop 1440 × 900: a 360px-wide `LoginCard` with a heading, a one-line subtitle, an `EmailField`, a `PasswordField`, a primary `SubmitButton` labelled 'Sign in', and a 'Forgot password?' link below. Atmosphere: balanced / symmetric / static. I'll instantiate `Input`, `ButtonPrimary`, and `LinkText` from your library; surface and text colours bind to your existing tokens."*

The atmosphere line (one adjective each from density / variance / motion) forces a stance the rest of the design has to honour. Without it the model defaults to *balanced / symmetric / fluid* for everything and the result reads generic.

I also commit at this step to:

- **Naming.** Every node gets a PascalCase, role-bearing name: `LoginCard`, `EmailField`, `EmailLabel`, `EmailInput`, `PasswordField`, `PasswordLabel`, `PasswordInput`, `SubmitButton`, `ForgotPasswordLink`. No `Frame 1`, no `wrapper`.
- **Context strings.** Every non-trivial node gets a `context` documenting intent and behaviour the visual can't carry. For the form: *"Sign-in form. Submit on Enter from any field. Idempotency key required server-side. On success, redirect to `/dashboard`."* For the email input: *"Type: email. Inputmode: email. Autocomplete: email. Autocapitalize: none. Spellcheck: false."* For the password: *"Type: password. Autocomplete: current-password. Autocapitalize: none. Spellcheck: false."* These come from `references/forms.md` § Input attributes — they're the difference between a form that works with password managers and one that doesn't.
- **Themes.** I'll call `get_variables()` first. If the document already has light + dark tokens, I bind to them and skip bootstrapping. If it's genuinely empty, I'll declare a `mode` axis and `set_variables` with the absent tokens only — never re-declaring anything that already exists, because `set_variables` with `replace: false` still overwrites by key.
- **Responsive.** I'd ask whether you want one frame (`LoginPage_Desktop` at 1440 × 900) or three siblings (`Desktop`, `Tablet`, `Mobile`). For a login the per-breakpoint pattern is overkill since the form barely shifts; I'd default to one fluid frame and only split if you tell me otherwise.
- **Empty-canvas placement.** If the canvas already has top-level frames, I call `find_empty_space_on_canvas({ width: 1440, height: 900, padding: 80, direction: "right" })` first and pass the returned `x`/`y` on my outermost frame. Skipping this on a populated canvas produces invisible overlaps that look like rendering bugs.

Then I share the plan with you and wait for any pushback before writing.

## Step 4.5 — Open the document if needed

If no `.pen` is open I ask whether to open an existing one (path?) or create a new one. For greenfield:

```
open_document({ path: "new" })
```

The server returns a fresh document root id (let's call it `doc`).

## Step 5 — Execute, one batch_design call

For a login screen this comfortably fits in a single call under the 25-op cap. The shape would look like:

```
U("doc", { themes: { mode: ["light","dark"] } })             # only if not already declared
U("doc", { imports: { "ds": "./design/system.lib.pen" } })   # only if library exists and isn't imported
page=I("doc", { type: "frame", name: "LoginPage", context: "Auth surface root. Centres LoginCard.", layout: "vertical", justifyContent: "center", alignItems: "center", padding: "$space-8", width: 1440, height: 900, fill: [{ type: "solid_color", color: "$surface" }] })
card=I(page, { type: "frame", name: "LoginCard", context: "Sign-in card. 360px column.", layout: "vertical", gap: "$space-4", padding: "$space-6", width: 360, cornerRadius: 12, fill: "$surfaceMuted", stroke: { thickness: 1, fill: "$border" } })
title=I(card, { type: "text", name: "Heading", text: "Sign in", fontSize: "$text2xl", fontWeight: 700 })
sub=I(card, { type: "text", name: "Subheading", text: "Welcome back. Enter your details below.", fontSize: "$textBase", fill: [{ type: "solid_color", color: "$textMuted" }] })
email=I(card, { type: "ref", ref: "Input", name: "EmailField", context: "Email input. Type: email. Inputmode: email. Autocomplete: email. Autocapitalize: none. Spellcheck: false.", descendants: { label: { text: "Email" }, input: { placeholder: "you@example.com" } } })
pwd=I(card, { type: "ref", ref: "Input", name: "PasswordField", context: "Password. Type: password. Autocomplete: current-password.", descendants: { label: { text: "Password" }, input: { type: "password", placeholder: "" } } })
submit=I(card, { type: "ref", ref: "ButtonPrimary", name: "SubmitButton", context: "Primary submit. On press: disable, show spinner alongside label 'Sign in', server idempotency required.", descendants: { label: { text: "Sign in" } } })
forgot=I(card, { type: "ref", ref: "LinkText", name: "ForgotPasswordLink", context: "Navigates to password reset.", descendants: { label: { text: "Forgot password?" } } })
```

A few rules I'd be honouring throughout:

- `foo=I(parent, {...})` binding form so later ops can reference nodes I just made — never hardcode a fresh id within the same call.
- `width: "fill_container"` / `"fit_content"` as bare strings, not `"100%"`, not the older `{ sizing: ... }` object form.
- Colour bindings use `"$variable"` over raw hex — and I avoid pure `#000000` / `#FFFFFF`, since those bound directly are an AI tell.
- IDs cannot contain `/`. Names can.
- 25 ops max in one call. This one's around 10.

## Step 6 — Verify, structural-first

I walk the verification ladder and stop at the cheapest rung that answers the question.

**Rung 1 — `batch_design` response.** Did the ops land? Free, immediate. If anything errored I cross-reference `references/batch-design-grammar.md` and fix specifically — never blind retries.

**Rung 2 — `snapshot_layout`.** Default after any structural write:

```
snapshot_layout({ parentId: "page", maxDepth: 2 })
```

I'm checking: is the card 360 wide? Is it actually centred (not just `justifyContent` set)? Did the gap land at `$space-4`? On a fresh doc the most common surprise is `page` height collapsing because the document root constrains it — fix is `U("page", { height: "fill_container(900)" })`.

**Rung 3 — `batch_get`.** For property-level confirmation of the things `snapshot_layout` doesn't surface:

```
batch_get({ nodeIds: ["email", "pwd", "submit"] })
```

Specifically that `ref` nodes resolved to the right component, `descendants` overrides hit the right child ids, and colour bindings stayed as `$variable` rather than getting flattened to hex.

**Rung 4 — `get_screenshot`.** Only when the question genuinely needs pixels. For a login screen the relevant pixel question is: does the form sit at optical centre (typically 40–45% from top reads better on tall viewports than geometric 50%), does the contrast of muted subheading against the muted card surface still pass WCAG AA (4.5:1 body), does the link sit centred against the form's column. One screenshot, scoped to the card:

```
get_screenshot({ nodeId: "card" })
```

Not the page. Not the document. The card. Page-frame screenshots are roughly 5x the tokens of card screenshots and reveal nothing extra. Dual-mode rule: I screenshot the primary mode only. Variables guarantee the dark mode holds up; I'd only re-screenshot dark if I'd used a raw hex somewhere.

## Step 7 — Iterate or report

If the screenshot surfaces an issue (link off-centre, subheading too low contrast against muted surface, form sitting too low because geometric centre on a tall viewport reads as sinking), I issue a targeted `U` op, re-snapshot or re-screenshot the specific subtree, move on. Three iterations max on the same issue — if it doesn't converge, the requirement is ambiguous and I stop and ask.

Then I run the self-critique gate before declaring done:

1. Could a non-designer recognise this as your product's voice? If it could be any auth screen, I haven't committed.
2. Does the eye land on Sign in heading, then form fields, then forgot link in that order?
3. Anything decorative-only that doesn't communicate? Strip it.
4. What single change would make this feel less AI-generated?

And the form-specific verification checklist from `references/forms.md`: Enter submits, validate-on-blur not on-keystroke, errors land inline with focus moving to the first one, autocomplete attributes documented in context, mobile font-size at least 16px, hit zones at least 44x44 for touch.

Final report back to you would be one paragraph: what landed, where it sits, which library components got instantiated, anything I noted to follow up on (if I noticed a missing focus state on `ButtonPrimary` for instance, I'd flag it without fixing it — that's a library change, not a screen change).

---

## Things I'd ask you before step 4 if any of these aren't obvious

The skill flags an "open-ended request" branch when there's no reference image, no description of users, and no `design-system/`. For a login I'd usually only need to ask:

1. **Library?** Do you have a `.lib.pen` with `Input`, `Button`, `Link` components? If yes, where? If no, do I build them inline or extract afterwards?
2. **Breakpoint targets?** Desktop only, or do you want sibling Tablet/Mobile frames?
3. **Brand direction?** Any colour, typography, atmosphere words, or default to your `design-system/tokens.md`?
4. **OAuth?** Should there be a "Continue with Google/GitHub/SSO" row above the email input? Auth screens almost always grow this; cheaper to design once with the slot than retrofit.
5. **Sign-up link?** Most login screens need a "Don't have an account? Sign up" line below or beside the forgot-password link.

If your `design-system/` already answers any of these, I skip those questions.

## References I consulted (and why)

- `skills/pencil-design/SKILL.md` — the default seven-step workflow, the six discipline rules (naming, context, components-first, themes, responsive, accessibility), the verification ladder, the failure-mode table.
- `references/forms.md` — submit-on-Enter, label patterns, validation timing, the input-attribute list (`type`, `inputmode`, `autocomplete`, `autocapitalize`, `spellcheck`), submit-state choreography, the 12-point form verification checklist.
- `references/mcp-tools.md` — exact call signatures for `get_editor_state`, `get_guidelines`, `batch_get`, `set_variables`, `snapshot_layout`, `get_screenshot`, `find_empty_space_on_canvas`, plus the `get_guidelines` category decision table.
- `references/component-anatomy.md` (skim) — how to read a component from `batch_get`, identify `descendants` keys, fill slots, activate states.
- `assets/examples/example-login-screen.md` — the worked structural template I'd lean on for the `batch_design` shape, including the centring pattern and the `page` height fix.

I'd load the full `references/component-anatomy.md`, `references/states.md`, and `references/accessibility.md` if you wanted me to extend this into the full state matrix (default, hover, focus, loading, error per field, plus the form's submit-state choreography) — say the word.
