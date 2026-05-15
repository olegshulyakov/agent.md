# Ruby Backend

Use this reference for Rails, Sinatra, or Ruby backend code.

For Rails, follow the app's conventions for controllers, models, service objects, jobs, serializers, policies, and concerns. Keep controllers thin and move business workflows into models or services according to local style. Use strong parameters, validations, transactions, and ActiveRecord scopes deliberately.

For background jobs, match the existing ActiveJob, Sidekiq, or queue setup and make retries/idempotency explicit for side-effecting work. Prefer framework conventions over custom plumbing unless the repository already has a clearer abstraction. Respect Rails autoloading, callbacks, validations, and strong parameters; avoid callback-heavy changes when a service object is already the local pattern.

Tests should use RSpec, Minitest, request specs, model specs, or job specs as already configured. Cover success, validation failure, authorization/policy failure when relevant, and transaction behavior for multi-write flows. Verify with bundle exec test/rspec and RuboCop or standardrb when present.
