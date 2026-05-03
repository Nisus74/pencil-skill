Great — happy to walk through the plan before I start designing. Here's how I'd approach a login screen in Pencil, step by step.

## 1. Understand the context first

Before I draw anything, I want to know what surface I'm designing for. A few quick questions I'd answer (or ask you):

- **Platform / form factor?** Web (desktop + responsive), or mobile (iOS/Android)? This drives sizing, hit targets, and whether the form is centered in a card or fills the screen.
- **Existing design system?** Is there already a Pencil document with brand colors, typography, spacing tokens, and components I should match? If yes, I'll reuse those rather than inventing new ones.
- **Brand tone?** Playful, enterprise, fintech-serious, consumer-friendly? Affects color, corner radius, type, and density.
- **Auth context?** Is this a standalone product or part of a suite (e.g., social sign-in, SSO, "remember me", links to sign-up)? You only mentioned email + password + forgot, so I'll keep scope tight to that.

If you don't have answers handy, I'll make reasonable defaults (web, neutral modern aesthetic, 8pt spacing, rounded inputs) and call them out.

## 2. Set up the Pencil document

- Open the active `.pen` file (or create a new one if we're greenfield).
- Check the editor state so I know the current selection, page, and any frames already there.
- Pull project guidelines (colors, type scale, spacing, component library) so the screen feels native to the system.

## 3. Sketch the structure on paper (mentally) before placing nodes

The login screen is small but has a clear hierarchy. I'd plan the layout as:

```
[Centered card / column, ~360–400px wide on desktop]
  Logo / brand mark              (optional, top)
  Heading: "Sign in"             (H1/H2)
  Subheading / helper text       (optional, muted)

  Email field
    Label: "Email"
    Input (type=email, autocomplete=email)

  Password field
    Label: "Password"            (with "Forgot password?" link aligned right)
    Input (type=password, autocomplete=current-password)
    Show/hide toggle (optional)

  Primary button: "Sign in"       (full-width)

  Footer: "Don't have an account? Sign up"   (optional, you didn't ask for it)
```

Vertical rhythm: consistent spacing between groups (e.g., 16px within a field, 24px between fields, 32px before the button).

## 4. Decide the component approach

I'd prefer to **reuse existing components** from your Pencil library if they exist (Input, Button, Link, FormField). I'd search the document for those first. If none exist, I'll build the screen with primitive nodes and flag where it'd be worth promoting them to reusable components later.

## 5. Build it in Pencil

Concretely, this is what I'd do with the tools, in order:

1. **Frame** — create a frame sized to the target (e.g., 1440×900 desktop, or 390×844 mobile) with the page background.
2. **Card container** — auto-layout column, centered, padding ~32px, white surface with subtle border or shadow, radius matching the system.
3. **Header block** — logo (placeholder if none provided) + heading + optional subheading.
4. **Form fields** — for each (email, password): label row + input. The password label row is a horizontal layout with the label on the left and "Forgot password?" link on the right.
5. **Submit button** — primary style, full width, label "Sign in".
6. **Spacing pass** — verify the vertical rhythm is consistent.
7. **States** — at minimum, sketch focus and error states for the inputs and a disabled state for the button. Even if you don't ask for them, they're cheap to add and make the design real.

## 6. Validate before handing off

- Accessibility quick check: labels are real labels (not placeholder-only), tap targets ≥ 44px, sufficient contrast on text and the button.
- Responsive check: does the card behave reasonably at narrow widths? On mobile, the card typically becomes full-width with side padding.
- Copy check: "Sign in" vs "Log in" — pick one and stay consistent with the rest of the product. "Forgot password?" with the question mark is standard.

## 7. Confirm with you

Once a v1 is on the canvas, I'd take a screenshot and walk you through it so you can react before I polish. Faster to course-correct early than to over-invest in details.

---

**Before I start, a couple of quick decisions I'd like from you:**

1. Web or mobile (or both)?
2. Any existing Pencil doc / design system to match, or starting fresh?
3. "Sign in" or "Log in" wording?
4. Anything else on the screen (logo, sign-up link, social auth, "remember me")? Or strictly the three elements you listed?

If you'd rather I just pick reasonable defaults and go, say the word and I'll start building.
