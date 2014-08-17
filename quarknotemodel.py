#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Project: Quark Note Taker
File: quarknotemodel.py
Author: Leonardo Banderali
Created: August 12, 2014
Last Modified: August 17, 2014

Description:
    This file contains the class used to represent a quark note in the note manager.


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



#~import modules~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#python modules
import sys
import os

#Qt objects
from PyQt5.QtCore import QFileInfo
#from PyQt5.QtGui import *
from PyQt5.QtWidgets import QFileIconProvider



#~note model class~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class QuarkNoteModel:
    """Files located in the Quark notes directory (defined by its path in
'config.json' under "notes_dir") are represented by this class in the Quark
note manager."""

    def __init__(self, fileInfo, _parent = None):
        """Initializes data for the model."""

        self._noteFile = QFileInfo(fileInfo)
        q = QFileIconProvider()
        self._icon = q.icon(self._noteFile)
        self._parent = _parent


    def getIcon(self):
        """Returns the icon to be displayed in the Quark note manager."""

        return self._icon


    def getName(self):
        """Returns the file name of the note."""

        return self._noteFile.fileName()


    def getFilePath(self):
        """Returns path to the note."""

        return self._noteFile.absoluteFilePath()


    def getParent(self):
        """Returns the parent notebook."""

        return self._parent


    def setNewParent(self, newParent):
        """Set a new parent for the note."""

        self._parent = newParent
