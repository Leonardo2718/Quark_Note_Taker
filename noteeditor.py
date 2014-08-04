#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Project: Quark Note Taker
File: noteeditor.py
Author: Leonardo Banderali
Created: August 3, 2014
Last Modified: August 3, 2014

Description:
    This file contains the class wich defines the markdown note editor.


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
#from PyQt5.QtCore import *
#from PyQt5.QtGui import *
from PyQt5.QtWidgets import QPlainTextEdit

#Quark specific
from mdhighlighter import MDHighlighter


#~note editor~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class NoteEditor(QPlainTextEdit):
    """The note editing class used uses a plain text editing window to edit markdown files (notes)."""
    def __init__(self, parent):
        super(NoteEditor, self).__init__(parent)
        self.mdHighlighter = MDHighlighter( self.document() )
    #%%% To do: use 'keyPressEvent' to implement auto-indent %%%
