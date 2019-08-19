# Scheduler
Fast and easy generation of schedules for use in hospital departments. 
Built in Python.

## Features
- [x] Generation of schedules given clinician requests
- [x] Robust and intuitive Qt GUI
- [x] Excel exporting options

## Download it
You can find the latest version of the executable at the [releases area](https://github.com/c-uhs/scheduler/releases). 
The executable comes pre-bundled with the COIN-OR LP solver. 

## Build it yourself
### Get COIN-OR LP solver
Before compiling the executable, you must download the 32bit version of the COIN-OR Branch-and-Cut (CBC)
executable, to be bundled together with the scheduler. Download the 2.9.9 version from [Bintray](https://bintray.com/coin-or/download/Cbc/2.9.9), unzip it, and place it under the ```scheduler\scripts``` folder.

### Run the script
**Note**: You must use a 32-bit Python 3 installation!

```sh
> git clone git@github.com:c-uhs/scheduler.git
> sudo pip install -r scheduler\src\requirements.txt
> cd scheduler\scripts
> sh make_exe.sh
```

This will create a `dist` folder under the root `scheduler` folder containing the executable file.
