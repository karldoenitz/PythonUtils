#!/usr/bin/env bash

python setup.py sdist
python setup.py install_lib
rm -rf ./build/ ./c_embedding.egg-info/ ./dist/
