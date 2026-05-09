# Customising Your Design System

This folder holds the files that tell your AI assistant how your product looks, feels, and sounds. Fill them in and your AI will use your actual brand colours, your fonts, and your rules for writing. Leave them blank and it makes sensible guesses, but they won't be specific to you.

You don't need to be a developer or a designer to edit these files. If you can type into a document, you can do this.

---

## Before you start

### What kind of files are these?

Each file in this folder is a plain text file with the extension `.md`. That stands for Markdown, which is just a way of adding simple formatting (like headings and bullet points) to a plain text file.

You can open and edit any of them using:

- **VS Code** (free, works on Mac and Windows, recommended)
- **TextEdit** on Mac — but open the file with Format > Make Plain Text first, or it'll add hidden formatting
- **Notepad** on Windows
- Any code editor your team already uses

Do not open these files in Microsoft Word or Google Docs. Those apps add hidden formatting that will break the files.

### What does editing these files actually do?

When you ask your AI to build or design something, it reads these files before it starts. It uses what it finds to make decisions: which colour to put on a button, what words to use in an error message, how wide to make a sidebar.

The more specific you make the files, the more consistent the AI's output will be. Vague guidance produces vague results. A clear rule like "use `$primary` for any button" is far more useful than a paragraph explaining your colour philosophy.

### Do I need to fill in everything?

No. Start with the three files below. Come back to the others when the AI produces something that doesn't look or sound right.

---

## Start here: the three most important files

### Step 1 — `design-system.md`

Open this file first. It's a one-page overview that the AI reads before anything else.

Fill in:

- **Your tech stack** — the framework your developers use to build the product (e.g. React, Next.js, Vue). If you're not sure, ask a developer or leave it blank.
- **Your font name** — the name of the main font your product uses (e.g. Inter, Poppins, Helvetica Neue).
- **Your icon library** — the name of the icon set you use (e.g. Lucide, Heroicons, Phosphor). If you don't have one, leave it blank.
- **A one-line description of your visual style** — something like "Clean and minimal with a dark mode" or "Bold and expressive with rounded corners and warm tones."

Even a few lines here give the AI a useful starting point.

---

### Step 2 — `tokens.md`

This is the most important file in the folder. It holds your actual colours, fonts, and spacing values. Getting this right makes the biggest difference to how your AI's output looks.

#### Colours

Look for a section that lists colour variables. They'll look something like this:

```
$primary: #3B82F6      # main brand colour, light mode
$primary-dark: #60A5FA # main brand colour, dark mode
```

Replace the values after the colon with your brand colours. Colours are written as hex codes — six characters after a `#` symbol, like `#FF5733` or `#1A1A2E`. Your brand guidelines should have these. If you don't have brand guidelines, ask your designer.

If your product has a dark mode, you'll see pairs of values — one for light and one for dark. Fill in both. If your product only has one mode, fill in the light mode value and copy it for the dark.

Common colours you'll see listed:

| Token name | What it's for |
|------------|--------------|
| `$primary` | Your main brand colour — buttons, links, key UI elements |
| `$accent` | A secondary highlight colour |
| `$surface` | Background colour for cards and panels |
| `$text` | The main body text colour |
| `$danger` | Colour for error messages and destructive actions |
| `$warning` | Colour for warning messages |
| `$success` | Colour for confirmations and success states |

#### Fonts

Find the lines for font families. They'll look like:

```
$fontHeading: "Inter"
$fontBody: "Inter"
$fontMono: "JetBrains Mono"
```

Replace the font names with the ones your product uses. If you use the same font for everything, put it in all three. `$fontMono` is for code snippets — if your product doesn't show any code, you can leave it as-is.

#### Spacing and sizing

You'll also see a section with spacing values. These control how much gap goes between things. The defaults work well for most products — only change them if you have a specific reason to.

---

### Step 3 — `voice.md`

This file covers how your product talks to users: the words on buttons, the phrasing of error messages, the copy on empty screens.

Fill in:

- **Tone** — two or three words that describe your brand's voice. For example: "Friendly and direct." "Professional but approachable." "Technical and precise." The AI will use this to write copy that fits your brand.
- **Forbidden words** — any words you never want to appear in your product. Common ones: "seamless", "leverage", "empower", "utilise". Add any that feel off-brand.
- **Date format** — how you write dates. For example: "12 April 2025" or "12/04/25" or "April 12, 2025".
- **Button copy rules** — anything specific about how you label buttons. For example: "Always use a verb. 'Save changes', not 'OK'."

Three minutes on `voice.md` will save you a lot of copy fixes later.

---

## The rest of the files

Once you've done the first three, the other files are there when you need them. Edit them when the AI's output on that topic isn't matching what you want.

### Files you'll probably edit

| File | What it covers |
|------|---------------|
| `components.md` | The building blocks of your UI: buttons, inputs, cards, modals, and more. Describes what each one is for and when to use it. |
| `layout.md` | How things are arranged on the page — grids, spacing between sections, how wide things should be. |
| `patterns.md` | Full-page layouts for common screen types: dashboards, settings pages, login screens, marketing landing pages. |
| `states.md` | What happens when something is loading, broken, empty, or disabled. Covers both individual components (a button in a loading state) and whole pages (a dashboard with no data yet). |
| `navigation.md` | Sidebars, top navigation bars, mobile menus, breadcrumbs. |
| `forms.md` | How forms validate input, how errors appear, how the submit button behaves. |
| `empty-states.md` | What users see when a list is empty or a dashboard has no data yet. |
| `code-export.md` | Instructions for how your designs translate into code. Mainly relevant for developers. |

### Optional files — delete the ones that don't apply

These files are included by default but only matter for specific kinds of products. If a file doesn't apply to yours, delete it. That keeps things tidy and prevents the AI from trying to apply rules that aren't relevant.

| File | Delete it if... |
|------|----------------|
| `mobile.md` | Your product is only used on desktop |
| `data-viz.md` | Your product has no charts, graphs, or data visualisations |
| `brand.md` | You have no distinct logo or brand mark |
| `imagery.md` | Your product uses no photos or illustrations |
| `visual-style.md` | You haven't chosen a specific visual style direction |
| `micro-interactions.md` | You have no specific requirements for animations |
| `onboarding.md` | Your product has no sign-up or first-use flow |
| `search.md` | Your product has no search feature |
| `accessibility.md` | You haven't set formal accessibility requirements yet |
| `file-architecture.md` | You have only one design file |
| `elevation.md` | You have no specific requirements for shadows and depth |
| `iconography.md` | You have no specific icon rules |
| `motion.md` | You have no animation requirements |

---

## Tips for keeping it useful

**Decisions, not descriptions.** "Use `$primary` for all interactive elements" is more useful than a paragraph about your colour philosophy. The AI can't interpret vague guidance — it needs a rule it can follow.

**Short beats long.** These files work best when they're under about 500 words each. A long file is harder for the AI to process and easier to write badly. If a file is getting long, cut the parts you're least certain about.

**Leave blanks rather than guessing.** If you're not sure what a value should be, leave it empty. The AI will use a sensible default. A wrong value is worse than a missing one.

**Edit any time.** These files aren't locked in. The AI picks up any changes you make on the next task. Don't feel like you have to get everything right before you start using the skill.

**You only need to fill in what's relevant.** If your product has no charts, delete `data-viz.md`. If you haven't chosen a visual style yet, leave `visual-style.md` blank. A focused, accurate file beats an ambitious, half-filled one.

---

## When something doesn't look right

If the AI produces something that doesn't match your brand, the fix is almost always in one of these files. Ask yourself: "Where would I write the rule about this?" Then open that file and add it.

| Problem | File to edit |
|---------|-------------|
| Wrong colour on a button or link | `tokens.md` |
| Wrong font | `tokens.md` |
| Wrong words on buttons or error messages | `voice.md` |
| Page layout looks wrong | `patterns.md` or `layout.md` |
| Shadows look too heavy or too flat | `elevation.md` |
| Icons are the wrong size or colour | `iconography.md` |
| Missing loading or error states | `states.md` |
| Empty screens look wrong | `empty-states.md` |
| Animations are too fast, too slow, or missing | `motion.md` or `micro-interactions.md` |
| Navigation structure is wrong | `navigation.md` |
| Form validation behaves incorrectly | `forms.md` |

Add one clear rule and try again on the next task. You'll see the difference.

---

## Questions?

This folder was created by the [pencil-design skill](https://github.com/Nisus74/pencil-skill). If something isn't working as expected, check the issues page on that repository.
