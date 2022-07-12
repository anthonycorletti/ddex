#!/bin/sh -ex

mypy ddex tests
flake8 ddex tests
black ddex tests --check
isort ddex tests scripts --check-only
