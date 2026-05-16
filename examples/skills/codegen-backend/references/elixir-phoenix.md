# Elixir Phoenix Backend

Use this framework reference after `references/elixir.md` when the backend is Phoenix.

Follow Phoenix context boundaries. Keep controllers and LiveView event handlers thin, validate with changesets, and put business workflows in contexts or domain modules according to the existing application design.

Use Ecto schemas, changesets, repos, transactions, and telemetry in the established style. Avoid calling Repo directly from controllers when the project uses contexts. Preserve route, plug, authorization, and error view conventions.

Tests should use the local ExUnit, ConnCase, DataCase, factories, and sandbox setup. Cover successful requests, changeset validation, authorization failure when relevant, and transaction-sensitive context behavior.
