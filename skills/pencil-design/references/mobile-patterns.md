# Mobile patterns

Mobile design isn't a smaller desktop. It's a different posture, a different input, and a different set of native conventions the user already knows. Most AI defaults treat mobile as 'the same screen, narrower'. The result reads as a website jammed into a phone: thumb-hostile hit zones, sheets that ignore detents, content hidden behind the notch, and gestures that fight the OS.

This file gives the agent the vocabulary to design like the platform expects: safe areas honoured, sheets used where they fit, haptics called out, native gestures respected.

**What this file owns:** safe-area handling (notch, home indicator, dynamic island), bottom sheets vs modals, sheet detents, pull-to-refresh, swipe gestures, haptic feedback, tab bars, native iOS / Android conventions, floating action buttons, keyboard avoidance for inputs.

**What this file does NOT own:** the project's mobile breakpoint commitments (those live in [`assets/design-system/mobile.md`](../assets/design-system/mobile.md)). State taxonomies for loading and error live in [`states.md`](states.md). Navigation patterns and back-stack model are in [`flows.md`](flows.md). Hit targets and focus management are in [`interactions.md`](interactions.md). ARIA, screen reader, and dynamic type are in [`accessibility.md`](accessibility.md).

## When to load this file

- The user asks for an iOS app, Android app, mobile web, responsive design below ~768px, or names a platform (iPhone, Pixel, iPad).
- The design includes a bottom sheet, action sheet, modal on mobile, tab bar, FAB, swipe action, or pull-to-refresh.
- The user says *safe area*, *notch*, *home indicator*, *detent*, *haptic*, *swipe*, *back gesture*, *keyboard*, *accessory bar*, or *dynamic island*.
- You're auditing a desktop-first design that's being adapted to mobile and the chrome doesn't fit.
- A native-feeling app is the goal and the design currently looks like a web view.

## Safe areas

Modern phones have hardware that intrudes on the screen: the notch (iPhone X through 14), the dynamic island (iPhone 14 Pro and newer), the home indicator bar (every iPhone since X), and the status bar everywhere. Content placed under any of these is invisible or unreachable.

The browser exposes safe areas via CSS environment variables:

```css
.app-shell {
  padding-top: env(safe-area-inset-top);
  padding-right: env(safe-area-inset-right);
  padding-bottom: env(safe-area-inset-bottom);
  padding-left: env(safe-area-inset-left);
}
```

Rules:

- **Top inset** covers the status bar plus the notch or dynamic island. On iPhone 16 Pro it's 59pt; on a notch-less iPhone SE it's 20pt. Don't hardcode either.
- **Bottom inset** covers the home indicator (34pt on every modern iPhone). Tab bars, sticky CTAs, and the bottom of bottom sheets all sit above this inset.
- **Left and right insets** matter in landscape on iPhone (the notch and curved corners). Vertical apps can usually ignore them; full-bleed media must respect them.
- **Use `viewport-fit=cover`** in the meta tag so the page actually fills the safe-area region: `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">`. Without it, `env()` returns 0 and your insets do nothing.
- **Never put a tap target in the bottom 20pt** of the screen. The home-indicator gesture lives there; iOS swallows the first tap.

For native iOS and Android, the platform handles safe areas through `safeAreaInsets` (UIKit / SwiftUI) and `WindowInsets` (Jetpack Compose). The same discipline applies: no chrome under the system bars.

## Bottom sheets vs modals

Both are overlays. The choice depends on whether the underlying context still matters.

**Bottom sheets** keep the underlying screen partially visible, slide up from the bottom, and let the user dismiss with a downward swipe. They're for selection, secondary actions, and decisions that don't block the main flow. Apple Mail's reply composer, Apple Maps' place card, and Linear iOS's filter panel all use sheets.

**Modals** take the full screen (or close to it), block everything underneath, and demand resolution before the user can return. They're for blocking decisions, one-shot tasks, and flows where the underlying context shouldn't distract. Sign-in, payment confirmation, and full-screen editors are modals.

Pick a sheet when:

- The user is choosing from a finite list (filter, sort, share target).
- The action is reversible and lightweight (mute notifications, mark as read).
- The underlying context informs the decision (replying to a thread you can still see).

Pick a modal when:

- The action is consequential and shouldn't be dismissed accidentally (delete account, confirm payment).
- The flow has multiple steps that wouldn't fit in a sheet without scrolling becoming hostile.
- The decision benefits from focus, with the rest of the app removed from the visual field.

A common mistake is shipping every secondary action as a modal. It feels heavy. The user can't peek at what they're acting on. Default to a sheet, escalate to a modal only when blocking is genuinely required.

## Sheet detents

iOS 16 introduced custom detents for `UISheetPresentationController`; web sheet libraries (Vaul, Radix) followed. A detent is a stop position the sheet rests at when the user drags it.

The standard detents:

- **Peek** (around 120-200pt of bottom slice, roughly 15-25% of the screen). Right for ambient context: a now-playing bar, a Maps place card, a Find My location banner.
- **Half** (50% of the screen). The default for selection sheets, share sheets, and most secondary actions. The underlying context stays visible above.
- **Full** (full screen, often with a small gap at the top). Right for sheets that turn into editors, long lists, or anything that needs the full canvas. The user can swipe down to collapse back.
- **Custom** (any specific height). iOS 16+ supports arbitrary detents; use them when content has a natural height that none of the standard stops match.

Default detent per use case:

| Use case | Default detent | Notes |
|---|---|---|
| Filter / sort | Half | The user picks, the sheet closes. |
| Share target picker | Half | Matches iOS native share sheet. |
| Now-playing / mini-player | Peek | Tap to expand to full. |
| Compose / reply | Full | Editor needs the canvas. |
| Place card / detail peek | Peek with Half on tap | Apple Maps pattern. |
| Action sheet (3-5 destructive options) | Half or fitted | Don't overshoot the content. |

Document the available detents and the default in the sheet's `context`: *"Detents: peek (180pt), half, full. Default: half. Drag handle visible. Dismissable by swipe-down."*

## Pull-to-refresh

The user knows the gesture. They expect it on lists, feeds, inboxes, and anywhere the content might have changed since they last looked. They don't expect it on settings, forms, or single-item views.

Where it's expected:

- Inboxes (Apple Mail, Gmail, Slack DMs).
- Feeds (Twitter / X, Instagram, Reddit, Discord channel scrollback).
- Lists that fetch from a server (Linear inbox, Things today list with cloud sync).
- Notification centres.

Where it's not:

- Settings pages. Settings don't change underneath the user; pull does nothing.
- Forms in progress. Pull would either ignore the gesture or, worse, lose the user's input.
- Single-item detail views (a single email, a single issue). The detail isn't a list.
- Anything below the fold of a long-scroll page. Pull only fires from the very top.

Visual conventions: a spinner appears at the top as the user pulls past a threshold (around 60pt), holds at maximum stretch, then snaps back when the request resolves. Use the platform's native indicator if you can; custom indicators usually feel slower than they are. Linear iOS, Apple Mail, and Things 3 all use the platform spinner.

## Swipe gestures

Two distinct gestures, both standard on iOS, both with conflict potential:

**Edge swipe (back gesture).** Swiping right from the left edge of the screen pops the current view in iOS navigation. The system reserves roughly the leftmost 20pt for this gesture. Don't put a swipeable element flush against that edge or the user will trigger the back nav by accident.

**Row swipe (action gesture).** Swiping left or right on a list row reveals contextual actions. Apple Mail uses left-swipe for Archive (short swipe) or Trash (long swipe), right-swipe for Mark Read / Flag. Linear iOS uses similar conventions on inbox items.

Rules:

- **Reserve the left edge for the back gesture** when the screen is part of a navigation stack. If you need a left-swipe-from-edge on a row, position the row at least 20pt from the screen edge or the gestures will fight.
- **Right-swipe on a row** for non-destructive actions (mark read, flag, snooze); reserve left-swipe for destructive ones (archive, delete). Match Apple Mail's conventions; they're the de facto standard.
- **Long-swipe-to-commit.** A short swipe reveals the action button; a full swipe across the row commits the action without an extra tap. Apple Mail does this for Archive; users have learned it.
- **Surface the swipe action** somewhere reachable for users who don't know the gesture or can't perform it (motor accessibility). A long-press menu or a row's overflow button must offer the same actions.

Document in the row component's `context`: *"Swipe-to-archive enabled. Right-swipe reveals Archive action; full right-swipe commits. Long-press menu offers same action for accessibility."*

## Haptic feedback

Haptics are the difference between an interface that feels alive and one that feels rendered. iOS gives you `UIImpactFeedbackGenerator` (light, medium, heavy), `UISelectionFeedbackGenerator` (picker tick), and `UINotificationFeedbackGenerator` (success, warning, error). Web exposes a subset via the Vibration API; Capacitor / React Native bridge to native.

Where to call out haptics in the design:

- **Success haptic** on confirmation: payment sent, message delivered, photo uploaded. The visual confirmation pairs with a short success buzz.
- **Selection haptic** (the light tick) on picker movement, segmented-control changes, and value-step adjustments. Cash App's amount slider is the reference.
- **Error haptic** (the warning pattern) on validation failure: wrong PIN, payment declined, biometric mismatch. Pairs with the visual error state.
- **Light impact** on toggle changes and confirm-tap of destructive actions. The user feels they did the thing.

Where to skip haptics:

- Routine taps on regular buttons (the system's default tap haptic is enough).
- Scrolling and pagination (the OS handles momentum haptics).
- Background events the user didn't initiate.

Never let an important state change happen silently. If the toggle for *Do Not Disturb* turns on with no haptic, no animation, and no sound, the user can't tell they actually turned it on without staring at the screen. Cash App, Things 3, and Apple Wallet all use haptics liberally for confirmations.

Document in the component's `context`: *"Tap fires light impact haptic. On success, fires success notification haptic paired with the checkmark animation."*

## Tab bars

Bottom tab bars are the default top-level navigation on iOS and Android.

Rules:

- **Five items maximum.** Four is better. Past five, users can't scan and the touch targets get cramped. If you have more than five sections, demote the rest to a *More* tab or a profile menu.
- **Semantic order.** Most-used tab leftmost, profile / settings rightmost. Don't reorder dynamically; users build muscle memory.
- **Current state visible.** The active tab uses the filled icon variant plus the brand colour for both icon and label. Inactive tabs use the outline icon and a muted label colour. Apple Mail, Apple Music, and Slack iOS all use this pattern.
- **Don't hide labels at default text size.** Icon-only tab bars are unreadable for first-time users and a regression for accessibility. Labels appear on every tab; they shrink with Dynamic Type but never disappear.
- **Respect the bottom safe-area inset.** The tab bar sits above the home indicator. The bar's background extends to the screen edge; the tap targets stop at the inset.

Don't overload a tab with a badge that means three different things. *9* could be unread messages or pending invites or new releases; pick one and stick to it.

## Native conventions per platform

iOS and Android have well-trained user expectations. Deviating costs you; following them makes the app feel native.

**iOS conventions to respect:**

- **Back swipe from left edge** pops the navigation stack. Always available unless you have an extremely good reason to disable it (an unsaved-form guard, with explicit confirmation). See [`flows.md`](flows.md) for the back-stack model.
- **Share sheet** for sharing anything. Use `UIActivityViewController` or the web Share API; don't roll your own list of share targets. The user knows the share sheet and trusts it.
- **Action sheet** (`UIAlertController` with `.actionSheet`) for 3-5 contextual options where one is destructive. Slides up from the bottom. Don't use action sheets for navigation; they're for choices.
- **Large title** on the top-level screen of a navigation stack. Collapses to a regular nav bar title on scroll. The default in iOS Mail, Notes, Settings.
- **Pull-to-refresh** on lists, as covered above.

**Android conventions to respect:**

- **Bottom navigation bar** for top-level navigation, matching the tab bar pattern. Material 3 spec.
- **FAB** (floating action button) for the screen's primary contextual action: compose in Gmail, new event in Calendar.
- **Snackbar** for transient feedback (saved, deleted with undo). Slides up from the bottom edge, auto-dismisses after 4-7 seconds. Material 3 prefers snackbars over toasts because snackbars can carry an action.
- **Hamburger drawer** for secondary navigation (account switcher, less-used sections). Don't use it for primary nav; that's the tab bar's job.
- **System back gesture** (edge swipe on Android 10+) and the back button (older devices) both pop the activity stack. Predictive back animations (Android 14+) preview the destination.

When to deviate: when you're building a cross-platform app with a deliberate brand identity that's bigger than either platform's defaults (Spotify, Instagram). Even then, respect the platform's gesture grammar; only the visual chrome differs.

## Floating action buttons

A FAB is the screen's primary contextual action, raised above the canvas, usually bottom-right or bottom-centre.

Use a FAB when:

- There's exactly one obvious next action on the screen (compose email, add event, new note).
- The action is high-frequency. Gmail's compose, Calendar's new event, Notion's new page.
- The screen is content-heavy and the action would otherwise compete with the content for attention.

Don't use a FAB when:

- There are multiple competing actions. The FAB demands attention; splitting it dilutes it.
- The action is low-frequency. A FAB for *Settings* would be louder than the function deserves.
- The screen is a form or a single-task flow. The submit button is the primary action; a FAB would compete.
- You're on iOS and trying to import an Android pattern wholesale. iOS doesn't have a FAB convention; the equivalent is a top-right *+* button in the nav bar (Apple Notes, Apple Calendar).

A speed-dial FAB (tap the FAB to reveal 3-5 sub-actions) is acceptable for genuinely multi-action surfaces (Gmail's compose menu on some Android revisions). Don't ship one without a single primary action also visible.

## Input keyboard avoidance

When the keyboard appears, it covers the bottom half of the screen. If the focused input is in that bottom half, the user can't see what they're typing.

Rules:

- **Scroll the focused input into view** above the keyboard. The OS does this automatically for native inputs; web requires manual intervention via `scrollIntoView({ block: 'center' })` on the input's `focus` event, or a CSS-based viewport adjustment.
- **Accessory bar** above the keyboard with a *Done* button. iOS exposes this via `inputAccessoryView`. For multi-field forms, add *Previous / Next* buttons too so the user can move between fields without dismissing the keyboard.
- **Dismiss on outside tap** for forms where dismiss is expected (search, comment composer). The user taps anywhere outside the input, the keyboard slides down. Don't dismiss on scroll; that fights the scroll-into-view behaviour.
- **Adjust the layout** so any sticky CTA (Continue, Save) sits above the keyboard. iOS handles this for native UIs; web needs `interactive-widget=resizes-content` in the viewport meta plus a layout that responds to the visual viewport.
- **Disable autocorrect and autocapitalize** for emails, usernames, and codes. Already covered in [`forms.md`](forms.md), but mobile is where it matters most. Spellcheck on a verification code creates red squiggles under every entry.

For native iOS and Android, the platform's `KeyboardAvoidingView` (React Native) and `WindowInsets.ime` (Compose) handle most of this. Document the expectation in the screen's `context`: *"On input focus, scroll input into view above keyboard. Continue button stays visible above keyboard. Done button on accessory bar dismisses."*

## Pencil expression

Mobile design in `.pen` files is structured the same way as desktop, with extra discipline at three points:

- **Breakpoint commitment.** The project's mobile breakpoint (typically `≤768px` or `≤640px`, set in [`assets/design-system/mobile.md`](../assets/design-system/mobile.md)) is the line at which layouts collapse from split to stacked. Don't drift from the project's chosen value.
- **Safe-area frame.** The outermost frame of any mobile screen carries `context: "Safe-area aware. Top inset: status bar + notch / dynamic island. Bottom inset: home indicator. viewport-fit=cover assumed."`. The engineer reads this and wires `env(safe-area-inset-*)` correctly.
- **Gesture markers in `context`.** Whenever the screen or component supports a swipe, pull, or long-press, name the gesture in the `context`. Examples: *"Swipe-to-archive enabled. Right-swipe reveals Archive action."*; *"Pull-to-refresh enabled at top. Triggers re-fetch of inbox."*; *"Long-press shows context menu with Mark Read / Flag / Move."*. The agent reads these markers later when iterating; the engineer reads them when implementing.
- **Sheet components with detents.** A `BottomSheet` reusable carries its supported detents in `context`: *"Detents: peek (180pt), half, full. Default: half. Drag handle visible. Dismissable by swipe-down."*. Variants per detent (`BottomSheet_Peek`, `BottomSheet_Half`, `BottomSheet_Full`) make the design intent visible at a glance.
- **Tab bar component.** Named `TabBar` with one frame per tab. Each tab carries its own `context`: *"Active state: filled icon, brand colour label. Tap fires selection haptic."*. The bar's outer frame names the safe-area inset: *"Sits above bottom safe-area inset; background extends to screen edge."*.
- **Haptic markers.** When a component should fire a haptic, name it: *"Tap fires light impact haptic. On success, fires success notification haptic."*. Don't bury haptics in the design tokens; they're behavioural, not visual.

When the project doesn't yet have `BottomSheet`, `TabBar`, or `MobileScreen` reusables in its `.lib.pen`, build them inline the first time you need them, then surface to the user: *"This mobile shell looks reusable. Should I add `BottomSheet`, `TabBar`, and `SafeAreaShell` to your library?"*

## Anti-patterns

These read as desktop-blind designs and should be fixed in passing:

- **Content under the notch or dynamic island.** A header logo placed at `top: 0` without the safe-area inset is invisible on most modern iPhones.
- **Tap target in the home-indicator zone.** Anything in the bottom 20pt is unreachable; iOS swallows the tap.
- **Modal where a sheet would do.** A full-screen modal for picking a sort order is heavy. Use a half-detent sheet.
- **Sheet with no drag handle.** Users learn the gesture from the visible affordance. A sheet without a handle reads as a stuck modal.
- **Pull-to-refresh on a settings page.** Settings don't refetch. The gesture does nothing and confuses the user.
- **Row swipe flush against the left screen edge.** The OS back gesture wins; the user accidentally pops the nav stack.
- **Tab bar with six or seven tabs.** Past five, scanning and tapping both fail. Demote to a *More* tab.
- **Icon-only tab bar at default text size.** Unreadable for first-time users and a Dynamic Type regression. Labels stay visible.
- **FAB on a form screen.** The form has its own primary action (Submit). The FAB competes.
- **Input that the keyboard covers on focus.** The user can't see what they're typing. Scroll into view.
- **Silent state change for an important toggle.** No haptic, no animation, no confirmation. The user can't tell they did the thing.

## Sources

- **Apple Human Interface Guidelines (iOS 18 / iPadOS 18 / visionOS 2)**: https://developer.apple.com/design/human-interface-guidelines : safe-area handling, sheet presentation and detents (UISheetPresentationController), tab bar conventions, action sheet vs share sheet, haptic feedback (UIFeedbackGenerator), back-swipe gesture, large title behaviour, accessory bar.
- **Material 3 (Google)**: https://m3.material.io : Android navigation bar, FAB usage and placement, snackbar over toast, predictive back gesture (Android 14+), bottom sheet detents.
- **WCAG 2.2 (ISO/IEC 40500:2025)**: hit-target minimums (Success Criterion 2.5.8 Target Size, 24x24 CSS pixel minimum), accessible alternatives to swipe gestures.
- **Real-world exemplars accessed 2025/2026**: Linear iOS (inbox swipe actions, sheet filters), Apple Mail (row swipe, pull-to-refresh, accessory bar), Things 3 (haptic feedback, single-detent sheets), Cron / Notion Calendar iOS (sheet detents on event creation), Apple Maps (peek detent on place cards), Cash App (selection haptics, success haptics on payment), Slack iOS (tab bar, snackbar-equivalent toasts), Discord iOS (bottom sheet for emoji picker), Notion iOS (full-screen modal for editor), Arc Search (gesture-first navigation), Stripe iOS (modal for payment confirmation).

## See also

- [`states.md`](states.md): loading, error, and empty states for mobile lists, sheets, and pull-to-refresh.
- [`flows.md`](flows.md): navigation patterns, back-stack model, deep links into mid-flow screens.
- [`interactions.md`](interactions.md): hit targets, focus management, keyboard everywhere principles.
- [`accessibility.md`](accessibility.md): ARIA on mobile, screen reader (VoiceOver / TalkBack) conventions, Dynamic Type behaviour.
- [`forms.md`](forms.md): mobile input attributes, font-size minimums, keyboard discipline.
- [`composition-patterns.md`](composition-patterns.md): slot design for `BottomSheet`, `TabBar`, and `MobileScreen` reusables.
- [`assets/design-system/mobile.md`](../assets/design-system/mobile.md): the project's mobile breakpoint commitments, touch-target sizes, and platform-specific tokens.
- [`assets/design-system/motion.md`](../assets/design-system/motion.md): sheet present / dismiss timing, swipe-action commit thresholds, haptic-paired animation curves.
