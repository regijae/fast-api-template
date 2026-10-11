#!/usr/bin/env bash

# Print the OpenAPI schema to stdout, for generating API clients.
# The caller redirects it:
#   docker compose run --rm -T api bash scripts/generate-openapi.sh > openapi.json

set -e

python -c "import app.main, json; print(json.dumps(app.main.app.openapi()))"
