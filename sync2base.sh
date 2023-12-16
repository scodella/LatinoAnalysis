#!/bin/sh -x
git checkout base
git fetch
#git pull
git checkout SUS23002
git merge origin/base

