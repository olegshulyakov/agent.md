# PHP Symfony Backend

Use this framework reference after `references/php.md` when the backend is Symfony.

Follow existing conventions for controllers, services, forms, validators, Doctrine entities and repositories, messages, voters, event subscribers, and configuration. Keep controllers thin and put business workflows in services or handlers.

Use constructor injection, Symfony config, environment variables, serializer groups, and exception mapping according to the project. Put multi-write behavior inside Doctrine transactions at the service boundary that owns consistency.

Tests should use the local PHPUnit or Pest setup, WebTestCase, KernelTestCase, factories, fixtures, and database reset strategy. Cover success, validation failure, authorization failure when relevant, and persistence or message handling edge cases.
