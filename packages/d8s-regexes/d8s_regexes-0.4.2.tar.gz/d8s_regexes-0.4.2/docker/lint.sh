#!/usr/bin/env bash

set -euxo pipefail

echo "Running linters and formatters..."

isort d8s_regexes/ tests/

black d8s_regexes/ tests/

mypy d8s_regexes/ tests/

pylint --fail-under 9 d8s_regexes/*.py

flake8 d8s_regexes/ tests/

bandit -r d8s_regexes/

# we run black again at the end to undo any odd changes made by any of the linters above
black d8s_regexes/ tests/
