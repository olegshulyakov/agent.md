# Delphi/Object Pascal Backend

Use this reference for Delphi/Object Pascal services, RAD Server, DataSnap, Horse, Lazarus, and legacy service code.

Follow the existing project structure and component model. Keep transport handlers thin, put business logic in service classes or units, and preserve local exception, logging, and dataset conventions. Be careful with ownership for components, interfaces, streams, and manually allocated objects.

Validate inputs before database or file side effects. Use transactions around multi-write database work and avoid returning raw database errors to clients. Do not modernize broad legacy code unless the requested change requires it. Use `try..finally` for owned objects and `try..except` only where errors are intentionally translated.

Tests should use DUnitX, local integration tests, or existing manual harnesses. Cover success, validation failure, transaction rollback, and ownership/resource cleanup when practical. Verify with the existing Delphi/Lazarus build, compiler warnings, and package/test runner commands.
