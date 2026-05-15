# R Backend

Use this reference for R APIs, Shiny server code, plumber services, RServe integrations, and production analytics jobs.

Follow the existing package structure, dependency management, and style, usually `renv`, `DESCRIPTION`, `testthat`, and tidyverse or data.table conventions. Keep API handlers thin and put reusable computation into functions that can be tested without HTTP or UI machinery.

Validate inputs explicitly, especially data frames, column names, factor levels, dates, and numeric ranges. Keep long-running computation, caching, and model loading behavior clear. Avoid hidden global state unless the app already uses it deliberately. Preserve vectorized operations and deterministic seeds where reproducibility matters.

Tests should use `testthat`, plumber route tests, or Shiny test helpers as configured. Cover success, invalid input, missing data, and reproducibility-sensitive cases. Verify with `devtools::test()`, `R CMD check`, lintr, or renv restore/status commands when configured.
