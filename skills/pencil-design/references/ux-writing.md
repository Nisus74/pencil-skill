# UX writing

Copy is a design surface. The same button with the same chrome reads differently depending on the verb on it. The same error message can scare or reassure depending on the words. Designs ship with copy baked in; treating copy as an after-thought-handoff to PMs or writers is how *"Something went wrong. Please try again later."* makes it into production.

This reference is the depth behind SKILL.md's "AI copywriting clichés" anti-pattern. It covers button labels, error messages, empty states, headings, microcopy, the cliché vocabulary to refuse, and the replacements that read as specific to the product. For per-register tone differences, see [brand.md](brand.md) and [product.md](product.md).

## Button labels

Buttons name the outcome, not the action. The user's mental model is *"I want X to happen"*, not *"I want to interact with this control."*

| Generic (refuse) | Outcome-named (reach for) |
|---|---|
| Submit | Create the workspace |
| Save | Save changes to 'Q3 forecast' |
| Delete | Delete 5 items |
| Remove selected | Remove the 3 collaborators |
| OK / Confirm | Publish to production |
| Cancel | Keep editing |
| Apply | Apply the filter |

Rules:

1. **Lead with the verb, name the noun.** *"Delete invoice"* over *"Delete"*. The verb tells the user what happens; the noun confirms what it happens to.
2. **Quantify when the count matters.** *"Delete 5 items"* over *"Delete"*. Showing the number reduces second-guessing on destructive actions.
3. **Match the success state to the button copy.** If the button says *"Publish"*, the success toast says *"Published"*. Not *"Update successful"*.
4. **Negative actions are positive sentences.** *"Keep editing"* over *"Cancel"*. The user is choosing what they DO want, not what they're saying no to.
5. **Avoid "Click here", "Here", "Learn more" as link copy.** The link itself describes the destination. *"See the API reference"* over *"Learn more here"*.

## Error messages

Error messages follow a three-part structure: what happened, why it happened, what the user can do.

The bad: *"Something went wrong. Please try again."*
- What: nothing specific
- Why: nothing
- How to fix: try again (might not work)

The good: *"Couldn't reach the billing service. Connection timed out. Retry now, or contact support if this keeps happening."*
- What: couldn't reach billing service
- Why: connection timed out
- How to fix: retry, with an escalation path

### Error tone calibration

| Severity | Tone | Example |
|---|---|---|
| **User error, recoverable** | Direct, non-blaming | *"Email and password don't match. Reset password?"* |
| **User error, blocking** | Explain the constraint, give the path forward | *"Workspace names must be unique. 'design-team' is already used."* |
| **System error, recoverable** | Calm, give the retry | *"Couldn't save the draft. Retry"* |
| **System error, blocking** | Acknowledge, give the escalation | *"Billing service is down. Try again in a few minutes or contact support."* |
| **Destructive confirmation** | Specific consequence, irreversible flag | *"Delete the 'analytics-2025' workspace and all 234 designs in it. This can't be undone."* |

### Patterns to refuse

- *"Something went wrong"* with no detail
- *"An error occurred"* (the user can see that)
- *"Invalid input"* without saying what's invalid
- *"Try again later"* without a time estimate or escalation
- *"Oops!"* anywhere in an error message
- *"We're sorry, but..."* (apology without action)
- Stack traces or error codes alone (the user can't act on `E_TIMEOUT_503`)

## Empty-state copy

The four empty-state types from [product.md](product.md) each take a different copy shape.

### First use
The user has never used this surface. The copy is onboarding-shaped: what is this, why does it matter, what's the first meaningful action.

*Bad:* *"No invoices yet."*
*Good:* *"You'll see invoices here once you start billing. Send your first invoice to get going."*

### No results
A filter or search returned nothing. Acknowledge what was searched; offer the way out.

*Bad:* *"No results."*
*Good:* *"No invoices from May 2026. Clear filters to see all 248 invoices."*

### No permission
The user can't see content here. Explain what they're missing without exposing details they shouldn't see, and name the path to access.

*Bad:* *"Forbidden."* / *"You don't have permission."*
*Good:* *"Only workspace admins can see billing. Ask your admin if you need access."*

### Post-action
The user cleared a queue or completed a list. Acknowledge the moment; offer next-meaningful-thing.

*Bad:* *"No items."*
*Good:* *"Inbox zero. Nothing else needs your attention."*

## Section headings

Headings are scannable signposts, not clever copy. The user reads headings to navigate; clever headings slow that down.

### Reach for
- Specific nouns: *"Billing history"* over *"Money matters"*
- Action verbs when the section is about doing something: *"Invite teammates"* over *"Team"*
- Domain language the user already uses: *"Tickets"* if the product uses that word, *"Issues"* if it uses that one

### Refuse
- Cute alliteration: *"Beautiful billing"*, *"Stellar settings"*
- One-word headings that hide content: *"Overview"* (over what?), *"Information"*, *"Details"*
- Question-form headings as a default: *"Want to invite your team?"* reads as marketing in a product surface
- Marketing-style emoji or punctuation: *"Settings ✨"*, *"Your Profile!"*

## Microcopy specificity

Domain-specific copy outperforms generic copy at every opportunity. The single highest-leverage move in UX writing is naming things in the vocabulary the user thinks in.

| Generic (refuse) | Domain-specific (reach for) |
|---|---|
| *"How your product performed over the last 7 days"* | *"API calls this week"* |
| *"You have 3 notifications"* | *"3 pull requests need review"* |
| *"Search"* | *"Search invoices, customers, or transaction ID"* |
| *"Last activity"* | *"Last commit: 2 hours ago"* |
| *"Account settings"* | *"Your billing and team settings"* |

For brand pages, microcopy lives in CTAs, captions, alt text, form-field placeholders. The same specificity rules apply; brand copy can be more expressive in tone but still stays grounded in the brand's actual vocabulary.

## The AI cliché list (refuse on sight)

These words and phrases are over-represented in AI-generated copy. Strike them from any text you author:

### Severity 1 (any one of these flags the copy as AI)
- Elevate / Elevated
- Seamless / Seamlessly
- Unleash / Unleashing
- Empower / Empowering
- Revolutionize / Revolutionary
- Cutting-edge
- Next-gen / Next-generation
- Transform / Transformative
- Game-changing / Game-changer

### Severity 2 (one or two in a long piece is borderline; three is a rewrite)
- Robust
- Comprehensive
- Holistic
- Streamline / Streamlined
- Foster / Fostering
- Leverage (as a verb)
- Utilise
- Facilitate
- In today's fast-paced world
- The power of
- The future of
- At the intersection of

### Severity 3 (overused but sometimes the right word; use sparingly)
- Beautiful (only if the design genuinely is)
- Powerful (only if you can name the specific capability)
- Simple (only if the user would also describe it that way)
- Easy (the user decides what's easy; usually empty)
- Magical (almost never)

### Replacement strategy
Most slop replacements are: *say the specific thing in fewer words.*

- *"Elevate your workflow"* → *"Ship work faster"* or *"Replace 4 tools with 1"*
- *"Seamless integration"* → *"Connects to GitHub in 2 clicks"*
- *"Unleash the power of AI"* → *"Generate test cases from your code"*
- *"Empower your team"* → *"Let designers ship without engineering review"*
- *"Cutting-edge technology"* → name the technology

The pattern: the slop word is a wrapper around a hollow claim. Replace it with a specific claim.

## Per-register guidance

- **Brand.** Copy can carry more personality, opinion, voice. The brand's tone of voice is half the design. CTAs are persuasive, headlines are confident, body can have rhythm.
- **Product.** Copy is functional. Specific, scannable, neutral in tone. The user is working; the copy stays out of the way except where it needs to inform or warn.

A brand microcopy that reads *"Let's make something beautiful"* on a CTA is fine on a landing page. The same copy on a save button in an app surface reads as out-of-place corporate friendliness.

## Pencil-specific

### Text content lives in the design

Text nodes in `.pen` carry their content in the `content` property:

```
T1 = Insert("parent", {
  type: "text",
  content: "Delete 5 items",
  fontFamily: "$fontBody",
  fontSize: 14,
  fontWeight: 500,
  fill: "$text"
})
```

This means the design carries the copy. There's no *"lorem ipsum and the writer fixes it later"* fallback; the content sits next to the layout in the same `.pen` file. Write copy as you build; don't defer. Copy behaviour during handoff is the same as design behaviour: what's in the file ships.

### Placeholder names

Per SKILL.md's anti-patterns: don't ship placeholder names like *"John Doe"*, *"Acme Corp"*, *"Lorem Ipsum"*. Use plausible, context-appropriate content or `Generate(node, "ai", ...)` for imagery. For copy, name people with real-sounding names drawn from the design's plausible user base (*"Aiko Watanabe"*, *"Daichi Ito"*, *"Sophia Lee"*). Recognise that placeholder names age the design instantly the moment they reach a real user.

### Empty-state copy as variants

When building an `EmptyState` component (recommended in [product.md](product.md)), build the four empty-state types (first-use, no-results, no-permission, post-action) as variants with different copy slots, not four hand-built surfaces. The copy variation lives in the component, not in the page.

### Audit copy as you go

When you read a node via `batch_get` and find generic copy (*"Click here"*, *"Learn more"*, *"Save"*), fix it in the same `batch_design` call. Like the `context` backfill rule in SKILL.md: the cost is one extra op; the value is a permanent improvement to the file.
