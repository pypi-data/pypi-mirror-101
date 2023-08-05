#!/usr/bin/env bash

set -euxo pipefail

echo "Running linters and formatters..."

isort d8s_xml/ tests/

black d8s_xml/ tests/

mypy d8s_xml/ tests/

pylint --fail-under 9 d8s_xml/*.py

flake8 d8s_xml/ tests/

bandit -r d8s_xml/

# we run black again at the end to undo any odd changes made by any of the linters above
black d8s_xml/ tests/
