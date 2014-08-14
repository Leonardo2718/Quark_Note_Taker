#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Project: Quark Note Taker
File: quarknotebookmodel.py
Author: Leonardo Banderali
Created: August 12, 2014
Last Modified: August 13, 2014

Description:
    This file contains the class used to represent a quark notebook in the note manager.


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


#~notebook model class~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class QuarkNotebookModel:
    """Subdirectories located in the Quark notes directory (defined by its path in
'config.json' under "notes_dir") are represented by this class in the Quark
note manager."""

    def __init__(self, dirPath):
        """Initialize data for the model."""

        self._notebookDir = QFileInfo(dirPath)
        q = QFileIconProvider()
        self._icon = q.icon(self._notebookDir)
        self._notes = []
        self._parent = None


    def noteAt(self, i):
        """Returns the note at a given index."""

        if i > 0 and i < len(self._notes):
            return self._notes[i]
        else:
            return None


    def noteCount(self):
        """Returns the number notes inside this notebook."""

        return len(self._notes)


    def getName(self):
        """Returns the name of this notebook/directory."""

        return self._notebookDir.fileName()


    def getIcon(self):
        """Returns the icon to be displayed in the Quark note manager."""

        return self._icon


    def getParent(self):
        """Returns the parent notebook.  Because notebooks must be in the root
of the model 'None' is always returned."""

        return self._parent
