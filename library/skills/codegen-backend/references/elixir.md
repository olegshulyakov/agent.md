# Elixir Backend

Use this reference for Phoenix, Plug, Ecto, OTP, and Elixir backend code.

Follow Phoenix contexts when present. Keep controllers focused on params, auth/session context, context calls, and response rendering. Put business behavior in context modules, schemas, changesets, and explicit service modules only when that matches local style.

Use Ecto changesets for validation and casting. Wrap multi-step writes in `Ecto.Multi` when consistency matters. Prefer pattern matching and explicit tagged tuples for control flow. For background work, match existing Oban, GenServer, Broadway, or supervision patterns. Keep side effects out of changesets and supervise long-running processes deliberately.

Tests should use ExUnit, Phoenix ConnCase, DataCase, factories, and local helpers. Cover success, changeset validation failure, authorization failure when relevant, and transaction behavior for multi-write flows. Verify with `mix format`, `mix test`, and Credo/Dialyzer when configured.
