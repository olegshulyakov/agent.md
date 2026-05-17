# Angular

Use this reference for Angular applications with standalone components or NgModules, services, RxJS, signals, forms, and Angular Router.

Follow the project's current architecture before introducing standalone APIs, signals, or new state libraries. Keep presentation in components, reusable logic in services, and route concerns in guards, resolvers, or route data when those patterns exist.

Use reactive forms for complex validation and template-driven forms only where already established. Manage subscriptions with `async` pipe, signals, `takeUntilDestroyed`, or existing cleanup utilities. Keep change detection and track functions explicit for large lists.

Prefer Angular Material, CDK, or the local component system when present. Preserve ARIA, focus management, and keyboard behavior for custom controls.
