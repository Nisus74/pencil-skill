# Performance design

Performance is a design property. It's decided in the layout, the asset choices, the loading choreography, and the sequencing of bytes; not in a final round of optimisation. Designs that ignore performance ship as designs that punish slower devices and weaker networks, which is most of the user base.

**What this file owns:** network budgets for common request types, Core Web Vitals targets and what they measure, virtualisation rules for long lists, image and font loading discipline, theme-color metadata, the skeleton-versus-spinner decision, perceived-performance patterns, and how to surface all of it in Pencil `context`.

**What this file does NOT own:** the visual design of skeleton, spinner, and loading states (that's [`states.md`](states.md)). The timing rules for when to show or hide a loading indicator (that's [`interactions.md`](interactions.md) § Loading state timing). The streaming-response patterns for AI-generated content (that's [`modern-patterns.md`](modern-patterns.md) § Streaming). Reduced-motion preferences and assistive-tech performance (that's [`accessibility.md`](accessibility.md)).

## When to load this file

- The design includes a list, table, or feed that could exceed 50 items. Virtualisation isn't optional at that scale.
- The design relies on hero imagery, video, or custom fonts that could compete for the critical path.
- You're hitting a server: the design's loading choreography needs a budget.
- The user names *performance*, *speed*, *Core Web Vitals*, *LCP*, *CLS*, *INP*, *skeleton*, *virtualise*, *lazy load*, *preload*, *optimistic UI*, or *streaming response*.
- You're auditing a shipped design that feels sluggish on mid-range hardware (and most hardware is mid-range).

## Network budgets

Every request the design triggers has a budget. If you can't name it, you haven't designed the loading state.

- **GET above-the-fold content < 200ms.** Anything the user sees on first paint should arrive in under 200ms from a warm cache, under 500ms from a cold one. Beyond that, a skeleton becomes mandatory.
- **POST / PATCH / DELETE < 500ms target.** Mutations are the actions the user is waiting on. Optimistic UI bridges the gap when the server can't.
- **> 1 second feels slow without explicit progress.** Once a request crosses one second, the design owes the user a visible signal: a skeleton, a determinate progress bar, or a streaming response that shows the work happening.
- **> 10 seconds needs cancel and recovery.** Long-running operations need a Cancel button alongside an explicit estimate, plus a fallback if they fail. Don't strand the user inside a spinner.

Document the expected budget in the component's `context`: `'Above-fold list. Budget < 200ms cached, < 500ms cold. Skeleton renders if request exceeds 200ms.'`

## Core Web Vitals

Google's Core Web Vitals are the field-measured performance signals every shipped page should meet. The 2025 baseline thresholds:

- **LCP (Largest Contentful Paint) < 2.5 seconds.** Time to render the largest above-the-fold element (usually the hero image or hero text block). Optimise by preloading the LCP candidate and serving the right image format. Render-blocking resources push it out.
- **CLS (Cumulative Layout Shift) < 0.1.** Sum of unexpected layout shifts during the page's lifetime. Usually caused by images without `width`/`height` or by web fonts without `font-display`. Reserve space for everything that loads asynchronously.
- **INP (Interaction to Next Paint) < 200ms.** Replaced FID as a Core Web Vital in March 2024. Measures the latency of the slowest user interaction during the page's lifetime. Heavy JavaScript on input handlers shows up here; so does an unbroken main thread that can't respond to a click.

These are user-facing signals measured from real browsers in the field. A design that meets these on a flagship phone in San Francisco may fail them on a Pixel 4a in Jakarta. Test with real-device throttling.

## Virtualisation for long lists

Lists with more than 50 items must virtualise. Rendering every row in the DOM ships as scroll jank and ballooning memory, with a main thread that can't keep up.

- **Render only what's visible plus a small buffer.** A typical viewport-buffer is one viewport above and below the visible region. The library handles the math.
- **Common libraries:** TanStack Virtual (framework-agnostic, the modern default), react-window (smaller, mature), react-virtualized (larger, older but still used). Pick TanStack Virtual for new work; the API is cleaner and it supports both fixed and dynamic row heights.
- **Document the intent in `context`.** Without the note, the engineer may render the naive map and ship a 5,000-row DOM. `'Virtualised list. Renders ~20 visible rows + 1 viewport buffer. Use TanStack Virtual or equivalent.'`
- **Fixed row heights are easier than dynamic.** If the design can commit to a uniform row height, virtualisation is trivial; dynamic heights need measurement passes that hurt scroll smoothness on mid-range devices. Don't pick dynamic heights without a reason.

## Image optimisation

Images are usually the LCP candidate and the most common source of CLS. Treat them with care.

- **Always specify `width` and `height`.** Or set `aspect-ratio` in CSS. Without explicit dimensions, the browser can't reserve space, and the page jumps when the image loads. This is the most common CLS cause on the web.
- **Preload above-the-fold images.** `<link rel="preload" as="image" href="..." imagesrcset="..." imagesizes="...">` tells the browser to fetch the LCP image as early as possible. Without it, the image waits for the parser to discover the `<img>` tag.
- **Lazy-load below-the-fold.** `loading="lazy"` on `<img>` and `<iframe>` defers loading until the element is near the viewport. Don't lazy-load the LCP image; that delays the metric you're trying to improve.
- **Modern formats.** AVIF gives the best compression (often 30 to 50% smaller than JPEG). WebP has broader support and is the safe default. Serve JPEG as a fallback via `<picture>` and `<source>`.
- **Responsive images.** `srcset` and `sizes` let the browser pick the right resolution for the device. A 4K hero shouldn't ship to a 360px phone.
- **LQIP or blur-up for hero media.** A tiny base64-encoded blurred preview (Low-Quality Image Placeholder) renders instantly while the full image loads. Linear, Vercel, and most modern image CDNs do this by default.

In Pencil, `image` nodes always carry width and height. Reserve space deterministically.

## Font loading

Custom fonts are the second most common cause of CLS, and a frequent cause of slow LCP.

- **Preload critical fonts.** `<link rel="preload" as="font" type="font/woff2" crossorigin>` for the fonts used in the LCP element (usually the hero headline). Don't preload every weight; pick the one the LCP needs.
- **`font-display: swap` for non-critical fonts.** The browser renders fallback type immediately, then swaps to the custom font when it loads. Without `swap`, the user sees blank space (FOIT, Flash of Invisible Text) for up to three seconds.
- **Subset fonts.** A font that ships only the latin or latin-ext subset is dramatically smaller than one shipping every glyph. For English-only body text, the latin subset is plenty. For multilingual sites, ship the relevant subsets per language.
- **Self-host where you can.** Hosting fonts on your own CDN (or the framework's edge network) avoids a third-party DNS lookup and gives you cache-control. Google Fonts' CSS file is render-blocking by default.

## Theme colour

`<meta name="theme-color">` colours the browser chrome. Mobile Safari's address bar picks it up; Android Chrome and installed PWAs do too. Match the page background per mode.

- **Light mode:** `<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">`
- **Dark mode:** `<meta name="theme-color" content="#0a0a0a" media="(prefers-color-scheme: dark)">`

Without it, mobile Safari shows a default grey bar above your beautifully designed hero. With it, the chrome blends and the design feels native. Five lines of HTML; significant perceptual upgrade.

## Skeleton vs spinner

The choice depends on whether you know the shape of the loaded content.

- **Skeleton when the layout is known.** A list of cards loading? Render skeleton cards in the same shape and position. The page doesn't reflow when content arrives, and the user sees the structure forming. Linear and Stripe lean on skeletons heavily.
- **Spinner when the duration is short and the shape is unknown.** A modal that triggers a one-off API call, a short search query: a spinner is fine. Reserve it for unknown shapes under one second.
- **Determinate progress when you know the duration.** A file upload, a multi-step migration: show a real progress bar with a percentage. Indeterminate spinners on long operations feel broken.

For the timing rules (when to show, when to hide, minimum visible time), see [`interactions.md`](interactions.md) § Loading state timing. The short version: don't show a loading indicator before 100ms; don't hide it before 300ms once shown.

## Perceived performance

The fastest-feeling apps aren't always the fastest in a benchmark. They've optimised perception.

- **Optimistic UI.** The action visually completes before the server confirms. The API call happens in the background, and the UI rolls back if the server returns an error. Linear's keyboard shortcuts feel instant because every state change is optimistic. Use it when failure is rare and recoverable; avoid it when failure is user-visible (a payment, a delete).
- **LQIP and blur-up for media.** Already covered above; perception-wise, the user sees something almost instantly, even if the full image is a second behind.
- **Streaming responses.** For AI-generated content, stream tokens as they arrive instead of waiting for the full response. The user reads while the model writes; the experience feels real-time even when total latency is several seconds. See [`modern-patterns.md`](modern-patterns.md) § Streaming responses.
- **Stable scroll position.** When new content loads above the user's scroll position (a feed prepending older items), don't shift the viewport. Anchor to a stable element. Linear and Discord handle this carefully. Many social feeds still get it wrong.

## Pencil expression

Performance hints belong in the component `context` so the engineer ships the right loading discipline:

- **List components.** `'Virtualised list. > 50 items must render only the visible viewport + 1-screen buffer. Use TanStack Virtual.'`
- **Image nodes.** Always specify `width` and `height`. For hero images, add `'Preload as LCP candidate. AVIF + WebP fallback. LQIP renders during load.'`
- **Below-the-fold sections.** `'Lazy-loaded below the fold. Preload only if the user is signed in.'`
- **Skeleton frames.** `'Skeleton matches loaded card shape. Renders if request exceeds 200ms. Min visible time 300ms once shown.'`
- **Optimistic actions.** On the action button or toggle: `'Optimistic UI. State flips immediately on click; rolls back if server returns error within 5s.'`
- **Streaming responses.** On the AI output frame: `'Streams tokens as they arrive. Renders incrementally. See modern-patterns.md § Streaming.'`

The engineer reads the `context`, and the design's performance intent ships with the design.

## Anti-patterns

These read as performance-blind designs and should be fixed in passing:

- **Lists rendering 500+ rows in the DOM.** Scroll jank and ballooning memory, plus an unresponsive main thread. Virtualise.
- **Images without `width`/`height`.** Guarantees CLS. Reserve space for every async-loaded element.
- **Custom fonts without `font-display`.** Three seconds of invisible text on slow connections.
- **Lazy-loading the hero image.** Defers the LCP. Preload it instead.
- **Spinner for any wait longer than two seconds.** The user can't tell if it's still working. Skeleton or determinate progress.
- **Auto-rotating carousels above the fold.** Compete with the LCP for the critical path and tank INP.
- **Disabling buttons during async work without keeping the label.** A bare spinner is a regression. Keep the label, add the spinner.
- **No `theme-color` meta tag.** Mobile Safari renders the default grey bar above your design.

## Sources

- **web.dev Core Web Vitals (2025 baseline)**: https://web.dev/articles/vitals : LCP, CLS, INP thresholds and measurement methodology, including the March 2024 INP-replaces-FID rollout.
- **MDN Web Docs**: https://developer.mozilla.org : image optimisation (`srcset`, `sizes`, `loading`), font loading (`font-display`, `preload`), `theme-color` meta documentation.
- **Chrome DevRel team**: posts and Chrome for Developers videos covering INP measurement, optimisation patterns, and the Core Web Vitals 2024-2025 evolution.
- **HTTP Archive**: httparchive.org annual Web Almanac : real-world performance data on what shipped sites actually do.
- **TanStack Virtual / react-window**: virtualisation library documentation and benchmarks.
- **Apple HIG**: performance guidance for iOS and macOS native experiences (where it crosses into web).
- **W3C Web Performance Working Group**: specs for `PerformanceObserver`, `LargestContentfulPaint`, `LayoutShift`.
- **Real-world exemplars accessed 2025/2026**: Vercel Edge Network, Cloudflare CDN, Linear (perceived performance via optimistic UI), Stripe (skeleton choreography, optimistic mutation).

## See also

- [`states.md`](states.md): visual design of skeleton, loading, and error states.
- [`interactions.md`](interactions.md): timing rules for loading indicators (show-delay, min-visible-time).
- [`modern-patterns.md`](modern-patterns.md): streaming responses, AI-UI affordances, perceived-performance patterns for AI-generated content.
- [`accessibility.md`](accessibility.md): `prefers-reduced-motion`, performance considerations for assistive tech.
- [`mobile-patterns.md`](mobile-patterns.md): mobile-specific performance budgets and patterns (when present in the project).
- [`composition-patterns.md`](composition-patterns.md): slot design for skeleton-aware list and card components.
