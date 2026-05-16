# Python Django Backend

Use this framework reference after `references/python.md` when the backend is Django or Django REST Framework.

Follow app boundaries and existing conventions for models, managers, services, serializers, forms, views, viewsets, and permissions. Keep validation in serializers or forms when that is the local pattern, and avoid moving business rules into views when the project has a service or domain layer.

Use the Django ORM and migration workflow already present. Put multi-write behavior inside `transaction.atomic()` at the service or view boundary that owns consistency. Avoid leaking model internals through APIs unless the project intentionally exposes model serializers for that surface.

Tests should use the existing pytest-django, Django `TestCase`, API client, factory, and fixture style. Cover permissions, validation, query behavior, and transaction-sensitive write paths when relevant.
