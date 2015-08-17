#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Project: Quark Note Taker
File: quarkExtra.py
Author: Leonardo Banderali
Created: August 3, 2014
Last Modified: August 16, 2015

Description:
    This file contains extra global data and functions for other Quark source files.


Copyright (C) 2015 Leonardo Banderali

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
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QDialogButtonBox, QFileDialog



#~extra data~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#load session settings from JSON file
sessionFile = open("session.json", "r")
session = json.loads( sessionFile.read() )
sessionFile.close()


#function to save changed settings
def saveCurrentConfigSettings(data=None):
    """Write changed configs to the config file."""

    configFile = open("config.json", "w")
    if data == None:
        data = config
    jsonData = json.dumps(data, sort_keys=True, indent = 4)
    configFile.write( jsonData )
    configFile.close()



#function to save the current session
def saveCurrentSession(sessionData = None):
    """Write session data to the JSON file."""

    sessionFile = open("session.json", "w")
    if sessionData == None:
        sessionData = session
    jsonData = json.dumps(sessionData, sort_keys=True, indent = 4)
    sessionFile.write(jsonData)
    sessionFile.close()



#function to make a path that is relative from the home directory, absolute
def makeAbsoluteFromHome(pathString):
    """Returns an absolute path string by replacing a '~' with the path
to the users home directory.  If 'pathString' does not contain a '~', then
the string itself is returned."""

    return os.path.expanduser(pathString)



#a dialog to prompt the user for the notes directory
class GetNotesDirDialog(QDialog):
    """This class creates a dialog window used to prompt the user for the path
to the Quark notes directory.  If the user cancels the dialog, the current directory
of execution is returned."""

    def __init__(self, defaultPath, parent = None):
        """Initializes the dialog window."""

        super(GetNotesDirDialog, self).__init__(parent)

        self._dirPath = defaultPath #set the path to be returned

        #set the layout
        self._layout = QVBoxLayout(self)    #create the main layout for the dialog
        self._layout.setSpacing(30)         #create some spacing between the items

        #add items to the dialog
        self._dialogText = QLabel(  #text for instructions
        """Pleas enter a path for the Quark notes directory.  Your notebooks and notes will be stored
in this directory and can be accessed easily through the Quark note manager.  (Note: If the directory you
specify does not exists, it will be created for you.)""",self)
        self._layout.addWidget(self._dialogText)

        self._inputArea = QFrame(self)                                  #create an area for the urer to provide input
        self._inputLayout = QHBoxLayout(self._inputArea)                #layout for the input area
        self._inputLayout.setSpacing(10)                                #create some space between the button and the input field
        self._pathInput = QLineEdit(self._dirPath, self._inputArea)     #the input field
        self._browseButton = QPushButton("&Browser", self._inputArea)   #the button
        self._inputLayout.addWidget(self._pathInput)                    #add the input field to the input layout
        self._inputLayout.addWidget(self._browseButton)                 #add the button to the input layout

        self._layout.addWidget(self._inputArea)                         #add the input area to the main layout

        self._buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self._layout.addWidget(self._buttons)

        #connect signals to slots
        self._browseButton.clicked.connect(self.browsForDir)
        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)


    def getNotesPath(self):
        """Returns the path entered by the user."""

        return self._dirPath


    def browsForDir(self):
        """Opens a prompt to search for an existing directory.  The returned directory is then selected
to be the notes directory."""

        dirPath = QFileDialog.getExistingDirectory( self, "Select Notes Directory", os.path.expanduser("~") )   #get the directory from the user
        if os.path.exists(dirPath):             #if the path exists, set it as the input path
            self._pathInput.setText(dirPath)

        return


    def accept(self):
        """Executed when the 'Ok' is clickec.  Saves the provided path."""

        self._dirPath = self._pathInput.text()  #set the path
        super(GetNotesDirDialog, self).accept() #execute othere required tasks


    def reject(self):
        """Executed when 'Cancel' (or ESC key) is clicked.  Sets the notes directory path to '.'"""

        self._dirPath = "."                     #set the path
        super(GetNotesDirDialog, self).reject() #execute othere required tasks
