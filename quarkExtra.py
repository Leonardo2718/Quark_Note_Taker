#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Project: Quark Note Taker
File: quarkExtra.py
Author: Leonardo Banderali
Created: August 3, 2014
Last Modified: August 14, 2014

Description:
    This file contains extra global data and functions for other Quark source files.


Copyright (C) 2014 Leonardo Banderali

License:

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
"""


#~import modules~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#python modules
import os
import json

#Qt objects
#from PyQt5.QtCore import QString
#from PyQt5.QtGui import *
#from PyQt5.QtWidgets import *


#~extra data~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#load config data from JSON  config file
configFile = open("config.json", "r")
config = json.loads( configFile.read() )
configFile.close()

#function to save changed settings
def saveCurrentConfigSettings(data=None):
    """Write changed configs to the config file."""

    configFile = open("config.json", "w")
    if data == None:
        data = config
    jsonData = json.dumps(data, sort_keys=True, indent = 4)
    configFile.write( jsonData )
    configFile.close()

def makeAbsoluteFromHome(pathString):
    """Returns an absolute path string by replacing a '~' with the path
to the users home directory.  If 'pathString' does not contain a '~', then
the string itself is returned."""

    return os.path.expanduser(pathString)
