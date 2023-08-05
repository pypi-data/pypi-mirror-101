#!/usr/bin/env bash

set -euxo pipefail

echo "Running linters and formatters..."

isort d8s_emails/ tests/

black d8s_emails/ tests/

mypy d8s_emails/ tests/

pylint --fail-under 9 d8s_emails/*.py

flake8 d8s_emails/ tests/

bandit -r d8s_emails/

# we run black again at the end to undo any odd changes made by any of the linters above
black d8s_emails/ tests/
