# Evals

Twenty test cases (IDs 0–19) covering the pencil-design skill's full surface: greenfield workflow, library import, verification ladder discipline, variable preservation, clarify-intent protocol, aesthetic defaults (shadows + colour architecture), form discipline, compound components, marketing archetypes, mobile patterns, data viz, microcopy, reference-image translation, industry awareness, iteration rescues, command palette, file architecture, and the SaaS completeness pressure test.

## Running the evals

The skill-creator workflow drives execution. From the skill-creator skill, the typical sequence:

1. **Spawn parallel runs** per eval: one with the skill, one baseline (no skill or prior version snapshot).
2. **Capture timing data** (`total_tokens`, `duration_ms`) per run.
3. **Grade structural assertions** programmatically against the `expected_output` field.
4. **Aggregate** via `python -m scripts.aggregate_benchmark <workspace>/iteration-N`.
5. **Launch the eval-viewer** for qualitative review of outputs and benchmark stats.

See the skill-creator skill for the full workflow.

## Review inside the Pencil app (mandatory)

Programmatic grading of `expected_output` catches structural patterns: did the agent call the right MCP tools in the right order, did it cite the right references, did it avoid the listed anti-patterns. **It does not catch design quality.**

Every eval that produces a `.pen` artifact must also be reviewed inside the Pencil app. Open the resulting `.pen` file in the Pencil desktop app or IDE extension and verify:

- **Visual hierarchy reads correctly.** Squint at the design; the eye should land on the intended primary action first.
- **Tokens render correctly in both modes.** Toggle light / dark; check that the chosen palette holds, contrast remains, and no element disappears against the background.
- **Layered shadows render with depth.** A 1-layer flat shadow vs the prescribed 2-layer ambient + direct is invisible in code review but obvious in the rendered design.
- **Spacing rhythm is consistent.** Section padding, gutter widths, component padding all align to the project's spacing scale.
- **Microcopy reads naturally.** Headlines verb-led, button labels action-specific, error messages guide the exit.
- **Component variants and states match the design-system spec.** Hover, focus, pressed, disabled, loading, error states render correctly per `references/states.md` § Component states matrix.
- **Mobile screens respect safe areas.** Notch, home indicator, dynamic island handled per `references/mobile-patterns.md` § Safe areas.
- **Accessibility patterns hold.** Focus ring visible, contrast meets APCA Lc 75 / WCAG 2.2 AA in both modes, state coding pairs colour with shape.

Without this in-app review step, an eval can pass programmatic assertions while shipping a visually broken design. The structural assertions are necessary; they are not sufficient.

## Evals that need image inputs

Two evals (id 14 `reference-image-translation`, id 16 `iteration-rescue-too-busy`) reference an input image. To run these end-to-end, attach the relevant screenshot in the runner's `files` array (the schema field is `files: []`; populate with paths to PNG / JPG attachments). For id 14, supply a Linear screenshot or similar reference. For id 16, supply or generate a busy design as the input.

If running without image inputs, the evals fall back to discussing the protocol the agent would follow rather than executing against a real image. The qualitative review accounts for this.

## Iterating on the skill from eval results

After running the evals:

1. **Read feedback per run** in the eval-viewer. Empty feedback means the run was acceptable; specific complaints flag where the skill content needs improvement.
2. **Open the `.pen` artifacts** in Pencil and compare the with-skill output against the baseline. The visual delta is the most honest signal.
3. **Iterate the skill** where complaints cluster. Per the skill-creator iteration loop: don't add narrow rules to fix one example; reframe the underlying guidance so it generalises.
4. **Re-run** in a new iteration directory (`iteration-2/`, `iteration-3/`).
5. **Stop iterating** when feedback is mostly empty or the user signals the skill is in a good place.

## Per-eval notes

| ID | Name | Notes for the reviewer |
|---|---|---|
| 0 | login-screen-greenfield | Watch for the get_variables() pre-execution call. Confirm structural-first verification ladder. |
| 1 | design-system-scaffold | Confirm 12 core templates copied; 13 optional templates mentioned with conditional triggers. |
| 2 | import-library-and-use | Confirm `imports` field check, `ref` instantiation, scoped get_screenshot. |
| 3 | edit-existing-card-verification-ladder | Total get_screenshot calls in the edit phase: 1. Scoped to the LoginCard, not the page. |
| 4 | multi-section-page-verification-cadence | Total get_screenshot across the build: 1 or 2. Per-region verification is structural. |
| 5 | preserve-existing-variables | get_variables() before set_variables. Diff against existing keys. Never `replace: true`. |
| 6 | clarify-intent-before-designing | Three clarifying questions before any batch_design. Skipped if design-system/ is populated. |
| 7 | shadow-and-color-architecture | Two-role colour, layered shadow, hover increases contrast, nested radius child ≤ parent. |
| 8 | form-design-discipline | Visible labels, on-blur validation, autocomplete attrs, mobile font-size ≥ 16px. |
| 9 | compound-component-design | Provider / Frame / Header / Input / Footer slot pattern. Explicit variants over boolean props. |
| 10 | marketing-page-archetypes | NO three-card grid. Asymmetric or bento. NO auto-rotating carousel. Verb-led microcopy. |
| 11 | mobile-bottom-sheet-vs-modal | Sheet for non-blocking; modal for destructive confirm. Safe areas. Tab bar ≤ 5 items. |
| 12 | data-viz-dashboard | Chart per data shape. Okabe-Ito + Viridis. NO pie > 5, NO 3D, NO dual y-axes. Sparklines inline. |
| 13 | microcopy-quality | Errors guide exit, not blame. Empty frames as beginning. Action-specific button labels. |
| 14 | reference-image-translation | Names layout pattern, extracts palette + type, calls out preserve vs change, recreates with project tokens. |
| 15 | industry-aware-saas | Developer-tool conventions: dense, monospace-friendly, dark-default. Cites Linear / Vercel / Cursor. |
| 16 | iteration-rescue-too-busy | Diagnoses the busyness; subtracts (not adds) to fix. The most common second-iteration failure is adding. |
| 17 | command-palette-pattern | Search + grouped results + keyboard nav indicators + recent commands. ⌘+K trigger. |
| 18 | file-architecture-cover-and-sections | Cover at (0,0), section regions, hierarchical naming, no Exploration in Source of Truth. |
| 19 | saas-completeness-pressure-test | Empty / loading / error / no-permission / plan-restricted states all designed. Admin surface covered. |

## See also

- `../SKILL.md`: the canonical skill content this eval suite tests.
- The skill-creator skill: workflow for spawning runs, grading, aggregating, and viewing.
- `assets/examples/`: worked examples that show the agent the patterns the evals test.
