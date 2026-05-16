# Ruby Sinatra Backend

Use this framework reference after `references/ruby.md` when the backend is Sinatra.

Follow existing app, modular route, middleware, helper, settings, and dependency conventions. Keep route blocks focused on request parsing, auth context, service calls, and response mapping.

Use the repository's validation, serialization, persistence, and error handling style. Avoid growing a single route file when the project already separates routes, services, models, and jobs.

Tests should use the local Rack::Test, RSpec, Minitest, fixtures, and persistence setup. Cover success, malformed input, authorization when relevant, and one service or persistence edge case.
