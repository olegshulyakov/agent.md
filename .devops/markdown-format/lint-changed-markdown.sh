#!/usr/bin/env bash
set -euo pipefail

mapfile -t files < changed-markdown-files.txt

set +e
.devops/markdown-format/node_modules/.bin/markdownlint-cli2 \
  --json \
  "${files[@]}" > markdownlint-results.json
status=$?
set -e

if [ "$status" -gt 1 ]; then
  exit "$status"
fi
