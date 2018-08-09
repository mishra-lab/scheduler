# Scheduler

## Introduction
This project aims to make the task of creating schedules for clinicians automatic. 

## Features
- [x] Quick and easy generation of schedules given constraints
- [x] Integration with Google Calendar
- [ ] (WIP) Robust and intuitive graphical user interface 

## Building Binaries
### Required Packages
The code makes use of linear programming library [PuLP](https://github.com/coin-or/pulp#installation) and [Google Calendar API](https://developers.google.com/calendar/quickstart/python#step_2_install_the_google_client_library).

To package the program into executables, we make use of [PyInstaller](http://www.pyinstaller.org/downloads.html#installation).

**Note**: Choose the correct script for your architecture. If you intend to build a 32-bit binary, check that you have a 32-bit python installation. Make sure to install the required packages using 32-bit `pip` and put 32-bit python at the beginning of your path. Likewise, if you intend to build a 64-bit binary make sure everything is setup using 64-bit python.

### 32-bit
```sh
> git clone git@github.com:c-uhs/scheduler.git
> cd scheduler
> git checkout lp-blocks        # currently, the main branch of the code
> cd scripts\
> sh make_exe32.sh              # this will create a folder called `dist_32` under scheduler with 2 exe files
```

### 64-bit
```sh
> git clone git@github.com:c-uhs/scheduler.git
> cd scheduler
> git checkout lp-blocks        # currently, the main branch of the code
> cd scripts\
> sh make_exe64.sh              # this will create a folder called `dist_64` under scheduler with 2 exe files
```
