#!/usr/bin/env python
"""
Python distutils setup.py script:

Usage:
------

 * Recommended: Install via pip / pypi for the latest version *
 
    $ pip install pythontoolkit
 
 
Install as a python package [not manual uninstall will be required]
    $ python setup.py install

Make a wheel and isntall [pip install wheel]
    $ python setup.py sdist bdist_wheel
    $ pip install wheel_file.whl
    
Install local copy via pip [builds wheel, removes previous versions and installs via pip]
    $ setup.py pip_install
    
Upload to pypi [requires authorisation]
    $ setup.py upload

editable install
pip install -e /path/to/package
    
"""
from setuptools import find_packages, setup, Command
import os
import shutil
import os.path
import sys
from shutil import rmtree


import ptk_lib

#-------------------------------------------------------------------------------
# Add useful commands
#-------------------------------------------------------------------------------
class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            here = os.path.abspath(os.path.dirname(__file__))
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system('"{}" setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist//*")

        sys.exit()

class PipCommand(Command):
    """Support setup.py pip_install."""

    description = "Install local copy via pip [builds wheel, removes previous versions and installs via pip]"
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            here = os.path.abspath(os.path.dirname(__file__))
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system('"{}" setup.py sdist bdist_wheel --universal'.format(sys.executable))
        
        self.status("Uninstalling previous version using pip [remove using pip uninstall pythontoolkit] …")
        os.system("pip uninstall pythontoolkit" )
        
        self.status("Installing Wheel using pip [remove using pip uninstall pythontoolkit] …")
        whl = [fname for fname in  os.listdir('dist') if fname.endswith('.whl')][0]
        os.system("pip install dist\{}".format(whl) )

        sys.exit()

#-------------------------------------------------------------------------------
# Collect data for the distutils setup() call.
#-------------------------------------------------------------------------------
# Package meta-data.
NAME = "PythonToolkit"
DESCRIPTION = "Framework for building multiple process applications."
URL = "http://pythontoolkit.sourceforge.net"
EMAIL = "tcharrett@gmail.com"
AUTHOR = "Tom Charrett"
REQUIRES_PYTHON = ">=3.7.6"
VERSION = ptk_lib.VERSION

# What packages are required for this module to be executed?
REQUIRED = ["wxpython"]

# What packages are optional?
EXTRAS = {"opt": ["numpy"]}

#scripts/exe lauchers to generate
#SCRIPTS = ['PTKengine.pyw']
ENTRY_POINTS = { 'gui_scripts':['PTK = ptk_lib.PTK:main','PTKengine = ptk_lib.PTKengine:main']}

PACKAGE_DATA = {'ptk_lib': ['resources/tips.txt',   
                            'resources/ptk.ico',
                            'resources/ptkicon.svg']}
DATA_FILES =[ 
            ('.',[ 'README.txt','LICENSE.txt','CHANGES.txt']),
            ]

DESCRIP = "PythonToolkit (PTK) an interactive python environment"
LONG_DESCRIP = """PythonToolkit (PTK) is an interactive environment for python. 
It was designed to provide a python based environment similiar to Matlab
for scientists and engineers however it can also be used as a general
purpose interactive python environment."""

#Find packages to install
PACKAGES = find_packages()

#-------------------------------------------------------------------------------
#Do the setup call
#-------------------------------------------------------------------------------
setup(
    name = 'PythonToolkit',
    version = VERSION,
    description = DESCRIP,
    long_description = LONG_DESCRIP,
    author = AUTHOR,
    author_email = EMAIL,
    url = URL,
    packages = PACKAGES,
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Topic :: Scientific/Engineering",
        "Intended Audience :: Developers",],
    #scripts = SCRIPTS,
	entry_points = ENTRY_POINTS,
    package_data = PACKAGE_DATA,
    data_files = DATA_FILES,
    #upload command
    cmdclass={"upload": UploadCommand, "pip_install": PipCommand},
)
