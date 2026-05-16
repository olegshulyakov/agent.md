# Python FastAPI Backend

Use this framework reference after `references/python.md` when the backend is FastAPI or Starlette-based.

Keep `APIRouter` handlers thin. Parse and validate request data with Pydantic models, enforce authorization through existing dependencies or middleware, and delegate business behavior to services or use cases. Reuse the project's dependency helpers for database sessions, current user context, settings, and external clients.

Match the existing sync or async stack. Do not call blocking database drivers, SDKs, or HTTP clients directly inside async handlers unless the project already isolates that work. Return response models when the project uses them, and keep status codes, error envelopes, and exception handlers consistent with the existing app.

Tests should use the local `TestClient`, `httpx.AsyncClient`, dependency overrides, fixtures, and database transaction strategy. Cover successful request handling, validation failure, authorization failure when relevant, and one service or persistence edge case for write flows.
