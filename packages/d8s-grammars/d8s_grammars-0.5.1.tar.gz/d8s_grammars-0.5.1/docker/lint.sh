#!/usr/bin/env bash

set -euxo pipefail

echo "Running linters and formatters..."

isort d8s_grammars/ tests/

black d8s_grammars/ tests/

mypy d8s_grammars/ tests/

pylint --fail-under 9 d8s_grammars/*.py

flake8 d8s_grammars/ tests/

bandit -r d8s_grammars/

# we run black again at the end to undo any odd changes made by any of the linters above
black d8s_grammars/ tests/
