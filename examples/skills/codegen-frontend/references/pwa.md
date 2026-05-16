# PWA

Use this reference for service workers, web app manifests, offline behavior, installability, caching, background sync, and push notifications.

Follow the existing PWA library or framework integration. Make caching strategies explicit: app shell, static assets, API responses, and user-generated data have different freshness and privacy requirements. Never cache sensitive authenticated responses unless the app already has a secure offline model.

Provide clear offline, stale, update-available, and retry states. Keep service worker registration, versioning, and update prompts consistent. Verify installability and offline behavior with browser tooling when possible.
