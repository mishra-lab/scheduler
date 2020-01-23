Installation
============

Download it
~~~~~~~~~~~
You can find the latest version of the executable from the `releases`_. 
The executable comes pre-bundled with the COIN-OR LP solver. 

.. _releases: https://github.com/c-uhs/scheduler/releases

Build it from source
~~~~~~~~~~~~~~~~~~~~
.. note::
    You must use a 32-bit Python 3 installation!

1. Get COIN-OR LP solver

    Before compiling the executable, you must download the 32bit version
    of the COIN-OR Branch-and-Cut (CBC)
    executable, to be bundled together with the scheduler. 
    Download the 2.9.9 version from `Bintray`_, unzip it, and place it 
    under the :code:`scheduler/scripts` folder.

.. _Bintray: https://bintray.com/coin-or/download/Cbc/2.9.9

2. Run the script

    .. code-block:: console

        > git clone git@github.com:c-uhs/scheduler.git
        > sudo pip install -r scheduler/src/requirements.txt
        > cd scheduler/scripts
        > sh make_exe.sh

    This will create a :code:`scheduler/dist` folder 
    containing the executable file.