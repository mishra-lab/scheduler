# Scheduler

## Introduction
This project aims to make the task of creating schedules for clinicians automatic. 

## Features
- [x] Quick and easy generation of schedules given constraints
- [x] Integration with Google Calendar
- [x] Robust and intuitive graphical user interface 

## Building Binaries
### Required Packages
The code makes use of linear programming library [PuLP](https://github.com/coin-or/pulp#installation), [Google Calendar API](https://developers.google.com/calendar/quickstart/python#step_2_install_the_google_client_library) and [PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro) To package the program into executables, we make use of [PyInstaller](http://www.pyinstaller.org/downloads.html#installation).

**Note**: You must use a 32-bit Python 3+ installation together with the above mentioned packages in order
to successfully build the executable.

```sh
> git clone git@github.com:c-uhs/scheduler.git
> sudo pip install -r scheduler\src\requirements.txt
> cd scheduler\scripts
> sh make_exe.sh
```

This will create a `dist` folder under `scheduler` with the scheduler executable file.
If you want to run the executable on a computer without PuLP installed, you must place the COIN-OR Branch-and-Cut (CBC) 32-bit executable (version 2.9.9) together with the scheduler executable. You can find it at https://projects.coin-or.org/Cbc.