#!/usr/bin/env bash

set -euxo pipefail

echo "Running linters and formatters..."

isort d8s_netstrings/ tests/

black d8s_netstrings/ tests/

mypy d8s_netstrings/ tests/

pylint --fail-under 9 d8s_netstrings/*.py

flake8 d8s_netstrings/ tests/

bandit -r d8s_netstrings/

# we run black again at the end to undo any odd changes made by any of the linters above
black d8s_netstrings/ tests/
