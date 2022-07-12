#!/bin/sh -ex

# Sort imports one per line, so autoflake can remove unused imports
isort --force-single-line-imports ddex tests scripts

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place ddex tests scripts --exclude=__init__.py
black ddex tests scripts
isort ddex tests scripts
