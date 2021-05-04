#!/bin/bash

python3 -m pip install bs4;
python3 -m pip install configparser;
python3 -m pip install pyinstaller;
python3 -m pip install python-crontab;
python3 -m pip install pillow;
if [[ "$(uname -s)" == 'Linux' ]]; then
    sudo apt-get install python3-pil.imagetk -y;
fi
python3 -m pip install requests;
python3 -m pip install tk;
