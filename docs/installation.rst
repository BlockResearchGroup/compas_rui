********************************************************************************
Installation
********************************************************************************

.. warning::

    ``compas_rui`` is meant to be used in Rhino 8, with the new CPython runtime.
    Outside of Rhino(8), or in combination with IronPython in Rhino 8, it will simply not work.


Stable
======

To use ``compas_rui`` in your Rhino CPython scripts,
use the requirements notation of the Rhino ScriptEditor,
by adding a comment to the top of your script files.

.. code-block:: python

    # r: compas_rui

Alternatively, you can install the package manually from PyPI,
using the `python3.9` executable that ships with Rhino.

.. code-block:: bash

    /path/to/rhino/python3.9 -m pip install compas_rui


Latest
======

The latest version can be installed from local source.

.. code-block:: bash

    git clone https://github.com/blockresearchgroup/compas_rui.git
    cd compas_rui
    /path/to/rhino/python3.9 -m pip install -e .


Development
===========

To install `compas_rui` for development, install from local source with the "dev" requirements.

.. code-block:: bash

    git clone https://github.com/blockresearchgroup/compas_rui.git
    cd compas_rui
    /path/to/rhino/python3.9 -m pip install --upgrade pip
    /path/to/rhino/python3.9 -m pip install -e ".[dev]"
