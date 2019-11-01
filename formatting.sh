#!/bin/bash
# Formatting code using yapf
yapf -ir src/loon/__init__.py -vv
yapf -ir src/loon/skeleton.py -vv
yapf -ir src/loon/classes.py -vv
yapf -ir src/loon/utils.py -vv
yapf -ir src/loon/tool.py -vv