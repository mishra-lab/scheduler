#!/bin/bash

# check for python 3
ret=$(python -c 'import sys; print("%i" % (sys.hexversion>0x03000000))')
if [ $ret -eq 0 ]; then
    echo "Need Python 3+ to continue."
    exit 1
fi

# check for 64bit python
ret=$(python -c "import platform; print(platform.architecture()[0])")
if ! [ $ret = "64bit" ]; then
    echo "Need 64bit version of Python to continue."
    exit 1
fi

# check for PyInstaller
if ! [ $(command -v pyinstaller) ]; then
    echo "Need PyInstaller to continue."
    exit 1
fi

# run pyinstaller
echo "Building scheduler.exe..."
pyinstaller ../src/main.py -F -n scheduler --distpath ../dist_64

echo "Building config_manager.exe..."
pyinstaller ../src/config_manager.py -F --distpath ../dist_64
