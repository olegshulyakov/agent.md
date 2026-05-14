#!/usr/bin/env bash
set -euo pipefail

base_ref_name="${BASE_REF_NAME:?BASE_REF_NAME is required}"
base_ref="origin/${base_ref_name}"

git fetch --no-tags --depth=1 origin "${base_ref_name}"

git diff --name-only --diff-filter=ACMRT "${base_ref}...HEAD" \
  -- '*.md' > changed-markdown-files.txt

if [ -s changed-markdown-files.txt ]; then
  echo "has_markdown=true" >> "$GITHUB_OUTPUT"
  printf 'Changed Markdown files:\n'
  cat changed-markdown-files.txt
else
  echo "has_markdown=false" >> "$GITHUB_OUTPUT"
  printf 'No changed Markdown files found.\n'
fi
