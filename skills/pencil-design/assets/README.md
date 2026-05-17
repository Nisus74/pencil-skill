# `assets/`

Bundled supplementary content that ships with the `pencil-design` skill. One subfolder:

| Subfolder | Purpose | Loaded |
|-----------|---------|--------|
| `examples/` | **Worked walkthroughs the agent reads on demand.** Not copied into user projects — they live here for the agent to consult when a task matches a pattern (greenfield design, importing a library, error screens, multi-step flows). | At runtime, on demand, by the agent |

If you're adding a new file:
- It belongs in `examples/` if it documents **how the skill should perform a workflow** (illustrative, not authoritative).
- Authoritative platform/technical reference docs (tool name maps, schema, grammar) belong in the sibling `references/` folder, not here.
