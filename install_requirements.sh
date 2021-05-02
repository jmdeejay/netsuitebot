#!/bin/bash

pip install bs4;
pip install configparser;
pip install pyinstaller;
pip install python-crontab;
pip install pillow;
if [[ "$(uname -s)" == 'Linux' ]]; then
    sudo apt-get install python3-pil.imagetk -y;
fi
pip install requests;
pip install tk;
