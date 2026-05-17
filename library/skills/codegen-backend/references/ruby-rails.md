# Ruby Rails Backend

Use this framework reference after `references/ruby.md` when the backend is Rails.

Follow Rails conventions and the project's boundaries for controllers, models, services, jobs, serializers, policies, mailers, and concerns. Keep controllers thin, use strong parameters, and keep business behavior in models or services according to local style.

Use ActiveRecord scopes, validations, callbacks, and transactions carefully. Prefer explicit service objects for multi-model workflows when the project already uses them, and avoid adding callbacks for behavior that needs clear ordering or error handling.

Tests should use the existing RSpec or Minitest setup, factories, request specs, model specs, job specs, and policy specs. Cover success, validation failure, authorization failure when relevant, and transaction-sensitive write behavior.
