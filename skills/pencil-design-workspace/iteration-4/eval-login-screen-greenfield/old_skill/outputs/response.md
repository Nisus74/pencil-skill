Here is exactly what I would do before touching any tools — and why.

---

## Step 1: Detect host

The first thing I do on any Pencil task is ping the MCP server:

```
get_editor_state({ include_schema: false })
```

If that call fails with "transport not connected to app: desktop" or anything like a connection error, I stop entirely and tell you: *"Pencil's MCP server isn't reachable. Open the Pencil desktop app or the Pencil IDE extension, then ask me again."* I don't silently fall back to anything. This check is non-negotiable.

If it succeeds, I note three things from the result:
- Is a `.pen` file already open? What's its id? What schema version?
- Is anything selected (which could be a hint about where to place the new screen)?
- Are there any existing top-level frames on the canvas already?

If no `.pen` is open, I ask before proceeding: *"No `.pen` file is open. Should I (a) open an existing one — give me the path, or (b) create a new one with `open_document('new')`?"* I wait for the answer.

---

## Step 2: Locate context

With the editor state in hand, I check two more things without MCP tools:

1. Does this project have a `design-system/` folder at the repo root? I do a directory listing (not a file read). Three outcomes matter:
   - Exists with docs → I'll read `README.md` in step 3 and load what's relevant.
   - Doesn't exist + this looks like real project work → I offer once to scaffold it. If you say no, I proceed and don't ask again.
   - Exists but contains code files (`.tsx`, `package.json`, etc.) → I don't overwrite anything. I ask where to put docs instead.

2. Are there already multiple top-level frames on the canvas? If yes, I'll need to call `find_empty_space_on_canvas` in step 4 before placing anything, so the new frame doesn't invisibly overlap existing content.

---

## Step 3: Load guidelines and inventory components

This step has two distinct parts.

**Guidelines.** I call `get_guidelines()` with no arguments first — the server tells me which categories exist for this document. For a login screen, I'd load the `Web App` category at minimum, and `Tailwind` if the stack uses it. If the project has `design-system/README.md`, I read that next, then follow its pointers to `design-system.md` (for the library path and icon library) and `tokens.md` (for which color and spacing tokens to use).

**Component inventory.** Before planning a single node, I check whether components already exist that cover what you've asked for. I run:

```
batch_get({ patterns: [{ reusable: true }], readDepth: 2 })
```

against the open document. Then, for each `.lib.pen` listed in the document's `imports`, I run the same query with `filePath` pointing to that library file. I'm looking specifically for: an input/text-field component, a primary button component, and a link/text-link component.

If any of those exist, I use them — I never rebuild a button from a frame + text node when a `ButtonPrimary` component is sitting in the library. Using a component means a `ref` node with `descendants` overrides; it means the design updates automatically when the library updates. Building from primitives when a component exists is a maintenance bug I won't introduce.

If no components exist, I build from primitives and note that the resulting patterns look reusable — I'd surface the question of whether to add them to a `.lib.pen`.

---

## Step 4: Plan (stated to you before any batch_design call)

Before I touch a single tool that writes to the canvas, I state a plan in plain language. This is where I name my assumptions so you can catch them cheaply.

**Vibe / atmosphere.** Per the aesthetic defaults, I commit to a stance before designing anything. For a login screen specifically, I'd default to: *Balanced density, symmetric, static.* The layout is naturally centered and restrained — there's no reason to push toward airy or dense without a design-system brief telling me otherwise.

**Breakpoints.** A login screen is typically a desktop-first flow. Unless you've told me this is a mobile app, I'd design the primary frame at 1440 × 900 (desktop), with the login card centered in the frame. If you want all three breakpoints, I'd name that and create `LoginPage_Desktop`, `LoginPage_Tablet`, `LoginPage_Mobile` as siblings.

**Concrete plan I'd state to you:**

> I'll create a 1440 × 900 `LoginPage_Desktop` frame, centered vertically and horizontally. Inside it, a 360px-wide `LoginCard` with 24px padding and a 12px corner radius, laid out vertically with 16px gaps. The card contains: a heading ("Sign in"), a subheading, an `EmailField` (label + input), a `PasswordField` (label + input), a `SubmitButton` (full-width, primary), and a `ForgotPasswordLink` below. If your library has `Input`, `ButtonPrimary`, and `LinkText` components, I'll instantiate those via `ref` nodes. If not, I'll build from primitives and flag the candidates for extraction. Colors and spacing will pull from your token variables where defined, or I'll declare sensible defaults with both light and dark values. Does this match what you have in mind?

That's the plan. Naming it explicitly surfaces any misalignment — wrong breakpoint, wrong card width, wrong hierarchy — before I've written a single op.

**One more check at this step:** if the canvas already has other top-level frames on it, I call `find_empty_space_on_canvas` here to get a safe coordinate for placing `LoginPage_Desktop`. I'll pass that `x`/`y` in my first `batch_design` call. Invisible overlaps look like rendering failures and waste debugging time.

---

## What I would NOT do before tools

- I would not start designing and then plan. The plan comes first.
- I would not assume the library has no components without actually checking.
- I would not build a button from a rectangle + text node if the library has a button component.
- I would not use `Inter` as the font (it's an AI-signature default). I'd reach for `Geist` or `Satoshi` for a software UI.
- I would not bind raw `#FFFFFF` or `#000000` directly to surfaces. Everything goes through a `$surface` / `$textPrimary` variable with both `light` and `dark` values declared upfront.
- I would not screenshot after every chunk "to check progress." The verification ladder starts cheap: `batch_design` response confirms ops landed; `snapshot_layout` confirms structure (padding, gaps, widths, child order); `batch_get` confirms property bindings (token references, text content, refs resolved). A screenshot only comes when the question is genuinely visual — real-rendered contrast, spacing rhythm at scale, or final sign-off. For a form this size, I'd expect one or two screenshots total.

---

## Summary of what step 5 (execute) would look like

Once the plan is confirmed, a single `batch_design` call handles most of the work — something in the range of 10–14 ops:

1. If a new document, `open_document("new")` first.
2. If the library isn't imported, `U("doc", { imports: { "ds": "./design/system.lib.pen" } })`.
3. Declare theme axis + color/spacing variables on the document root (if no `design-system/tokens.md` is doing this already).
4. Insert `LoginPage_Desktop` (the 1440 × 900 page frame, centered layout).
5. Insert `LoginCard` inside it (360px wide, vertical auto-layout, padding, corner radius, border via a `$border` variable).
6. Insert heading text node (`LoginHeading`, "Sign in").
7. Insert subheading text node (`LoginSubheading`).
8. Insert `EmailField` — either a `ref` to the library Input component with `descendants` overrides for label/placeholder, or a from-scratch field with a `FieldLabel` + `FieldInput` stack.
9. Insert `PasswordField` — same pattern, `type: "password"`.
10. Insert `SubmitButton` — either a `ref` to `ButtonPrimary` with the "Sign in" label override, or from-scratch. Width `fill_container`.
11. Insert `ForgotPasswordLink` — either a `ref` to `LinkText`, or a styled text node. Center-aligned.

Every node gets a meaningful `name` (PascalCase, role-bearing) and a `context` string for non-trivial nodes. No node is named `Frame 1` or `Text 4`.

After execution: `snapshot_layout` on `LoginCard` to confirm gaps, padding, and widths. Then `batch_get` on the button and link nodes to confirm token bindings resolved. Then — only then — a single `get_screenshot` on `LoginPage_Desktop` for final visual sign-off.

That's the complete pre-tool walkthrough.
