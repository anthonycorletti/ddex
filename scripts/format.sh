#!/bin/sh -ex

# Sort imports one per line, so autoflake can remove unused imports
isort --force-single-line-imports ddex tests docs_src scripts

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place ddex tests docs_src scripts --exclude=__init__.py
black ddex tests docs_src scripts
isort ddex tests docs_src scripts
