#!/bin/bash

pip install virtualenv
virtualenv abhismartmirror
source ./abhismartmirror/bin/activate
pip install -r requirements.txt
pip install --global-option='build_ext' --global-option='-I/usr/local/include' --global-option='-L/usr/local/lib' pyaudio
