# PHP Backend

Use this reference for Laravel, Symfony, or PHP backend code.

For Laravel, follow controllers, form requests, policies, services/actions, jobs, resources, migrations, and Eloquent conventions already present. Validate with FormRequest or the local validation style. Keep business workflows in services/actions when controllers would otherwise grow.

For Symfony, match controllers, services, forms/validators, Doctrine repositories, messages, and event subscribers. Keep configuration in framework config files and environment variables through the established mechanism. Preserve PSR-4 namespaces, dependency injection container conventions, and framework exception mapping.

Tests should use Pest or PHPUnit according to the repository. Cover feature/request behavior, validation failure, authorization failure when relevant, and model or service edge cases. Verify with Composer scripts, PHPStan/Psalm, Pint/PHP-CS-Fixer, or framework test commands when configured.
