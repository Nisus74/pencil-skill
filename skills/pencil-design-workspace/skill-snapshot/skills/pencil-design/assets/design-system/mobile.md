# Mobile

Native-mobile patterns. **Delete this file if your project doesn't ship a native or mobile-web app** — it's noise for desktop-only products.

The default `layout.md` covers responsive web at a mobile breakpoint (390 × 844). This file covers the patterns that *only* matter when the product is genuinely mobile-first: native iOS, native Android, React Native, Flutter, SwiftUI, or a mobile-web app that should *feel* native.

## Navigation chrome

| Pattern | When to use | Notes |
|---------|-------------|-------|
| **Tab bar** (bottom) | 3–5 top-level destinations | The default for native apps. ≤ 5 items; > 5 means rethink the IA. iOS calls this `UITabBar`, Android calls it `BottomNavigationBar`. |
| **Top app bar** | Single page with a clear title and 0–2 actions | Always pair with safe-area inset (notch / Dynamic Island). |
| **Drawer / hamburger** | When tab bar runs out of room AND the destinations are genuinely peer-level | Pattern of last resort. Buries navigation; reserve for less-frequently-used sections. |
| **Sheet** (bottom or modal) | Focused subtask, optionally dismissible by drag | Use for filters, share, single-task forms. Includes a drag handle if dismissible. |
| **Full-screen modal** | Multi-step task that needs total focus (e.g. checkout flow) | Has a clear close affordance (X top-left on iOS, ✕ top-right on most flows; pick one and stay consistent). |

**Rule:** pick a primary navigation pattern *per app*, not per screen. Mixing tab bar on some screens and drawer on others is jarring.

## Touch targets

- **iOS minimum:** 44 × 44 pt.
- **Android minimum:** 48 × 48 dp.
- **Spacing between adjacent targets:** ≥ 8.

Apply even when the visual element is smaller (e.g. a 16 × 16 ✕ icon needs 28pt of padding to hit 44pt). Pencil components for mobile should bake this in — don't reinstate it on every screen.

## Safe areas

Every full-screen frame must respect:

- **Top inset** (status bar + notch / Dynamic Island).
- **Bottom inset** (home indicator on iPhone, gesture pill).
- **Left/right insets** in landscape on devices with notches.

In Pencil:

- Use a top-level frame matching the device dimensions (e.g. `390 × 844`).
- Place a `SafeAreaTop` (h: 47 for iPhone) and `SafeAreaBottom` (h: 34) as fixed-height frames.
- Lay content inside the safe region.

Code-side: `safe-area-inset-top/bottom/left/right` (CSS) or `SafeAreaView` (React Native) / `SafeArea` (SwiftUI).

## Gestures

| Gesture | Conventional meaning | When to use |
|---------|---------------------|-------------|
| **Tap** | Activate | Default. |
| **Long-press** | Context menu / drag handle | Reserve for power-user features; don't make it the only way to do something. |
| **Swipe horizontal on row** | Reveal row actions (delete, archive, pin) | List items in inbox-shaped UIs. |
| **Swipe down on top of screen** | Pull-to-refresh | Lists, feeds. Always pair with a visible loader. |
| **Swipe down on a sheet** | Dismiss | Bottom sheets, modals where it makes sense. |
| **Swipe right at left edge** | Back (iOS interactive pop) | Free with native nav stacks; preserve it — don't intercept. |
| **Pinch** | Zoom | Photos, maps. Don't fake it on regular content. |

**Rule:** every gesture must have a non-gesture equivalent. Swipe-to-delete also needs a button-tap path (long-press menu, edit mode). Gesture-only is an accessibility regression.

## Keyboard handling

- The keyboard appears over content. Scroll the focused field into view; don't let it land behind the keyboard.
- Dismiss the keyboard on: tapping outside an input (where it makes sense), swipe-down on a scroll view, or a clear "Done" button on the keyboard.
- Use the right keyboard type per input: `numeric` for numbers, `email` for emails, `tel` for phones, `url` for links, `decimal-pad` for currency.
- Autocomplete tokens: `username`, `email`, `current-password`, `new-password`, `one-time-code`, `street-address`, etc. These let password managers and autofill work — skipping them is hostile.

## Haptics

A small set of system haptics, used sparingly:

| Event | Haptic |
|-------|--------|
| Toggle / switch flip | Light impact |
| Successful primary action (saved, sent) | Success notification |
| Destructive action confirmed | Medium impact |
| Error / failed validation | Error notification |
| Selection change (picker, tab swap) | Selection (rigid) |

Don't haptic on every tap. Haptics on hover-equivalent or scroll feels broken.

## Platform conventions vs custom

When in doubt, follow platform convention:

| Concern | iOS convention | Android convention |
|---------|---------------|-------------------|
| Back button | Top-left chevron, plus edge swipe | Top-left arrow, plus system back gesture |
| Settings icon | Gear | Gear |
| Modal dismiss | "Cancel" left, "Done"/primary right | "✕" top-left or back-arrow |
| Action sheet | Bottom-sliding sheet | Bottom-sheet or dialog |
| Alert with destructive action | Red text on confirm button | Red filled button |

Cross-platform apps (React Native, Flutter): pick **one** convention as the design source of truth and mirror as needed at runtime, rather than designing two parallel systems. Reduces drift.

## Performance feel

Mobile makes performance gaps visceral. A few rules:

- **First content paint < 1s on 4G.** If you can't, ship a skeleton.
- **Tap response < 100ms.** A button that takes 300ms to visibly respond feels broken.
- **Animations at 60fps.** If a transition janks, simplify it (cut filter blurs, large shadows, layout-triggering properties).
- **Avoid full-page loaders for partial updates.** A spinner that blocks the whole screen for a list refresh is worse than the old data + a top-bar progress indicator.

## What this file doesn't cover

- Push notifications (system / OS concern).
- Deep linking (router/runtime concern).
- App Store / Play Store screenshots (those are marketing assets — see `imagery.md` if present).
- Specific cross-platform framework idioms — see your code-export.md.
