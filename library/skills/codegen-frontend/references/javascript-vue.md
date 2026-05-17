# Vue

Use this reference for Vue apps using the Composition API, Options API, Vue Router, Pinia, Vite, or component libraries.

Follow the existing single-file component style. Prefer Composition API and `<script setup>` only when the project already uses it. Keep props and emits explicit, computed values derived, and watchers reserved for real side effects.

Use Pinia or the existing store for shared state. Keep route-specific fetch logic near routes or composables according to local patterns. Preserve accessibility in custom components by forwarding attributes, labels, keyboard behavior, and focus state.
