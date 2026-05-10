# developer-platform

Developer-facing consoles and dashboards where the user is building something with the product's API, managing keys and usage, and reading technical documentation. Trust, precision, and developer ergonomics are primary.

**Surface category:** saas-apps/b2b2b
**Exemplars:** Stripe Dashboard, Twilio Console, AWS Console, Vercel Dashboard
**Confidence:** high; Stripe and Vercel confirmed from direct use (May 2026); Twilio from direct use

Read this alongside `references/batch-design-grammar.md`. The critical differentiators from `analytics-dashboard`: this archetype serves technical users who need to read API responses, copy keys, and debug integrations. Monospace is used more broadly. Code is a primary content type.

---

## When to use this archetype

Pick this for API consoles, developer dashboards, key management interfaces, webhook event logs, and any product where the end user is a software engineer integrating the service. Skip it when the primary user is a business analyst or executive; use `analytics-dashboard` instead.

---

## Design token reference

| Token | Value | Role |
|-------|-------|------|
| `$bg` | `#0A0A0D` (dark canonical) or `#F9FAFB` (light option) | Page background. Stripe and Vercel use dark. |
| `$bgPanel` | `#111115` (dark) or `#FFFFFF` (light) | Card and panel surfaces. |
| `$bgCode` | `#161619` (dark) or `#F3F4F6` (light) | Code block and terminal background. |
| `$textPrimary` | `#F0EEEC` (dark) or `#111110` (light) | Primary content text. |
| `$textSecondary` | `#A8A29E` (dark) or `#6B6A6B` (light) | Labels, metadata, secondary copy. |
| `$textMuted` | `#57534E` (dark) or `#A1A0A0` (light) | Timestamps, helper text. |
| `$border` | `#2A2A2E` (dark) or `#E7E5E4` (light) | Card borders, table dividers. |
| `$accent` | Saturation 55–65%. Stripe uses `#635BFF` (violet). | Primary CTA, selected state. |
| `$positive` | `#22C55E` | Successful event, 2xx status, active subscription. |
| `$warning` | `#F59E0B` | Warning event, degraded, limited quota. |
| `$negative` | `#EF4444` | Failed event, 4xx/5xx status, expired key. |
| `$fontMono` | `Geist Mono` | API keys, IDs, event data, HTTP methods, response bodies, ALL technical identifiers. |
| `$fontBody` | `Inter` | Labels, descriptions, navigation. |
| `$fontCode` | Same as `$fontMono` | Code examples, inline code in documentation. |

### The monospace rule for developer platforms

`$fontMono` applies to everything that is technically precise:
- API keys (`sk_live_...`, `pk_test_...`)
- Resource IDs (`cus_abc123`, `pi_xyz789`, `req_7h3k...`)
- HTTP method labels (`GET`, `POST`, `DELETE`)
- HTTP status codes (`200`, `404`, `500`)
- Timestamps in logs (`2026-05-10T14:23:11Z`)
- Webhook event names (`payment_intent.succeeded`)
- Response body content
- Command-line examples

The only developer-platform content that is NOT monospace: navigation labels, button text, headings, descriptive prose.

---

## Page shell

```
AppShell (frame, fill_container x fill_container, layout: horizontal,
           fill: "$bg")
├── Sidebar (frame, 240 x fill_container, layout: vertical,
│             fill: "$bgPanel",
│             stroke: { right: { color: "$border", thickness: 1 } })
│   // Navigation: Dashboard, Payments, Customers, Events, API Keys, Docs, Settings
└── MainContent (frame, fill_container x fill_container, layout: vertical,
                  fill: "$bg", padding: [24, 24], gap: 20)
```

---

## API key card

The API key card is a canonical developer-platform component. Key management is a primary task.

```
APIKeyCard (frame, fill_container x fit_content, layout: vertical,
             gap: 12, padding: [16, 16],
             cornerRadius: 8,
             stroke: { color: "$border", thickness: 1 },
             fill: "$bgPanel")
├── KeyHeader (frame, fill_container x fit_content, layout: horizontal,
│               alignItems: center, justifyContent: space_between)
│   ├── KeyLabel (text, 14px, fontWeight: 600, $textPrimary,
│   │             content: "Secret key")
│   └── KeyStatus (frame, fit_content x 20, layout: horizontal,
│                   alignItems: center, gap: 4, padding: [0, 8],
│                   cornerRadius: 4, fill: "$positive at 12% opacity")
│       ├── StatusDot (5×5, cornerRadius: 3, fill: "$positive")
│       └── StatusLabel (text, 12px, fontWeight: 500, fill: "$positive",
│                          content: "Live")
├── KeyValue (frame, fill_container x 36, layout: horizontal,
│              alignItems: center, justifyContent: space_between,
│              padding: [0, 12], cornerRadius: 6,
│              fill: "$bgCode")
│   ├── KeyText (text, 13px, $fontMono, $textSecondary,
│   │            content: "sk_live_••••••••••••••••FKJH")
│   │   // Masked by default. Full value visible on click.
│   └── CopyButton (frame, fit_content x 24, cornerRadius: 4,
│                    fill: transparent, padding: [0, 8])
│       └── CopyLabel (text, 12px, $textMuted, $fontBody, content: "Copy")
└── KeyMeta (text, 12px, $textMuted, content: "Created May 3, 2026 · Last used 2h ago")
```

### What generic looks like

```
// WRONG: API key in proportional font
KeyText=I(keyCard, {
  type: "text",
  fontFamily: "$fontBody",   // WRONG: proportional font
  fontSize: 14,
  content: "sk_live_abc123..."
})
// API keys are technical identifiers, not prose. Proportional font makes
// a key look like a username. Monospace at 13px signals "this is a token
// you will copy into a terminal or config file."

// WRONG: full key displayed by default
KeyText=I(keyCard, {
  content: "sk_live_MqfT8vKJnPL2..."  // WRONG: full key exposed
})
// Secret keys should be masked by default. Displaying full key values
// in a dashboard where colleagues might walk past the screen is a
// security anti-pattern. Show the last 4 characters: "••••FKJH".
```

---

## Event log row

```
EventRow (frame, fill_container x 48, layout: horizontal,
           alignItems: center, gap: 12, padding: [0, 16],
           stroke: { bottom: { color: "$border", thickness: 1 } })
│   // 48px. Events need room for 5 columns: status, method, path, time, detail.
├── StatusCode (frame, 40 x 20, layout: horizontal,
│               alignItems: center, justifyContent: center,
│               cornerRadius: 4)
│   // 200–299: fill: "$positive at 12%", text: "$positive", $fontMono, 12px
│   // 400–499: fill: "$warning at 12%", text: "$warning", $fontMono, 12px
│   // 500+:    fill: "$negative at 12%", text: "$negative", $fontMono, 12px
│   └── CodeLabel (text, 12px, fontWeight: 600, $fontMono)
├── Method (text, 12px, fontWeight: 600, $fontMono, fill: "$accent",
│           content: "POST")
│   // HTTP method always monospace. GET/POST/DELETE/PUT/PATCH each same width.
├── EventPath (text, 13px, $fontMono, $textSecondary,
│               content: "/v1/payment_intents", width: fill_container)
├── Timestamp (text, 12px, $fontMono, $textMuted,
│               content: "14:23:11")
└── ChevronRight (12×12, $textMuted)
```

### Critical measurements

| Element | Value | Notes |
|---------|-------|-------|
| Row height | 48px | 5 columns of technical data need more vertical space than typical list rows. |
| Status code badge | 40×20px, cornerRadius: 4 | Fixed width so codes align vertically. `cornerRadius: 4` is institutional; `cornerRadius: 10` is consumer. |
| All text in log rows | `$fontMono` except label column | Path, method, status, timestamp: all monospace. |
| HTTP method colour | `$accent` | The method is the most semantically important cell. Accent colour distinguishes it. |

### What generic looks like

```
// WRONG: event log in proportional font
EventPath=I(row, {
  fontFamily: "$fontBody",   // WRONG: proportional
  fontSize: 14
})
// A developer reading "/v1/payment_intents/pi_3abc123..." in Inter
// cannot visually scan it as a technical path. Monospace makes paths,
// IDs, and timestamps instantly readable as machine output.

// WRONG: all three HTTP status groups in the same colour
StatusCode=I(row, {
  fill: "$accent at 12% opacity",   // WRONG: same for 200, 400, 500
  text: "$accent"
})
// Status codes tell the developer what went wrong. Green/amber/red
// colour coding allows instant status scanning without reading each code.
// A uniform accent colour requires the developer to read every number.
```

---

## Code block

Developer platform code blocks are larger, more detailed, and more frequently present than in other archetypes.

```
CodeBlock (frame, fill_container x fit_content, layout: vertical,
            cornerRadius: 8,
            fill: "$bgCode",
            stroke: { color: "$border", thickness: 1 })
├── CodeHeader (frame, fill_container x 36, layout: horizontal,
│               alignItems: center, justifyContent: space_between,
│               padding: [0, 12],
│               stroke: { bottom: { color: "$border", thickness: 1 } })
│   ├── LanguageTabs (frame, fit_content x fit_content, layout: horizontal, gap: 0)
│   │   └── LangTab × N
│   │       // Each tab: 60pt wide, 36pt tall, 13px $fontMono, $textMuted
│   │       // Active tab: $textPrimary, bottom border 2px $accent
│   └── CopyButton (frame, fit_content x 24, cornerRadius: 4, padding: [0, 8])
│       └── CopyLabel (text, 12px, $textMuted, content: "Copy")
└── CodeBody (text, 13px, $fontMono, $textPrimary,
               lineHeight: 1.6, padding: [16, 16])
```

### Language tabs

Language tabs let users pick their preferred SDK:

```
// Common tab set for payment API:
tabs: ["curl", "Node", "Python", "Ruby", "PHP", "Go"]
// Always show at minimum: curl, Node.js, Python
// Show all that the product supports. Don't assume one language.
```

---

## Sidebar navigation

Developer platform sidebars have two registers: product navigation (top) and utility navigation (bottom).

```
DevSidebar (frame, 240 x fill_container, layout: vertical,
             padding: [12, 8], gap: 0,
             fill: "$bgPanel",
             stroke: { right: { color: "$border", thickness: 1 } })
├── ProductLogo (frame, fill_container x 40, layout: horizontal,
│                alignItems: center, padding: [0, 8], gap: 10, margin: [0, 0, 8, 0])
│   // Logo + product name. Links to dashboard root.
├── PrimaryNav (frame, fill_container x fill_content, layout: vertical, gap: 2)
│   └── NavItem × N (see below)
└── UtilityNav (frame, fill_container x fit_content, layout: vertical, gap: 2,
                 padding: [12, 0, 0, 0],
                 stroke: { top: { color: "$border", thickness: 1 } })
    // Bottom of sidebar: API Keys, Documentation, Settings, Help

NavItem (frame, fill_container x 32, layout: horizontal,
          alignItems: center, gap: 8, padding: [0, 8], cornerRadius: 6)
│   // Active: fill: "$accent at 10% opacity", text/icon: "$accent"
│   // Resting: fill: transparent, text/icon: "$textSecondary"
│   // No left border (use background fill for active state in dev platforms)
├── NavIcon (16×16, fill: context-dependent)
└── NavLabel (text, 14px, $fontBody, fill: context-dependent)
    // Navigation labels are $fontBody, NOT $fontMono.
    // "Payments", "Customers" — these are product nouns, not technical identifiers.
```

---

## Microcopy library

### API key interface

| Generic (avoid) | This archetype |
|-----------------|----------------|
| Your private key | Secret key |
| Public key | Publishable key |
| Test keys | Test mode keys |
| Live keys | Live mode keys |
| Copy key | Copy |
| Revoke this key | Roll key |

### Event log

| Generic (avoid) | This archetype |
|-----------------|----------------|
| Request succeeded | 200 OK |
| Request failed | 400 Bad Request / 500 Internal Server Error |
| Event timestamp | 2026-05-10T14:23:11Z (`$fontMono`) |
| Request ID | req_7h3k4r9p2m (`$fontMono`) |

### Empty log state

| Generic (avoid) | This archetype |
|-----------------|----------------|
| No events | No events in this time range |
| Nothing here | No requests in the last 24 hours |
| All clear | Your API hasn't been called yet |

---

## Verification checklist

### Monospace rule

- [ ] **API keys, resource IDs, HTTP methods, status codes, paths, and timestamps all use `$fontMono`.**
  WHY: Technical identifiers in proportional fonts look like UI labels, not data. Monospace is the visual code for "this is a value you will read precisely, copy, or use in code." A developer scanning an event log with proportional text has to shift mental register between "reading UI labels" and "reading API data." Monospace eliminates that shift.

- [ ] **Navigation labels and button text use `$fontBody` (not `$fontMono`).**
  WHY: Making everything monospace overcorrects. Navigation items and actions are human-readable labels, not technical identifiers. A monospace "Payments" in the sidebar reads as a terminal command. The distinction between `$fontMono` (data) and `$fontBody` (interface) must be consistent.

### API keys

- [ ] **Secret keys are masked by default, showing only the last 4 characters.**
  WHY: Security practice. A developer sitting at their laptop in a coffee shop should not have their live secret key visible to someone walking past. Partial masking (`sk_live_••••FKJH`) provides enough visual identification without exposure.

- [ ] **Key value container uses `$bgCode` fill and monospace font.**
  WHY: The key container's code background (`$bgCode`) signals "this is a technical value, not a form field." Without the code background, an API key in a card looks like an editable input. The code background says "read this, copy this, don't type into it."

### Event log

- [ ] **Status codes are colour-coded: 2xx green, 4xx amber, 5xx red.**
  WHY: An event log with 50 rows is unreadable if the developer has to read each status code. Colour coding allows instant pattern recognition: "I see red rows, something is failing." This matches the universal convention across Stripe, Twilio, AWS, and all major developer platforms.

- [ ] **HTTP method (`GET`, `POST`, etc.) is `$accent` colour.**
  WHY: The method is the most semantically loaded column in an event log. `POST /v1/payment_intents` is different from `GET /v1/payment_intents`. Highlighting the method in accent colour draws the eye to the action, not just the path.

---

## Contrast examples

### Example 1: Event log row (correct vs generic)

**Correct:**

```
eventRow=I(eventLog, {
  type: "frame", name: "EventRow",
  layout: "horizontal", alignItems: "center",
  height: 48, width: "fill_container",
  padding: [0, 16], gap: 12,
  stroke: { bottom: { color: "$border", thickness: 1 } }
})
statusBadge=I(eventRow, {
  type: "frame",
  width: 40, height: 20, cornerRadius: 4,
  fill: "$positive at 12% opacity"
})
statusCode=I(statusBadge, {
  type: "text", content: "200",
  fontFamily: "$fontMono", fontSize: 12, fontWeight: 600,
  fill: "$positive"
})
method=I(eventRow, {
  type: "text", content: "POST",
  fontFamily: "$fontMono", fontSize: 12, fontWeight: 600,
  fill: "$accent"
})
path=I(eventRow, {
  type: "text", content: "/v1/payment_intents",
  fontFamily: "$fontMono", fontSize: 13,
  fill: "$textSecondary"
})
```

Why this is right: monospace throughout the technical columns. Green tinted badge for 200. Accent-coloured POST. Path in `$textSecondary` so it doesn't compete with the method.

**Generic:**

```
eventRow=I(eventLog, {
  type: "frame", height: 40, layout: "horizontal"   // WRONG: 40px, tight
})
statusBadge=I(eventRow, {
  type: "frame", cornerRadius: 12,   // WRONG: pill-shaped
  fill: "$positive"   // WRONG: full-opacity green
})
statusCode=I(statusBadge, {
  type: "text", content: "200",
  fontFamily: "$fontBody",   // WRONG: proportional font for a code
  fill: "#FFFFFF"   // WRONG: white on green
})
path=I(eventRow, {
  type: "text", content: "/v1/payment_intents",
  fontFamily: "$fontBody"   // WRONG: API path in proportional font
})
```

Why this is wrong: proportional font on status codes and paths removes the "this is technical data" signal. Full-opacity green badge with white text fails contrast for small monospace text. Pill-shaped badge reads as a consumer tag, not a technical status indicator. 40px rows are cramped for 5-column technical data.

---

### Example 2: API key (correct vs generic)

**Correct:**

```
keyCard=I(panel, {
  type: "frame", name: "APIKeyCard",
  layout: "vertical", gap: 12, padding: [16, 16],
  cornerRadius: 8,
  stroke: { color: "$border", thickness: 1 },
  fill: "$bgPanel"
})
keyValue=I(keyCard, {
  type: "frame", height: 36,
  cornerRadius: 6, fill: "$bgCode"
  // Contains: masked key + copy button
})
keyText=I(keyValue, {
  type: "text",
  content: "sk_live_••••••••••FKJH",
  fontFamily: "$fontMono", fontSize: 13,
  fill: "$textSecondary"
})
```

Why this is right: `$bgCode` fill signals "technical value." Monospace at 13px reads as a token. Masked with partial last-4 visible. Card with 1px border (not shadow).

**Generic:**

```
keyCard=I(panel, {
  type: "frame",
  fill: "$surface",
  effect: [{ type: "drop_shadow", ... }],   // WRONG: shadow on key card
  cornerRadius: 12
})
keyText=I(keyCard, {
  type: "text",
  content: "sk_live_MqfT8vKJnPL2...",   // WRONG: full key exposed
  fontFamily: "$fontBody",   // WRONG: proportional font
  fontSize: 14, fill: "$textPrimary"
})
```

Why this is wrong: a shadow on the key card prioritises visual decoration over technical legibility. Proportional font makes the key look like a username. Full key value exposed is a security anti-pattern. The shadow, proportional font, and exposed key together produce the "landing page features section" aesthetic, not the "developer console" aesthetic.
