# Python Backend

Use this reference for FastAPI, Django, Flask, or Python service code.

Prefer the framework already present. For FastAPI, keep routers thin, put business logic in services, use Pydantic models for request and response boundaries, and inject database/session dependencies through existing dependency helpers. For Django, follow app boundaries, use model managers or services for business logic when the project already does, and keep serializers/forms responsible for validation.

Use type hints for new public functions. Keep async code async all the way down; do not call blocking drivers in async handlers unless the project already isolates that work. Use SQLAlchemy, Django ORM, or the repository's existing persistence layer rather than raw SQL unless raw SQL is the local convention. Prefer explicit dependency injection over module-level clients for testable services.

Tests should use the existing pytest, Django TestCase, or unittest setup. Cover the handler or service path, validation failure, authorization failure when relevant, and one persistence or transaction edge case for write flows. Verify with local formatter/linter/typecheck tools such as ruff, black, mypy, pyright, or Django checks when configured.
