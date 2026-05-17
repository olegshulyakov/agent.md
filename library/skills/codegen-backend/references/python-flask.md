# Python Flask Backend

Use this framework reference after `references/python.md` when the backend is Flask.

Follow the existing application factory, blueprint, extension, and configuration patterns. Keep route functions thin, validate request bodies and params with the project's chosen library or helper, and move business behavior into services or domain modules when present.

Reuse Flask extension instances for database access, auth, serialization, logging, and background jobs. Respect request and application context boundaries; do not hide global mutable state in modules when dependency injection or app config is already available.

Tests should use the local Flask test client, app fixtures, database fixtures, and auth helpers. Cover successful requests, validation failures, auth failures when relevant, and persistence behavior for write flows.
