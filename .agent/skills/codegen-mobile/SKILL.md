---
name: codegen-mobile
description: >
  Generates production-ready mobile code for iOS (SwiftUI), Android (Jetpack Compose), React Native, and Flutter,
  including screens, navigation, state management, and platform-specific patterns. Use this skill whenever the
  user wants to write mobile app code, create a screen or view, implement mobile navigation, add platform-specific
  features, or asks to "build this mobile screen", "write Swift code for X", "create a Kotlin/Compose screen",
  "implement this in React Native", "write Flutter widgets", or "scaffold this mobile feature". Detect the
  platform from context automatically (file extensions, imports, project structure). Also trigger for "make this
  work on iOS/Android", mobile state management, and cross-platform component patterns.
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# codegen-mobile

Generate **production-ready mobile code** for the detected platform with idiomatic patterns, proper state management, and platform conventions.

## Variant Detection

Identify the target platform in this order:

1. **File extensions**: `.swift` → SwiftUI/iOS, `.kt` + Android imports → Jetpack Compose, `.tsx`/`.jsx` + RN imports → React Native, `.dart` → Flutter
2. **Import statements**: `import SwiftUI`, `import androidx.compose.*`, `import React Native`, `import 'package:flutter'`
3. **Project files**: `Package.swift` → iOS, `build.gradle` → Android, `pubspec.yaml` → Flutter, `app.json` with Expo → React Native
4. **Explicit user mention**: "SwiftUI", "Compose", "React Native", "Flutter", "iOS", "Android", "Expo"
5. **If ambiguous**: Ask once with options: `Which platform? [SwiftUI/iOS] [Jetpack Compose/Android] [React Native] [Flutter]`

Then **read the appropriate reference file** from `references/`:
- `swift.md` → SwiftUI patterns, Combine, Swift concurrency, SPM
- `kotlin-android.md` → Jetpack Compose, Coroutines, Hilt, Room
- `react-native.md` → Expo, navigation, NativeWind, MMKV
- `flutter.md` → Widgets, Riverpod, go_router, freezed

## Code quality standards (all platforms)

- Use the platform's idiomatic state management (not raw primitives where a pattern exists)
- Handle loading, error, and empty states explicitly
- Include accessibility labels/hints where applicable
- Extract reusable components from repeated UI patterns
- No hardcoded colors or strings — use theme/resource system
- Handle keyboard, safe area insets, and platform-specific edge cases

## Output format

Produce complete, runnable code files. For each file:

```
// File: path/to/FileName.swift (or .kt, .tsx, .dart)
// Description: [what this file does]

[complete code]
```

Follow with any setup notes (dependencies to add, permissions required, etc.).

## Common patterns (all platforms)

### Screen structure
Every screen should have:
- A root container respecting safe areas
- Loading state while data fetches
- Error state with retry option
- Empty state when no data
- The actual content state

### Navigation
Pass typed/structured arguments between screens rather than raw strings or Any types.

### API calls
Wrap in a ViewModel/BLoC/Hook that separates network logic from UI. The view observes state, not raw data.

### Forms
- Real-time or on-submit validation
- Disable submit while loading
- Clear error feedback per field
