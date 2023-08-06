#!/bin/bash

# Fail early
set -e

coverage run --branch --omit=tests/*,venv/* -m pytest -p no:cacheprovider tests
coverage report --fail-under=100 --show-missing --skip-covered

echo "--Black--"
black --diff --line-length=79 bencode tests setup.py

echo "--Flake8--"
flake8 bencode tests setup.py

echo "--Isort--"
isort --check-only --diff bencode tests setup.py

echo "--Mypy--"
mypy --cache-dir=/dev/null --ignore-missing-imports bencode tests setup.py

echo "--Pylint--"
pylint --score=no bencode tests setup.py
