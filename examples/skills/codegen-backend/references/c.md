# C Backend

Use this reference for C services, embedded backend components, POSIX network daemons, native extensions, and low-level service libraries.

Follow the existing build system, usually Make, CMake, Meson, Bazel, or Autotools. Keep request parsing, validation, domain logic, and persistence separated where the project has those boundaries. Make ownership rules explicit: document whether callers own buffers, returned pointers, file descriptors, and allocated structs.

Validate all inputs at boundaries. Check every allocation, system call, parser result, and I/O operation. Avoid unsafe string handling when bounded alternatives are available. Use the project's logging, error-code, cleanup, and test conventions. Prefer single-exit cleanup blocks or local cleanup helpers when they reduce leaks without obscuring control flow.

Tests should use the existing C test setup such as Check, CMocka, Unity, Criterion, or integration scripts. Cover success, invalid input, resource cleanup, and failure paths that are easy to miss in manual testing. Verify with the existing compiler warnings, sanitizer, static analyzer, or `clang-tidy`/`cppcheck` target when present.
