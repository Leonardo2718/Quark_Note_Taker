#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Project: Quark Note Taker
File: quarknotemanagermodel.py
Author: Leonardo Banderali
Created: August 13, 2014
Last Modified: August 15, 2014

Description:
    This file contains the class which models the Quark note manager.


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
import shutil

#Qt objects
from PyQt5.QtCore import Qt, QAbstractItemModel, QModelIndex, QVariant
#from PyQt5.QtGui import *
#from PyQt5.QtWidgets import *

#Quark specific
import quarkExtra
from quarknotebookmodel import QuarkNotebookModel
from quarknotemodel import QuarkNoteModel


#~notebook model class~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class QuarkNoteManagerModel(QAbstractItemModel):
    """This class represents the data model used for the Quark note manager.
Items in this model represent the files (notes) and subdirectories(notebooks)
in the user specified notes directory.  Any subdirectory is considered to be
and notebook and every file is considered a note.  Notebooks are only allowed
to be in the root of the model.  By extension, notebooks can only contain notes
and cannot have other "sub-notebooks".  However, the notes directory (root of
the model) can have both notes and notebooks.  The directory tree shoul look
something like this:

Quark Notes Directory (root)
 |
 |-- Note 1
 |-- Note 2
 |-- Note 3
 +-- Notebook A
 |    |
 |    |-- Note 1
 |    |-- Note 2
 |
 +-- Notebook B
 |    |
 |    |-- Note 1
 |    |-- Note 2

Note: I arbitrarily decided that notebooks are always displayed after notes.
"""

    def __init__(self, parent):
        """Initializes the model by gowing through the notes directory tree."""

        super(QuarkNoteManagerModel, self).__init__(parent)

        self._noteList = []     #initialize empty list of notes
        self._notebookList = [] #initialize empty list of notebooks

        notesDir = quarkExtra.makeAbsoluteFromHome(quarkExtra.config["notes_dir"])  #get the Quark notes directory from the config file

        if not os.path.exists(notesDir):                            #if the the notes directory does note exits, open/create one
            promptDialog = quarkExtra.GetNotesDirDialog(notesDir, parent)   #prompt the user for for a directory path
            promptDialog.exec()                                             #
            notesDir = promptDialog.getNotesPath()                          #
            quarkExtra.config["notes_dir"] = notesDir                       #save the directory path
            if not os.path.exists(notesDir):                                #if the directory does not exits yet, create it
                os.makedirs(notesDir)
            readmeFile = os.path.join(os.path.dirname(os.path.realpath(__file__)), "README.md") #get path to Quark's main 'README.md' file
            if os.path.exists(readmeFile):                                  #if it exists, copy it to the notes directory
                shutil.copyfile(readmeFile, os.path.join(notesDir, "README.md") )

        #load all the notes and notebooks from the notes directory
        if os.path.exists(notesDir):
            for item in os.listdir(notesDir):                   #for every item in the notes directory

                itemPath = os.path.join(notesDir, item)             #get absolute path to the item

                if os.path.isfile(itemPath):                        #if the item is a file/note
                    self._noteList.append( QuarkNoteModel(itemPath) )           #append a new note to the notes list

                elif os.path.isdir(itemPath):                       #if the item is directory/notebook
                    self._notebookList.append( QuarkNotebookModel(itemPath) )   #append a new note to the notebooks list


    def index(self, row, column, itemParent = QModelIndex() ):
        """Returns the 'QModelIndex' of an item based on its (row,column) position
inside its parent."""

        returnIndex = QModelIndex()         #index to be returned

        if column == 0 and row >= 0:        #note that only one column is used in this model

            if itemParent.isValid() and type(itemParent.internalPointer()) is QuarkNotebookModel: #if the index provided is valid and the item is a notebook
                notebook = itemParent.internalPointer() #get the notebook
                note = notebook.noteAt(row)             #get the note from the notebook
                if not (note is None):                  #if the note exists, create an index for it
                    returnIndex = self.createIndex(row, column, note)

            else:                               #else assume the parent is the root
                if row < len(self._noteList):                               #check if item is a note
                    note = self._noteList[row]
                    returnIndex = self.createIndex(row, column, note)
                elif row < len(self._noteList) + len(self._notebookList):   #check if item is a notebook
                    notebook = self._notebookList[row - len(self._notebookList)]
                    returnIndex = self.createIndex(row, column, notebook)

        return returnIndex


    def parent(self, itemIndex):
        """Returns the 'QModelIndex' of an item's parent.  The item specified using its 'QModelIndex'."""

        returnIndex = QModelIndex()     #index to be returned

        if itemIndex.isValid()  and type(itemIndex.internalPointer()) is QuarkNoteModel:    #only check for parent if index is valid and item is a note,
                                                                                            #  in which case it could be in a notebook and have a parent
            note = itemIndex.internalPointer()          #get the note
            noteParent = note.getParent()               #get the parent
            if not (noteParent is None):                #if the note has no defined parent, then its parent must be the model root
                indexRow = self._notebookList.index(noteParent)         #get the list/row index of the parent (which must be in the root of the model)
                returnIndex = self.createIndex(indexRow, 0, noteParent) #create the parent index

        return returnIndex


    def rowCount(self, parentIndex):
        """Returns the number of rows in a given item, wich is identified by its 'QModelIndex'."""

        count = 0

        if parentIndex.isValid():                       #if the index provided is valid
            if type(parentIndex.internalPointer()) is QuarkNotebookModel:#if the item is a notebook
                notebook  = parentIndex.internalPointer()                   #get the notebook
                count = notebook.noteCount()                                #get the number of notes
        else:                                           #else, the item must be root
            count = len(self._noteList) + len(self._notebookList)

        return count


    def columnCount(self, parentIndex):
        """Returns the number of columns in a given item.  Because of the nature of this
model, this method always returns '1'."""

        return 1


    def data(self, itemIndex, role = Qt.DisplayRole):
        """Returns data for the viewing class."""

        data = QVariant()

        if role == Qt.DisplayRole:
            data = QVariant( itemIndex.internalPointer().getName() )
        elif role == Qt.DecorationRole:
            data = QVariant( itemIndex.internalPointer().getIcon() )

        return data


    def headerData(self, section, orientation, role = Qt.DisplayRole):
        """Returns data for the model display header."""

        data = QVariant()       #initialize return data

        if role == Qt.DisplayRole:              #if display data is requested
            if section == 0:                        #if data for the first column is requested
                data = QVariant("Quark Notes and Notebooks")    #set the data

        return data             #return the data
