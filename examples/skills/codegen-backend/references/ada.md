# Ada Backend

Use this reference for Ada services, safety-critical backend components, GNAT projects, Alire packages, and Ada Web Server applications.

Follow the existing package specs/bodies, project files, runtime profile, and coding standard. Keep interfaces explicit in `.ads` files and implementation details in `.adb` files. Preserve strong typing, range constraints, and contract aspects where the project uses them.

Validate inputs through types, preconditions, and explicit checks before side effects. Be conservative with concurrency, tasking, and protected objects. For SPARK-adjacent code, avoid changes that make proof obligations harder without need. Prefer explicit subtypes, contracts, and controlled exception propagation over loosely typed status plumbing.

Tests should use AUnit, GNATtest, local integration harnesses, or build checks. Cover success, constraint violations, error propagation, and concurrency behavior when relevant. Verify with GNAT/Alire build checks, style checks, and SPARK proof commands when the project uses them.
