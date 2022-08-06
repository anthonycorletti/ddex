#!/bin/sh -ex

mypy ddex tests docs_src
flake8 ddex tests docs_src
black ddex tests docs_src --check
isort ddex tests docs_src --check-only
