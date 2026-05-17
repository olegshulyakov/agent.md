# PHP Laravel Backend

Use this framework reference after `references/php.md` when the backend is Laravel.

Follow existing conventions for controllers, form requests, resources, policies, services, jobs, events, listeners, models, and migrations. Keep controllers thin, validate with Form Requests or the project's validation style, and map responses through resources when present.

Use Eloquent relationships, query scopes, transactions, queues, and configuration in the established project style. Avoid burying business behavior in controllers or model events when the workflow needs explicit ordering and testability.

Tests should use Pest or PHPUnit with the local factories, database refresh strategy, HTTP helpers, and queue/event fakes. Cover success, validation failure, authorization failure when relevant, and one persistence or job edge case.
