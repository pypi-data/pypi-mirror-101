#!/usr/bin/env bash
#xwtools
#xuwei@2020
python setup.py sdist bdist_wheel
twine upload dist/*
