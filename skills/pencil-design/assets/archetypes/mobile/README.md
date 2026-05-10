# mobile

Native and native-feeling mobile app surfaces. These archetypes assume single-column, gesture-driven, status-bar-aware design. Adjust spacing for safe-area insets; assume the user holds the device in one hand most of the time.

## Archetypes in this folder

- **ios-native-utility.md**, Apple stock apps / Things. Native-feel chrome, large titles, sheet-driven, gesture-rich.
- **ios-native-social.md**, Instagram / TikTok. Image-first, full-bleed, chrome-light, vertical-scroll dominant.
- **android-material.md**, Google apps / modern Material 3. Bold colour, FAB pattern, expressive type, motion-led.
- **cross-platform-modern.md**, Notion mobile / Linear mobile. Cross-platform but designed once; refined typography, restrained colour, tab bar where useful.

## Picking between them

| User cue | Archetype |
|---|---|
| "iOS native, utility / productivity" | ios-native-utility |
| "iOS native, social / content / feed" | ios-native-social |
| "Android native, expressive" | android-material |
| "Cross-platform, designed-once feel" | cross-platform-modern |

If platform isn't specified, default to **cross-platform-modern**, it travels well to iOS and Android with minor adaptation. Don't reach for `android-material` unless Android is explicitly the primary platform.
