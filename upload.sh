#!/bin/bash

git add .
git commit -m $1

# 如何 $2 长度大于2，则上传到pypi
if [ ${#2} -gt 2 ]; then
    git tag $2
    rm -rf dist
    rm -rf build
    rm -rf zfuns.egg-info
    python -m pip install --upgrade pip setuptools wheel twine ez_setup
    python setup.py sdist
    python -m twine upload dist/*
fi

git push --tags