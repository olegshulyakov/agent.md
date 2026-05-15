# MATLAB Backend

Use this reference for MATLAB Production Server code, batch analytics workers, toolboxes used by backend systems, and scientific service functions.

Follow the existing folder layout, function/class style, toolbox dependencies, and deployment target. Keep computation functions separate from I/O, orchestration, and service wrappers. Preserve numeric precision, vectorization assumptions, and deterministic setup.

Validate input dimensions, units, missing values, table schemas, and numeric ranges before computation. Avoid hidden workspace state; prefer explicit function inputs and outputs. When code is called from another runtime, keep serialization and type conversions explicit. Preserve vectorization and preallocation where they are part of performance-critical paths.

Tests should use MATLAB Unit Test, golden fixtures, or wrapper-level tests. Cover expected numeric results, invalid shapes, missing data, and tolerance-sensitive edge cases. Verify with MATLAB test runners, Code Analyzer guidance, and deployment packaging checks when available.
