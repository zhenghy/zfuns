#!/bin/bash


#####!git init#####
#git init
#git remote add github https://github.com/zhenghy/zfuns.git
#git remote add gitee https://gitee.com/zhenghy/zfuns.git
#####!git init END#####



git add .
git commit -m """$1"""

python -m pip install --upgrade pip setuptools wheel twine ez_setup
python setup.py sdist
python -m twine upload dist/*

git push -u github master
git push -u gitee master
rm -rf dist
rm -rf build
rm -rf zfuns.egg-info