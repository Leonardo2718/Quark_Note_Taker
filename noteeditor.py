#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Project: Quark Note Taker
File: noteeditor.py
Author: Leonardo Banderali
Created: August 3, 2014
Last Modified: December 21, 2015

Description:
    This file contains the class wich defines the markdown note editor.


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



#~import modules~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#python modules
import sys
import os
import locale
import enchant

#Qt objects
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtGui import QTextOption, QTextCursor, QFontMetrics, QFont
from PyQt5.QtWidgets import QPlainTextEdit, QMenu, QActionGroup, QAction

#Quark specific
from highlighter import Highlighter



#~note editor~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class NoteEditor(QPlainTextEdit):
    """The note editing class used uses a plain text editing window to edit markdown files (notes)."""

    def __init__(self, parent):
        super(NoteEditor, self).__init__(parent)
        self.highlighter = Highlighter( self.document() )

        # the language dictionary to be used
        self.dictionary = None
        self.highlighter.setDictionary(self.dictionary)

        # create dictionary selector menu
        self.dictionarySelector = QMenu("&Dictionary")
        self.dictionaryActions = QActionGroup(self)

        self.noDicitionaryAction = self.dictionaryActions.addAction("None")
        self.noDicitionaryAction.setCheckable(True)
        self.dictionarySelector.addAction(self.noDicitionaryAction)

        self.defaultDicitionaryAction = self.dictionaryActions.addAction("Default")
        self.defaultDicitionaryAction.setCheckable(True)
        self.dictionarySelector.addAction(self.defaultDicitionaryAction)

        self.dictionarySelector.addSeparator()

        for lang in enchant.list_languages():
            langAction = self.dictionaryActions.addAction(lang)
            langAction.setCheckable(True)
            self.dictionarySelector.addAction(langAction)

        # connect signal to change language dictionary and set the default language
        self.dictionaryActions.triggered.connect(self.changeDictionary)
        self.defaultDicitionaryAction.trigger()

        # configure the custom context menu for spelling suggestions
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

        # settings
        self.setWordWrapMode(QTextOption.NoWrap)
        self.noteFilePath = ""                  #stores path to the file being edited
        self.setFont(QFont("Monospace"))
        tabWidth = QFontMetrics( self.currentCharFormat().font() ).width("    ")#get the width of four spaces
        self.setTabStopWidth(tabWidth)                                          #set the default tab width to be that of four spaces

    #%%% To do: use 'keyPressEvent' to implement auto-indent %%%


    def getDictionarySelector(self):
        return self.dictionarySelector


    def changeDictionary(self, action):
        # change the language dictionary
        if action is self.noDicitionaryAction:
            self.dictionary = None
        elif action is self.defaultDicitionaryAction:
            self.dictionary = enchant.Dict(locale.getdefaultlocale()[0])
        else:
            self.dictionary = enchant.Dict(action.text())

        # rehighlight the text to find spelling errors
        self.highlighter.setDictionary(self.dictionary)
        self.highlighter.rehighlight()


    def showContextMenu(self, position):
        # select the word that was right-clicked
        textCursor = self.cursorForPosition(position)
        textCursor.select(QTextCursor.WordUnderCursor)
        word = textCursor.selectedText()

        # if a word was selected and it's misspelled, show a suggestion menu
        if word and not self.dictionary.check(word):

            # create the suggestion menu
            suggestionMenu = QMenu()
            for suggestion in self.dictionary.suggest(word):
                suggestionMenu.addAction(suggestion)
            suggestionMenu.addSeparator()
            standardMenu = self.createStandardContextMenu(position);
            standardMenu.setTitle("Other...")
            suggestionMenu.addMenu(standardMenu)

            # show suggestions
            suggestion = suggestionMenu.exec(self.mapToGlobal(position))

            # if a suggestion was selected, replace the current word with it
            if suggestion:
                textCursor.removeSelectedText()
                textCursor.insertText(suggestion.text())

        # otherwise, show the standard menu items
        else:
            self.createStandardContextMenu(position).exec(self.mapToGlobal(position))


    def openFileRequest(self, filePath):
        """Open a file using its path (string) in the editor.  Return 'True' if successful, 'False' otherwise."""

        noErrors = True                 #set return state
        noteFile = open(filePath, "r")
        if noteFile:                    #if the file was opened successfully
            self.setPlainText( noteFile.read() )    #set its contents in the editor
            self.noteFilePath = filePath            #save the file path to the internal variable
            self.noteFileChanged.emit( os.path.abspath(self.noteFilePath) ) #emit signal to notify other objects of file change
        else:                           #else, return an error
            noErrors = False

        noteFile.close()
        return noErrors


    def writeToFile(self, filePath):
        """Writes text in editor to file 'filePath'.  Return 'True' if successful, 'False' otherwise."""

        noErrors = True
        if os.path.exists(filePath):    #check if file exists
            filePath = os.path.abspath(filePath)    #make path absolute just in case...
            noteFile = open(filePath, "w")
            if noteFile:                            #if file was opened successfully
                noteFile.write( self.toPlainText() )    #write text to file
            else:
                noErrors = False
        else:
            noErrors = False

        return noErrors


    def saveFileRequest(self):
        """Saves text in editor to note file.  Return 'True' if successful, 'False' otherwise."""

        noErrors = True
        if self.noteFilePath != "":                     #if note path is set (the editor knows which file it should save to)
            noErrors = self.writeToFile( self.noteFilePath )#write text to note file
        else:
            noErrors = False

        return noErrors


    def saveAsRequested(self, filePath):
        """Save text in editor to a new file ('filePath') and set it as the new note file.  Return 'True' if successful, 'False' otherwise."""

        noErrors = True

        newFile = open(filePath, "w+")          #create the new file
        newFile.close()

        noErrors = self.writeToFile( filePath ) #write text to the new file
        if noErrors:                            #if no errors occured
            self.noteFilePath = filePath            #set the new file as the internal note file
            self.noteFileChanged.emit( os.path.abspath(self.noteFilePath) ) #emit signal to notify other objects of file change

        return noErrors


    def saveCopyAsRequested(self, filePath):
        """Save note to a new file without loading it.  Return 'True' if successful, 'False' otherwise."""

        noErrors = True

        newFile = open(filePath, "w+")          #create the new file
        newFile.close()

        noErrors = self.writeToFile( filePath ) #wrtie text to the new file

        ########################################################################################
        ### Note that 'self.noteFilePath' (path to the note file being edited) is not changed ##
        ########################################################################################

        return noErrors


    def getNoteFileName(self):
        """Returns the file name of the note being edited."""

        return os.path.basename(self.noteFilePath)


    def getNotePath(self):
        """Returns the path to the note being edited."""

        return self.noteFilePath


    #~signals~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    noteFileChanged = pyqtSignal([str]) #a signal to be emitted when 'self.noteFilePath' (path to the note file being edited) is changed
