#!/usr/bin/env bash

set -euxo pipefail

echo "Running linters and formatters..."

isort d8s_timer/ tests/

black d8s_timer/ tests/

mypy d8s_timer/ tests/

pylint --fail-under 9 d8s_timer/*.py

flake8 d8s_timer/ tests/

bandit -r d8s_timer/

# we run black again at the end to undo any odd changes made by any of the linters above
black d8s_timer/ tests/
