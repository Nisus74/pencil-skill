# consumer-finance

Banking, investing, and fintech products where trust, clarity, and precise numerics are primary. The design must read as stable and reliable while feeling modern, not clinical. Number presentation is the most consequential design decision in this archetype.

**Surface category:** saas-apps/b2c
**Exemplars:** Mercury (banking), Robinhood (investing), Stripe Dashboard (payments), Monzo (mobile banking)
**Confidence:** high; Mercury and Stripe confirmed from direct use (May 2026); Robinhood from direct use

Read this alongside `references/batch-design-grammar.md`. The critical rule: all financial figures use `$fontMono`. No exceptions. A balance displayed in a proportional font is the primary visual tell that a financial app is unserious.

---

## When to use this archetype

Pick this for bank accounts, investment portfolios, payment dashboards, expense trackers, and any product where monetary values are primary content. Skip it for internal analytics; use `analytics-dashboard` instead. Skip it for accounting software with dense tabular data; use `enterprise-corporate` instead.

---

## Design token reference

| Token | Value | Role |
|-------|-------|------|
| `$bg` | `#F8F8FA` | Page background. Near-white, slightly cool. Trust register. |
| `$surface` | `#FFFFFF` | Card surfaces. |
| `$surfaceDark` | `#0A0A0D` | Dark hero cards (account balance, portfolio total). |
| `$textPrimary` | `#0D0D10` | Labels, UI text. |
| `$textSecondary` | `#6B6B76` | Metadata, date labels, secondary figures. |
| `$textMuted` | `#A0A0AA` | Placeholder, help text. |
| `$border` | `#E8E8F0` | Card borders, dividers. |
| `$positive` | `#16A34A` | Gain, positive delta, incoming transaction. Green. |
| `$negative` | `#DC2626` | Loss, negative delta, outgoing transaction. Red. |
| `$neutral` | `#6B6B76` | Zero change, pending, stable. |
| `$accent` | Saturation 55–65%. Often blue or violet. | Primary CTA, selected state. |
| `$fontMono` | `Geist Mono` | All monetary values, all percentages, all numeric data. |
| `$fontBody` | `Inter` or `system-ui` | Labels, descriptions, UI copy. |
| `$fontDisplay` | `Inter Display` or a deliberate serif | Hero balance figure only. |

### The monospace rule

Every financial figure uses `$fontMono`. This includes:
- Account balances ($23,419.50)
- Transaction amounts (+$240.00, -$84.99)
- Portfolio values and percentages (+4.7%)
- Price figures ($2,847.30 per share)
- Fee displays ($0.00, $2.50)

The only exception: narrative pricing copy on marketing-adjacent surfaces ("Just $9/month"). In the app itself, every number is monospace.

---

## Page shell

```
AppShell (frame, fill_container x fill_container, layout: horizontal,
           fill: "$bg")
├── Sidebar (frame, 220 x fill_container, layout: vertical,
│             fill: "$surface",
│             stroke: { right: { color: "$border", thickness: 1 } })
│   // 220px. Navigation: Accounts, Transactions, Cards, Transfers, Settings.
└── MainPanel (frame, fill_container x fill_container, layout: vertical,
                fill: "$bg", padding: [24, 24], gap: 20)
```

---

## Account balance card

The account balance card is the first thing the user sees. It deserves the most design attention in this archetype.

```
BalanceCard (frame, fill_container x 180, layout: vertical,
              gap: 8, padding: [28, 28],
              cornerRadius: 12,
              fill: "$surfaceDark")
│   // Dark card for the primary balance. Signals importance.
│   // Not the accent colour — dark is trust, accent is brand.
├── AccountLabel (text, 13px, $fontBody, fill: "#A8A3B0",
│                  content: "Checking account")
├── BalanceFigure (text, 40px, fontWeight: 700, $fontMono,
│                   fill: "#F0EEFC",
│                   content: "$23,419.50")
│   // 40px. Range: 36–48px depending on digit length.
│   // $fontMono is mandatory. 40px monospace reads as "this is a precise figure."
│   // 40px proportional reads as "this is a headline."
├── BalanceDelta (frame, fit_content x 24, layout: horizontal,
│                  alignItems: center, gap: 4)
│   ├── DeltaArrow (text, 12px, fill: "$positive" or "$negative",
│   │               content: "↑" or "↓")
│   └── DeltaLabel (text, 13px, $fontMono, fill: "$positive" or "$negative",
│                    content: "+$842.00 this month")
└── ActionRow (frame, fill_container x fit_content, layout: horizontal,
                gap: 8, padding: [8, 0, 0, 0])
    ├── SendButton (frame, fit_content x 32, cornerRadius: 6,
    │               fill: "#FFFFFF18", padding: [0, 12])
    │   └── SendLabel (text, 13px, fontWeight: 500, fill: white, content: "Send")
    └── ReceiveButton (same style as SendButton, content: "Receive")
```

### What generic looks like

```
// WRONG: balance in proportional font
BalanceFigure=I(card, {
  type: "text",
  fontFamily: "$fontDisplay",   // WRONG: display/proportional font
  fontSize: 40, fontWeight: 700,
  content: "$23,419.50"
})
// A 40px balance in Inter Display looks like a hero number on a marketing page.
// A 40px balance in Geist Mono looks like a bank statement.
// The font is the signal. Proportional = "this is design."
// Monospace = "this is data." Financial figures are data.

// WRONG: balance card in $accent colour
BalanceCard=I(panel, {
  fill: "$accent"   // WRONG: brand colour for balance card
})
// Accent-coloured balance cards look like a CTA button.
// Dark (`$surfaceDark`) reads as premium and stable. It's the Mercury register.
```

---

## Transaction row

```
TransactionRow (frame, fill_container x 56, layout: horizontal,
                 alignItems: center, gap: 12, padding: [0, 4],
                 stroke: { bottom: { color: "$border", thickness: 1 } })
├── MerchantLogo (frame, 36 x 36, cornerRadius: 8,
│                  fill: derived from merchant name)
│   // If logo unavailable: monogram from merchant name. Same pattern as
│   // analytics-dashboard avatar. 36px is slightly larger (financial rows are taller).
├── TransactionInfo (frame, fill_container x fit_content, layout: vertical, gap: 2)
│   ├── MerchantName (text, 14px, fontWeight: 500, $textPrimary, $fontBody)
│   └── TransactionMeta (text, 12px, $textSecondary,
│                          content: "May 10 · Debit card")
└── AmountBlock (frame, fit_content x fit_content, layout: vertical,
                  alignItems: flex_end, gap: 2)
    ├── Amount (text, 15px, fontWeight: 600, $fontMono,
    │           fill: "$negative" for outgoing, "$positive" for incoming,
    │           content: "-$84.99" or "+$500.00")
    └── Balance (text, 12px, $fontMono, $textSecondary,
                  content: "$22,576.51")
        // Running balance after this transaction. Optional but valuable.
```

### Critical measurements

| Element | Value | Notes |
|---------|-------|-------|
| Row height | 56px | Taller than B2B rows. Financial context benefits from extra breathing room per transaction. |
| Amount font | `$fontMono`, 15px, fontWeight: 600 | All transaction amounts are monospace. The weight distinguishes amount from running balance. |
| Running balance | `$fontMono`, 12px, `$textSecondary` | Smaller and muted. It's contextual, not the primary read. |
| Outgoing amount | `$negative` (red) | Standard financial convention: spend is red, receive is green. |
| Incoming amount | `$positive` (green) | Do not reverse this. Red for positive and green for negative reads as broken. |

### What generic looks like

```
// WRONG: amount in proportional font
Amount=I(transactionRow, {
  type: "text",
  fontFamily: "$fontBody",   // WRONG: proportional
  fontSize: 15, fontWeight: 600,
  content: "-$84.99"
})
// Proportional font transaction amounts look like price tags in an e-commerce app.
// Monospace is the visual code for "precise financial figure."
// This is the most common mistake in AI-generated fintech designs.

// WRONG: amounts all in $textPrimary (no colour coding)
Amount=I(row, {
  fill: "$textPrimary",   // WRONG: same colour for credit and debit
  content: "-$84.99"
})
// Without colour coding, the user has to read the sign character (+ or -)
// to understand each transaction. With colour coding, the read is instant.
// Financial convention: red = spend, green = receive. It is universal.
```

---

## Portfolio / performance card

For investment products: the performance summary card showing total value and returns.

```
PortfolioCard (frame, fill_container x fit_content, layout: vertical,
                gap: 4, padding: [24, 24],
                cornerRadius: 12,
                fill: "$surfaceDark")
├── PortfolioLabel (text, 13px, $fontBody, fill: "#A8A3B0",
│                    content: "Portfolio value")
├── TotalValue (text, 48px, fontWeight: 700, $fontMono,
│               fill: "#F0EEFC",
│               content: "$142,847.30")
│   // 48px. Investment totals are larger than checking account balances
│   // because the numbers are larger and need more visual weight.
├── ReturnBlock (frame, fit_content x fit_content, layout: horizontal,
│                alignItems: center, gap: 12)
│   ├── TotalReturn (text, 14px, $fontMono,
│   │                fill: "$positive",
│   │                content: "+$12,847.30")
│   └── ReturnPct (text, 14px, $fontMono,
│                   fill: "$positive",
│                   content: "(+9.9%)")
│   // Both absolute and percentage returns are shown.
│   // Both are monospace. Both use $positive or $negative.
└── SparklineChart (see chart-anatomy.md for sparkline spec)
    // 7-day portfolio trend. Small, 60px tall.
```

---

## Microcopy library

### Balance labels

| Generic (avoid) | This archetype |
|-----------------|----------------|
| Total Money | Available balance |
| Balance | Checking account |
| Account total | Total balance |
| Net Worth | Portfolio value |

### Transaction metadata

| Generic (avoid) | This archetype |
|-----------------|----------------|
| Transaction date | May 10 |
| Payment method | Debit card |
| Category: Food | Restaurants · $84.99 |
| Reference number | Ref: #MX-928471 |

### CTA labels on the balance card

| Generic (avoid) | This archetype |
|-----------------|----------------|
| Transfer money | Send |
| Add money | Add funds |
| View transactions | Transactions |
| Pay | Pay |

Keep labels short: this is a card on a dashboard, not a full-page flow. One word is often best.

### Delta labels

| State | Label format | Example |
|-------|-------------|---------|
| Positive this period | +$[amount] this month | +$842.00 this month |
| Negative this period | -$[amount] this month | -$214.50 this month |
| Zero change | No change this month | — |
| Percentage return | +[pct]% all time | +9.9% all time |

---

## Verification checklist

### Monospace rule

- [ ] **All monetary values, percentages, and numeric figures use `$fontMono`.**
  WHY: Monospace is the visual code for "precise financial figure." Proportional fonts make financial data look like marketing copy. This is the single most important specification in this archetype. If `$fontMono` is missing from any number in the design, the archetype has not been applied.

- [ ] **Transaction amounts use colour: `$negative` for outgoing, `$positive` for incoming.**
  WHY: Colour-coded amounts allow instant classification at scanning speed. Without colour, the user has to read the sign character to understand the direction of each transaction. Financial convention across all products (Robinhood, Mercury, bank statements) uses red = spend, green = receive.

### Balance card

- [ ] **Primary balance card fill is `$surfaceDark`, not `$accent`.**
  WHY: The balance card is the most important element on the page. An accent-coloured card looks like a CTA button. Dark (`$surfaceDark`) is the trust register: it reads as premium, stable, and authoritative. Mercury pioneered this pattern in modern fintech; it has become the convention.

- [ ] **Balance figure font size is 36–48px.**
  WHY: The balance is the most important number in the product. If it doesn't have visual weight proportional to its importance, the hierarchy is wrong. 36–48px at monospace font weight makes it immediately readable as "the number that matters."

### Transactions

- [ ] **Transaction rows are 56px tall.**
  WHY: Each transaction row contains a merchant logo/monogram, merchant name, date, card type, amount, and running balance. At 40px, the row is visually crowded. At 56px, each transaction is a readable unit. Financial transactions are not list items to be scanned in bulk; each one is a record the user might need to inspect.

---

## Contrast examples

### Example 1: Balance card (correct vs generic)

**Correct:**

```
balanceCard=I(panel, {
  type: "frame", name: "BalanceCard",
  layout: "vertical", gap: 8,
  padding: [28, 28],
  height: 180, width: "fill_container",
  cornerRadius: 12,
  fill: "$surfaceDark"   // dark, not accent
})
balanceFigure=I(balanceCard, {
  type: "text",
  content: "$23,419.50",
  fontFamily: "$fontMono",   // monospace
  fontSize: 40, fontWeight: 700,
  fill: "#F0EEFC"
})
```

Why this is right: dark background reads as premium and stable. Monospace at 40px reads as "precise financial data." The white-tinted text on dark has strong contrast.

**Generic:**

```
balanceCard=I(panel, {
  type: "frame",
  fill: "$accent",   // WRONG: accent colour
  cornerRadius: 12, padding: [24, 24]
})
balanceFigure=I(balanceCard, {
  type: "text",
  content: "$23,419.50",
  fontFamily: "$fontDisplay",   // WRONG: display/proportional
  fontSize: 40, fill: "#FFFFFF"
})
```

Why this is wrong: accent fill looks like a CTA button. Proportional font on the balance makes it look like a hero number on a landing page. The balance is not a headline; it is a precise financial figure. These two mistakes together produce the most common fintech AI-default output.

---

### Example 2: Transaction amount (correct vs generic)

**Correct:**

```
amount=I(transactionRow, {
  type: "text", name: "Amount",
  content: "-$84.99",
  fontFamily: "$fontMono",
  fontSize: 15, fontWeight: 600,
  fill: "$negative"   // red for outgoing
})
runningBalance=I(transactionRow, {
  type: "text",
  content: "$22,576.51",
  fontFamily: "$fontMono",
  fontSize: 12,
  fill: "$textSecondary"   // muted — contextual, not primary
})
```

Why this is right: monospace amount in red. Running balance in smaller monospace muted. The hierarchy is clear: amount is the primary read, running balance is contextual.

**Generic:**

```
amount=I(transactionRow, {
  type: "text",
  content: "-$84.99",
  fontFamily: "$fontBody",   // WRONG: proportional
  fontSize: 15, fontWeight: 600,
  fill: "$textPrimary"   // WRONG: no colour coding
})
```

Why this is wrong: proportional font on a transaction amount looks like a price tag in a shopping app. No colour coding means the user must parse the minus sign to understand this was a spend. In a list of 30 transactions, the cognitive load of parsing each sign is significant.
