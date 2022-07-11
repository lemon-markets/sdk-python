#! /bin/sh

set -x

mypy lemon tests
pylint lemon tests
black lemon tests --check
isort lemon tests --check-only
