# Perl Backend

Use this reference for Perl web services, scripts that power backend workflows, and CPAN-based service code.

Follow the existing framework and module layout, such as Mojolicious, Dancer2, Catalyst, PSGI/Plack, DBI, or local scripts. Use `strict`, `warnings`, and the project's object/module style. Keep request handlers thin and put reusable behavior into modules.

Validate input before side effects, use placeholders for SQL, and keep secrets in the existing configuration mechanism. Preserve legacy behavior unless the user explicitly asks for modernization; Perl codebases often have important fossils in the walls. Keep taint, UTF-8, localtime/timezone, and context-sensitivity issues in mind for old services.

Tests should use Test::More, Test::Most, Test::Mojo, or local harnesses. Cover success, invalid input, database failures, and compatibility behavior. Verify with prove, dzil/minil, Perl::Critic, or cpanm/carton commands when configured.
