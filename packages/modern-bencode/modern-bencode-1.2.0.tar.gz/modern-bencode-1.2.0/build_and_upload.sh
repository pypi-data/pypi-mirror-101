#!/bin/bash

# Fail early
set -e

rm -rf build dist
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*
rm -rf .eggs build dist modern_bencode.egg-info