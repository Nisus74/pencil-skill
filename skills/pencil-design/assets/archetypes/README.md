# Archetypes

A library of named design archetypes the AI can pick from when the user is silent on aesthetics. Each archetype is a concrete specification: component-by-component node trees, exact pixel values, WHY reasoning for every non-obvious decision, WRONG code examples showing what generic output looks like, and a verification checklist.

## Defaults, not prescriptions

The user's own direction always wins. If the user has supplied a reference, named a brand, described an aesthetic, or pointed to an existing design, follow that direction. Archetypes only apply when the user is silent on aesthetics. Treat them as starting points to react against, never as fixed answers.

When a user does provide direction, you can still load the closest archetype as scaffolding, then override the sections their direction touches. Per-session direction always overrides.

## How to use

1. **At the start of a design task,** check whether the user has expressed any aesthetic direction. If yes, follow that. If no, scan this index and pick the archetype whose surface category and moves match the brief.
2. **Read the chosen archetype file in full** before any `batch_design` call. Each section has exact specification values, not guidance.
3. **Name the archetype out loud** in your plan ("I'm building this in `analytics-dashboard`") so the user can correct course before you commit time.
4. **Run the verification checklist** at step 6 of the default workflow. Each archetype file includes a `## Verification checklist` section with pass/fail items and WHY for each.

## Index

| Surface category | Archetype | File |
|---|---|---|
| **saas-apps/b2b** | analytics-dashboard | [saas-apps/b2b/analytics-dashboard.md](saas-apps/b2b/analytics-dashboard.md) |
| | enterprise-corporate | [saas-apps/b2b/enterprise-corporate.md](saas-apps/b2b/enterprise-corporate.md) |
| | modern-pro-tool | [saas-apps/b2b/modern-pro-tool.md](saas-apps/b2b/modern-pro-tool.md) |
| | workflow-platform | [saas-apps/b2b/workflow-platform.md](saas-apps/b2b/workflow-platform.md) |
| **saas-apps/b2c** | consumer-finance | [saas-apps/b2c/consumer-finance.md](saas-apps/b2c/consumer-finance.md) |
| | consumer-productivity | [saas-apps/b2c/consumer-productivity.md](saas-apps/b2c/consumer-productivity.md) |
| **saas-apps/b2b2b** | developer-platform | [saas-apps/b2b2b/developer-platform.md](saas-apps/b2b2b/developer-platform.md) |
| **mobile** | cross-platform-modern | [mobile/cross-platform-modern.md](mobile/cross-platform-modern.md) |
| | ios-native-utility | [mobile/ios-native-utility.md](mobile/ios-native-utility.md) |
| **ai-products** | agent-execution | [ai-products/agent-execution.md](ai-products/agent-execution.md) |
| | ai-augmented-workspace | [ai-products/ai-augmented-workspace.md](ai-products/ai-augmented-workspace.md) |
| | conversation-chat | [ai-products/conversation-chat.md](ai-products/conversation-chat.md) |
| **marketing-websites** | conversion-focused-saas | [marketing-websites/conversion-focused-saas.md](marketing-websites/conversion-focused-saas.md) |
| | editorial-storytelling | [marketing-websites/editorial-storytelling.md](marketing-websites/editorial-storytelling.md) |

## Picking between archetypes

| User cue | Archetype |
|---|---|
| Analytics, metrics, KPIs, dashboards | `analytics-dashboard` |
| Project management, tasks, status tracking | `workflow-platform` |
| Productivity tool for individual (todos, notes) | `consumer-productivity` |
| Banking, investing, payments, fintech | `consumer-finance` |
| Enterprise software (HR, CRM, ERP) | `enterprise-corporate` |
| Dev console, API dashboard, webhook logs | `developer-platform` |
| Power tool for experts (Linear-style, dense) | `modern-pro-tool` |
| Native iOS app | `ios-native-utility` |
| React Native / Expo / Flutter | `cross-platform-modern` |
| AI chat assistant | `conversation-chat` |
| Agent doing autonomous work | `agent-execution` |
| AI embedded in an editor/workspace | `ai-augmented-workspace` |
| Marketing/landing page with CTAs | `conversion-focused-saas` |
| Methodology/editorial narrative page | `editorial-storytelling` |

## File structure

Each archetype is a specification document, not a guidance document. Sections are organised by component/surface (not by aesthetic concept like "typography" or "density"). Each section includes:

- **Node tree** — ASCII hierarchy showing the exact parent/child structure
- **Exact values** — specific pixel measurements, token names, font sizes
- **WHY** — the reason behind each non-obvious decision, grounded in first principles
- **What generic looks like** — WRONG code showing the AI default that produces slop
- **Detect** — how to spot a failure in a screenshot
- **Verification checklist** — pass/fail items with WHY for each

This format is based on `references/chart-anatomy.md`. Read that file to understand the register.

## Adding new archetypes

Two paths:

- **Per-session ephemeral.** When a user pastes a reference image, the skill synthesises an ephemeral archetype for that session only. See `references/reference-ingestion.md`.
- **Permanent contribution.** A user's per-session ephemeral that proves itself across multiple projects can graduate into a shipped file via PR. Follow the specification format above; cite real exemplars; confirm values against devtools rather than impressions.
