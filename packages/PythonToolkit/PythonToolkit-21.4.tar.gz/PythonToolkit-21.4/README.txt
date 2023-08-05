README.txt
----------
Python Toolkit (ptk) is an interactive environment for python. Based around a 
set of interacting tools it includes an interactive console (with support for 
multiple python interpreters and GUI mainloops), a simple python source editor,
a python path manager and namespace browser.


INSTALLING
----------
PTK is now available from pypi so installing is suggested via pip:
$ pip install pythontoolkit

This will install PTK.exe launch script in your python installation/bin folder.
If python is available on your path, launch via $PTK

UPGRADING
---------
If you are upgrading from previous versions the configuration may have changed
between versions, this can give strange effects with window layouts etc. To fix
any problems it is recommended to run:

PTK --clear_settings

This will clear any previously stored settings from previous versions. 
Alternatively you can delete the .PTK folder in the home directory.

LICENSE
-------
MIT compatible see LICENSE.txt
