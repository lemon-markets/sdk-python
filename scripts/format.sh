#! /bin/sh

set -x

autoflake --remove-all-unused-imports --in-place -r lemon tests
isort --profile black lemon tests
black lemon tests
