# Fortran Backend

Use this reference for Fortran numerical backend components, batch compute services, scientific service kernels, and native modules used by other backend runtimes.

Follow the existing compiler, standard, module layout, and build system, usually fpm, Make, CMake, or vendor toolchains. Keep numerical kernels separate from I/O, orchestration, and language-binding code. Preserve precision choices and array layout assumptions.

Validate dimensions, units, missing values, convergence parameters, and file inputs before computation. When exposing Fortran through C, Python, or service wrappers, keep ABI boundaries explicit with `ISO_C_BINDING` and document ownership. Preserve `implicit none`, kind parameters, array ordering, and tolerance choices.

Tests should use the existing fpm tests, pFUnit, custom numerical fixtures, or wrapper-level tests. Cover expected results, invalid dimensions, edge cases, and tolerance-sensitive behavior. Verify with fpm, compiler warnings, bounds checking, and relevant optimization/debug builds when practical.
