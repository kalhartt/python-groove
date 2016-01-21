Installation
------------

To install python-groove, you must have libgroove 4.x and a C complier
installed on your system. Then to install, use the following command:

.. code-block:: bash

    pip install git+https://github.com/kalhartt/python-groove.git

Development Setup
-----------------

As always, it is recommended to isolate the development environment as much as
possible. For that reason, the following steps outline how to build libgroove
locally and create a python venv that installs and uses the local libgroove.
Example installation will be done in :samp:`~/dev`, adjust paths as you see fit.

.. code-block:: bash

    # Make / cd into the development directory
    mkdir -p ~/dev && cd $_

    # Checkout libgroove 4.3.0 source
    git clone https://github.com/andrewrk/libgroove --branch 4.3.0

    # Build libgroove
    mkdir ~/dev/libgroove/build && cd $_
    cmake ..
    make

    # Checkout python-groove source
    cd ~/dev
    git clone https://github.com/kalhartt/python-groove

    # Create a python venv
    cd ~/dev/python-groove
    pyvenv venv
    source venv/bin/activate

    # Build python-groove
    export CFLAGS="-I${HOME}/dev/libgroove/ -L${HOME}/dev/libgroove/build"
    export LD_LIBRARY_PATH="${HOME}/dev/libgroove/build:${LD_LIBRARY_PATH}"
    pip install -e .

After the one time setup, continued development only requires setting
:samp:`LD_LIBRARY_PATH` and activating the python venv. For convenience, you
may consider adding the library path to the venv activate script.
