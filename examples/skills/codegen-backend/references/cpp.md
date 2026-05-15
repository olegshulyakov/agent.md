# C++ Backend

Use this reference for C++ services, RPC servers, native backend libraries, and high-performance service components.

Follow the existing standard level, build system, and dependency style. Prefer RAII, value types, smart pointers, and explicit ownership over raw lifetime management. Keep transport handlers thin and put business behavior into services or domain modules.

Reuse local framework conventions, such as Boost.Asio/Beast, Drogon, Pistache, oatpp, gRPC, Protobuf, or custom networking. Preserve exception/error-code style already used by the project; do not mix styles casually. Validate inputs before side effects and keep concurrency behavior explicit. Prefer `std::string_view`, spans, move semantics, and const-correct APIs only where lifetimes stay clear.

Tests should use the existing framework such as GoogleTest, Catch2, doctest, Boost.Test, or integration harnesses. Cover success, validation failure, ownership/resource cleanup, and concurrency-sensitive edge cases when relevant. Verify with the configured build, compiler warnings, sanitizers, clang-tidy, or static analysis targets when available.
