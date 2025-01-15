#!/bin/bash


#####!git init#####
#git init
#git remote add gitee https://gitee.com/zhenghy/zfuns.git
#git remote add github https://ghp_*@github.com/zhenghy/zfuns.git
#git checkout -b master
#git add .
#git commit -m "init"
#git push -u gitee master
#git push -u github master
#####!git init END#####



git add .
git commit -m """$1"""

python -m pip install --upgrade pip setuptools wheel twine ez_setup
python setup.py sdist
python -m twine upload dist/*

git push github
git push gitee
rm -rf dist
rm -rf build
rm -rf zfuns.egg-info