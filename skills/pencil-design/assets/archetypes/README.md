# Archetypes

A library of named design archetypes the AI can pick from when the user is silent on aesthetics. Each archetype is a concrete bundle of moves: typography, density, accent strategy, surface treatment, data display, microcopy, motion, anti-cues.

## Defaults, not prescriptions

The user's own direction always wins. If the user has supplied a reference, named a brand, described an aesthetic, or pointed to an existing design, follow that direction. Archetypes only apply when the user is silent on aesthetics. Treat them as starting points to react against, never as fixed answers.

When a user does provide direction, you can still load the closest archetype as scaffolding, then override the sections their direction touches. Per-session direction always overrides.

## How to use

1. **At the start of a design task,** check whether the user has expressed any aesthetic direction. If yes, follow that. If no, scan this index and pick the archetype whose surface category and moves match the brief.
2. **Read the chosen archetype file in full** before any `batch_design` call. Each section is concrete, typography, density, accent strategy, etc.
3. **Name the archetype out loud** in your plan ("I'm building this in `analytics-dashboard`") so the user can correct course before you commit time.
4. **Follow the anti-cues.** Each archetype lists moves that break it. Treat those as bugs.

## Index

| Surface category | Archetype | Status |
|---|---|---|
| **saas-apps/b2b** | analytics-dashboard | populated v2.0.0 |
| | enterprise-corporate | populated v2.0.0 |
| | modern-pro-tool | populated v2.0.0 |
| | workflow-platform | populated v2.0.0 |
| **saas-apps/b2c** | consumer-finance | populated v2.0.0 |
| | consumer-media | populated v2.0.0 |
| | consumer-productivity | populated v2.0.0 |
| | consumer-social | populated v2.0.0 |
| **mobile** | android-material | populated v2.0.0 |
| | cross-platform-modern | populated v2.0.0 |
| | ios-native-social | populated v2.0.0 |
| | ios-native-utility | populated v2.0.0 |
| **ai-products** | agent-execution | populated v2.0.0 |
| | ai-augmented-workspace | populated v2.0.0 |
| | canvas-spatial | populated v2.0.0 |
| | conversation-chat | populated v2.0.0 |
| **marketing-websites** | conversion-focused-saas | populated v2.0.0 |
| | editorial-storytelling | populated v2.0.0 |
| | (4 more planned) | coming in v2.x |
| **saas-apps/b2b2b** | (3 planned) | coming in v2.x |
| **editors-creative-tools** | (5 planned) | coming in v2.x |
| **e-commerce-content** | (3 planned) | coming in v2.x |
| **docs-onboarding** | (3 planned) | coming in v2.x |

## File shape

Every archetype follows the same 11-section template so AI implementers can read any one and know where to find what they need. The sections, in order:

1. **Essence** (one line)
2. **When to choose this archetype**
3. **Typography**
4. **Density**
5. **Accent strategy**
6. **Surface treatment**
7. **Data display**
8. **Microcopy / voice**
9. **Motion personality**
10. **Anti-cues** (moves that break the archetype)
11. **Worked example** (a typical surface in this archetype, made concrete)
12. **Notes for AI implementers** (Pencil tokens, components most affected, common slip-ups)

Each section is 3–8 lines max. Files cap at ~200 lines.

## Adding new archetypes

Two paths:

- **Per-session ephemeral.** When a user pastes a reference image, the skill synthesises an ephemeral archetype for that session only. See `references/reference-ingestion.md`.
- **Permanent contribution.** A user's per-session ephemeral that proves itself across multiple projects can graduate into a shipped file via PR. Use the same template; cite real exemplars; describe in your own words (no third-party screenshots shipped).
