#!/bin/sh -ex

./scripts/lint.sh

# pytest --cov=ddex --cov=tests --cov-report=term-missing --cov-report=xml -o console_output_style=progress --disable-warnings --cov-fail-under=100 ${@}
# TODO: get back to 100% coverage – pending network connection removal from tests
pytest --cov=ddex --cov=tests --cov-report=term-missing --cov-report=xml -o console_output_style=progress --disable-warnings ${@}
