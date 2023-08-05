#!/usr/bin/env bash

set -euxo pipefail

echo "Running linters and formatters..."

isort d8s_utility/ tests/

black d8s_utility/ tests/

mypy d8s_utility/ tests/

pylint --fail-under 9 d8s_utility/*.py

flake8 d8s_utility/ tests/

# we run black again at the end to undo any odd changes made by any of the linters above
black d8s_utility/ tests/
