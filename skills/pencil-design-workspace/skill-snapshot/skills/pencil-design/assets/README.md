# `assets/`

Bundled supplementary content that ships with the `pencil-design` skill. Two subfolders, two purposes:

| Subfolder | Purpose | Loaded |
|-----------|---------|--------|
| `design-system/` | **Templates copied into user projects** when the skill scaffolds a `design-system/` folder. Markdown only; users edit them by hand. | At scaffold time (one-shot copy into the user repo) |
| `examples/` | **Worked walkthroughs the agent reads on demand.** Not copied into user projects — they live here for the agent to consult when a task matches a pattern (greenfield design, importing a library, scaffolding the system). | At runtime, on demand, by the agent |

If you're adding a new file:
- It belongs in `design-system/` if a user should be able to **edit it inside their own project**.
- It belongs in `examples/` if it documents **how the skill should perform a workflow** (illustrative, not authoritative).
- Authoritative platform/technical reference docs (tool name maps, schema, grammar) belong in the sibling `references/` folder, not here.
