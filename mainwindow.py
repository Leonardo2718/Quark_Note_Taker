#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Project: Quark Note Taker
File: mainwindow.py
Author: Leonardo Banderali
Created: August 3, 2014
Last Modified: August 23, 2014

Description:
    This file contains the class wich defines the main application window for Quark.


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
import sys
import os
import shutil

#extra modules
import markdown

#Qt objects
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebKit import *
from PyQt5.QtWebKitWidgets import *

#Quark specific
import quarkExtra
from noteeditor import NoteEditor
from quarknotemanagermodel import QuarkNoteManagerModel
from quarknotemodel import QuarkNoteModel
from quarknotebookmodel import QuarkNotebookModel



#~main window setup~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MainWindow(QMainWindow):
    """The main window class contains all the components of the app"""

    def __init__(self):
        super(MainWindow, self).__init__()

        #setup the main window menu
        self.mainToolBar = self.addToolBar("Main Toolbar")
        self.mainToolBar.setMovable(False)

        #create menues
        self.menu = {"File" : self.menuBar().addMenu("&File")}
        self.menu["View"] = self.menuBar().addMenu("&View")
        self.menu["Help"] = self.menuBar().addMenu("&Help")

        #create actions for 'File' menu
        self.action = {"New Note": self.menu["File"].addAction("&New Note")}
        self.action["New Notebook"] = self.menu["File"].addAction("New Note&book")
        self.action["Open"] = self.menu["File"].addAction("&Open")
        self.menu["File"].addSeparator()
        self.action["Save"] = self.menu["File"].addAction("&Save")
        self.action["Save As"] = self.menu["File"].addAction("Save &As")
        self.action["Save Copy As"] = self.menu["File"].addAction("Save &Copy As")
        self.menu["File"].addSeparator()
        self.action["Rename This Note"] = self.menu["File"].addAction("&Rename This Note")

        #create shorcuts for actions in 'File' menu
        self.action["New Note"].setShortcut( QKeySequence.New )
        self.action["New Notebook"].setShortcut( QKeySequence("Ctrl+Shift+N") )
        self.action["Open"].setShortcut( QKeySequence.Open )
        self.action["Save"].setShortcut( QKeySequence.Save )
        self.action["Save As"].setShortcut( QKeySequence("Ctrl+Shift+S") )

        #create actions for 'View' menu
        self.actionGroup = {"display mode": QActionGroup(self) }
        self.action["View Mode"] = self.actionGroup["display mode"].addAction("V&iew Mode")
        self.menu["View"].addAction( self.action["View Mode"] )
        self.action["Edit Mode"] = self.actionGroup["display mode"].addAction("&Edit Mode")
        self.menu["View"].addAction( self.action["Edit Mode"] )
        self.action["View & Edit Mode"] = self.actionGroup["display mode"].addAction("View && Edit &Mode")
        self.menu["View"].addAction( self.action["View & Edit Mode"] )
        self.menu["View"].addSeparator()
        self.action["View Editor/Preview Vertically"] = self.menu["View"].addAction("View Editor/Preview &Vertically")
        self.menu["View"].addSeparator()
        self.action["Note Manager"] = self.menu["View"].addAction("&Note Manager")

        #create shorcuts for actions in 'File' menu
        self.action["Note Manager"].setShortcut( QKeySequence("Ctrl+M") )

        #set check state for actions in 'File' menu
        self.action["View Mode"].setCheckable(True)
        self.action["Edit Mode"].setCheckable(True)
        self.action["View & Edit Mode"].setCheckable(True)
        self.action["View Editor/Preview Vertically"].setCheckable(True)
        self.action["Note Manager"].setCheckable(True)

        #create actions for 'Help' menu
        self.action["About Quark Note Taker"] = self.menu["Help"].addAction("&About Quark Note Taker")
        self.action["View GitHub Page"] = self.menu["Help"].addAction("View &GitHub Page")
        self.menu["Help"].addSeparator()
        self.action["About Qt"] = self.menu["Help"].addAction("About &Qt")

        #setup main window layout
        self.centralWidget = QSplitter(self)                #widget container to hold all others
        self.centralWidget.setOrientation(Qt.Horizontal)
        self.centralWidget.setChildrenCollapsible(False)
        self.setCentralWidget(self.centralWidget)

        #setup note manager
        self.noteManager = QTreeView(self.centralWidget)                        #manage notes in a tree display
        self.noteManager.setModel(QuarkNoteManagerModel(self))
        self.noteManager.setContextMenuPolicy(Qt.CustomContextMenu)             #set manager to display a custum menu when an item is right clicked
        self.noteManager.setSelectionMode(QAbstractItemView.SingleSelection)    #only allow for one single item to be selected at a time
        self.centralWidget.addWidget(self.noteManager)

        #create actions for the note manager
        self.managerNoteAction = {"Open Note" : QAction("Open Note", self.noteManager)}
        self.managerNoteAction["Rename Note"] = QAction("Rename Note", self.noteManager)
        self.managerNoteAction["Remove Note"] = QAction("Remove Note", self.noteManager)
        self.managerNotebookAction = {"Rename Notebook" : QAction("Rename Notebook", self.noteManager)}
        self.managerNotebookAction["Remove Notebook"] = QAction("Remove Notebook", self.noteManager)

        #setup an area to hold the note editor and previewer
        self.noteArea = QSplitter(self.centralWidget)
        self.noteArea.setChildrenCollapsible(False)
        self.centralWidget.addWidget(self.noteArea)

        #create and set the note editor
        self.noteEditor = NoteEditor(self.noteArea)
        editorSizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        editorSizePolicy.setHorizontalStretch(3)
        editorSizePolicy.setVerticalStretch(3)
        self.noteEditor.setSizePolicy(editorSizePolicy)
        self.noteArea.addWidget(self.noteEditor)

        #create and set the note previewer
        self.notePreview = QWebView(self.noteArea)          #note preview widget
        self.notePreview.page().setLinkDelegationPolicy(QWebPage.DelegateExternalLinks)
        previewSizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        previewSizePolicy.setHorizontalStretch(1)
        previewSizePolicy.setVerticalStretch(1)
        self.notePreview.setSizePolicy(previewSizePolicy)
        self.noteArea.addWidget(self.notePreview)

        #connect signals in 'File' menu to slots
        self.action["New Note"].triggered.connect(self.newNoteAction)
        self.action["New Notebook"].triggered.connect(self.newNotebookAction)
        self.action["Open"].triggered.connect(self.openFileAction)
        self.action["Save"].triggered.connect(self.saveFileAction)
        self.action["Save As"].triggered.connect(self.saveAsFileAction)
        self.action["Save Copy As"].triggered.connect(self.saveCopyAsAction)
        self.action["Rename This Note"].triggered.connect(self.renameNoteAction)

        #connect signals in 'View' menu to slots
        self.action["Note Manager"].toggled.connect(self.noteManager.setVisible)
        self.actionGroup["display mode"].triggered.connect(self.changeLayoutModeOnAction)
        self.action["View Editor/Preview Vertically"].toggled.connect(self.changeNoteDirectionOnAction)

        #connect signals in 'Help' menu to slots
        self.action["About Quark Note Taker"].triggered.connect(self.displayAboutQuark)
        self.action["View GitHub Page"].triggered.connect(self.openGithubPage)
        self.action["About Qt"].triggered.connect(self.displayAboutQt)

        #connect signals from the note editor to slots
        self.noteEditor.textChanged.connect(self.updatePreview)
        self.noteEditor.noteFileChanged.connect(self.changeTitle)
        self.noteEditor.verticalScrollBar().valueChanged.connect(self.changePreviewScrollOnEditorScroll)

        #connect signals from the note previewer to slots
        self.notePreview.page().linkClicked.connect(self.linkClickHandler)

        #connect signals from the note manager to slots
        self.noteManager.doubleClicked.connect(self.openNoteFromManager)
        self.noteManager.customContextMenuRequested.connect(self.showManagerItemMenu)
        self.managerNoteAction["Open Note"].triggered.connect(self.openSelectedNote)
        self.managerNoteAction["Rename Note"].triggered.connect(self.renameItemInManager)
        self.managerNoteAction["Remove Note"].triggered.connect(self.removeItemInManager)
        self.managerNotebookAction["Rename Notebook"].triggered.connect(self.renameItemInManager)
        self.managerNotebookAction["Remove Notebook"].triggered.connect(self.removeItemInManager)

        #last minute configs
        self.changeTitle("")        #set default window title
        self.loadSession()

        #setup timer to trigger autosave
        self.autosaveTimer = QTimer(self)                           #create the timer
        self.autosaveTimer.timeout.connect(self.saveFileAction)     #connect the timer to the save method
        autosave_interval = int(quarkExtra.config["autosave_every"])#get the time interval from the config file (in milliseconds)
        self.autosaveTimer.start(autosave_interval)                 #set the interval and start the timer


    def closeEvent(self, event):
        """Cleanup and close the main window."""

        self.saveFileAction()   #save the current note
        self.saveSession()      #save the user's session

        #call parent method
        super(MainWindow, self).closeEvent(event)


    def changeLayoutModeOnAction(self, action):
        """Changes the layout of the editing area (editor + preview window) based on the 'view' menu action triggered."""

        if action == self.action["View Mode"] :         #if the user choses to only display the note preview
            self.noteEditor.setVisible(False)
            self.notePreview.setVisible(True)

        elif action == self.action["Edit Mode"] :       #if the user choses to only display the note editor
            self.noteEditor.setVisible(True)
            self.notePreview.setVisible(False)

        elif action == self.action["View & Edit Mode"] :  #if the user choses to display both the note editor and note preview
            self.noteEditor.setVisible(True)
            self.notePreview.setVisible(True)


    def changeNoteDirectionOnAction(self, isVertical):
        """Changes direction (horizontal/vertical) of the note editor and previewer."""

        if not isVertical:
            self.noteArea.setOrientation(Qt.Horizontal)
        elif isVertical:
            self.noteArea.setOrientation(Qt.Vertical)


    def mdNoteToHtml(self, noteMarkdown):
        """Converts note text/markdown to an html document"""

        #create markdown parser
        parser = markdown.Markdown(['extra', 'toc', 'sane_lists'])

        #create an html document using the start (top/head) HTML template
        htmlFile = open(quarkExtra.config["start_html_template_file"] , "r")
        htmlDoc = htmlFile.read()
        htmlFile.close()

        #convert markdown note to html and append the result to the HTML document
        htmlDoc = htmlDoc + parser.convert(noteMarkdown)

        #append the end (bottom/foot) template to the HTML document
        htmlFile = open(quarkExtra.config["end_html_template_file"], "r")
        htmlDoc = htmlDoc + htmlFile.read()
        htmlFile.close()

        return htmlDoc


    def updatePreview(self):
        """Converts the Markdown note to HTML and loads it into the previewer."""

        htmlDocument = self.mdNoteToHtml( self.noteEditor.toPlainText() )
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%% Some debug code that outputs the HTML to a file %%
        #htmlFile = open("_output.html", "w+")
        #htmlFile.write(htmlDocument)
        #htmlFile.close()
        #%%                                                 %%
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        self.notePreview.setHtml(htmlDocument,  QUrl("file://" + os.getcwd() + "/" + quarkExtra.config["start_html_template_file"]) )


    def openFileAction(self):
        """Open an existing file by getting its path from a dialog."""

        self.saveFileAction()   #save the current note

        p = quarkExtra.makeAbsoluteFromHome(quarkExtra.config["notes_dir"])     #get the search directory
        searchPath = os.path.abspath(p)                                         #
        filePath = QFileDialog.getOpenFileName(self, "Open File", searchPath)   #prompt the user for the file path (note: 'filePath' is a tuple)
        if filePath[0] != "":                                                   #if the user did not hit the 'cancel' button
            self.noteEditor.openFileRequest(filePath[0])                        #open the file in the editor


    def saveFileAction(self):
        """Save text in editor to note."""

        if self.noteEditor.noteFilePath == "":  #if the file has not been saved yet and there is text to be saved, do a 'save as' instead
            if len( self.noteEditor.toPlainText() ) > 0:
                self.saveAsFileAction()
        else:                                   #else, just save the file
            self.noteEditor.saveFileRequest()
            self.scrollPreview()                    #scroll preview to edited line


    def saveAsFileAction(self):
        """Save text in editor to a new note and load it."""

        p = quarkExtra.makeAbsoluteFromHome(quarkExtra.config["notes_dir"])     #get the search directory
        searchPath = os.path.abspath(p)                                         #
        filePath = QFileDialog.getSaveFileName(self, "Save As File", searchPath)#prompt the use for the new file path
        if filePath[0] != "":                                                   #do not perform the save if the user pressed the 'cancel' button
            self.noteEditor.saveAsRequested(filePath[0])

        self.scrollPreview()                                                    #scroll preview to edited line
        self.noteManager.model().updateModel()                                          #update the note manager


    def saveCopyAsAction(self):
        """Save text in editor to a new note but do not load it."""

        p = quarkExtra.makeAbsoluteFromHome(quarkExtra.config["notes_dir"])
        searchPath = os.path.abspath(p)
        filePath = QFileDialog.getSaveFileName(self, "Save Copy As", searchPath)
        if filePath[0] != "":
            self.noteEditor.saveCopyAsRequested(filePath[0])

        self.scrollPreview()    #scroll preview to edited line
        self.noteManager.model().updateModel()


    def changeTitle(self, noteFilePath):
        """Change the window title based on the path to the open note.  Title is of the form: file_name.ext- Quark Note Taker"""

        titleTail = " - Quark Note Taker"   #store portion of window title that is common to all cases (goes at the end of title)
        if noteFilePath == "":              #if no file is specified (new note and file has not been saved  yet), set the file name to be 'Untitled'
            self.setWindowTitle("Untitled" + titleTail)
        else:                               #else, get the file name for the file path
            self.setWindowTitle(os.path.basename(noteFilePath) + titleTail)


    def newNoteAction(self):
        """Create a new note.  Automatically saves old note."""

        self.saveFileAction()   #save currently open note

        p = quarkExtra.makeAbsoluteFromHome(quarkExtra.config["notes_dir"])
        searchPath = os.path.abspath(p)
        filePath = QFileDialog.getSaveFileName(self, "New Note", searchPath)

        if filePath[0] != "":
            noteFile = open(filePath[0], "w+")  #create blank file
            noteFile.write("")                  #
            noteFile.close()                    #

            self.noteEditor.openFileRequest(filePath[0])    #open newly created file

        self.noteManager.model().updateModel()


    def newNotebookAction(self):
        """Create a new notebook."""

        notebookName, ok = QInputDialog.getText(self, "Create New Notebook - Quark Note Taker", "Notebook name: ", QLineEdit.Normal, "New Notebook");

        if ok and notebookName is not None and len(notebookName) > 0:
            p = quarkExtra.makeAbsoluteFromHome(quarkExtra.config["notes_dir"])
            rootPath = os.path.abspath(p)
            os.makedirs( os.path.join(rootPath, notebookName) )

        self.noteManager.model().updateModel()


    def linkClickHandler(self, url):
        """Handles links clicked (in note preview) which do not point to local files."""

        QDesktopServices.openUrl( url );


    def changePreviewScrollOnEditorScroll(self, scrollPosition):
        """Scrolles note preview when editor is scrolled ('scrollPosition' is not used)."""

        self.scrollPreview()


    def changePreviewScrollOnLoadFinished(self, ok):
        """Scrolles note preview when page is reloaded ('ok' is not used)."""

        self.scrollPreview()


    def scrollPreview(self):
        """Scrolles note preview to same 'height' as editor."""

        editorVal = self.noteEditor.verticalScrollBar().value()     #get the scroll height of the editor window
        if editorVal == 0:                                          #if it is '0' then just seth the height of the preview window to '0' also (can prevent division by zero error)
            viewVal = 0
        else:                                                       #otherwise calculate the corresponding scroll height for the preview window
            editorMax = self.noteEditor.verticalScrollBar().maximum()
            editorMin = self.noteEditor.verticalScrollBar().minimum()
            viewMax = self.notePreview.page().mainFrame().scrollBarMaximum(Qt.Vertical)
            viewMin = self.notePreview.page().mainFrame().scrollBarMinimum(Qt.Vertical)
            viewVal = editorVal/(editorMax - editorMin)*(viewMax - viewMin)

        self.notePreview.page().mainFrame().setScrollBarValue(Qt.Vertical, viewVal) #set the calculated scroll height on the preview window


    def loadSession(self):
        """Load a session based on the saved session data."""

        #set the note viewing mode
        viewMode = self.action[ quarkExtra.session["default_view_mode"] ]
        viewMode.setChecked(True)
        self.changeLayoutModeOnAction(viewMode)

        #set the notes manager's visibility
        if quarkExtra.session["display_note_manager"] == "true":
            self.action["Note Manager"].setChecked(True)
            self.noteManager.setVisible(True)
        elif quarkExtra.session["display_note_manager"] == "false":
            self.action["Note Manager"].setChecked(False)
            self.noteManager.setVisible(False)

        #set the display direction
        if quarkExtra.session["note_display_direction"] == "vertical":
            self.action["View Editor/Preview Vertically"].setChecked(True)
            self.changeNoteDirectionOnAction(True)
        elif quarkExtra.session["note_display_direction"] == "horizontal":
            self.action["View Editor/Preview Vertically"].setChecked(False)
            self.changeNoteDirectionOnAction(False)

        #open note for editing
        noteFilePath = quarkExtra.session["opened_note"]
        if os.path.exists(noteFilePath) and os.path.isfile(noteFilePath) :
            self.noteEditor.openFileRequest(noteFilePath)


    def saveSession(self):
        """Saves the current session to the JSON file."""

        #save the visibility of the notes manager
        if self.action["Note Manager"].isChecked():
            quarkExtra.session["display_note_manager"] = "true"
        else:
            quarkExtra.session["display_note_manager"] = "false"

        #save direction of the note displau
        if self.action["View Editor/Preview Vertically"].isChecked():
            quarkExtra.session["note_display_direction"] = "vertical"
        else:
            quarkExtra.session["note_display_direction"] = "horizontal"

        #save the note viewing mode
        for key, value in self.action.items():
            if value == self.actionGroup["display mode"].checkedAction():
                quarkExtra.session["default_view_mode"] = key

        #save the path of the currently open note
        quarkExtra.session["opened_note"] = self.noteEditor.getNotePath()

        #write session to the JSON file
        quarkExtra.saveCurrentSession()


    def openNoteFromManager(self, itemIndex):
        """If the item passed is a note, the note is opened for edit.  Otherwise, nothin is done."""

        self.saveFileAction()   #save the current note

        if itemIndex.isValid() and type(itemIndex.internalPointer()) is QuarkNoteModel: #if the item index is valid and points to note
            note = itemIndex.internalPointer()                                              #get the note
            notePath = note.getFilePath()                                                   #get path to the note file
            self.noteEditor.openFileRequest(notePath)                                       #open the note file


    def displayAboutQuark(self):
        """Display 'About - Quark Note Taker' message box."""

        QMessageBox.about(self, "About - Quark Note Taker",
        """<p>Quark Note Taker is an opensource, cross platform note taking application, written in python.
Notes are stored as plain-text/markdown files. Quark is highly customizable
as all files (including config files) are editable by the user.  It uses the
<a href="http://www.riverbankcomputing.com/software/pyqt/intro">PyQt</a> framework to display
the user interface.  It also uses <a href="https://github.com/waylan/Python-Markdown">Python Markdown</a>
to create a live preview of the note with support for <a href="http://www.mathjax.org/">MathJax</a> syntax.</p>

<p><a href="https://github.com/Leonardo2718/Quark_Note_Taker">View GitHub page &rarr;</a></p>

<p>Copyright &copy; 2014 Leonardo Banderali</p>

<p>Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:</p>

<p>The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.</p>

<p>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.</p>""")


    def openGithubPage(self):
        """Open Quark GitHub page in the users default browser."""

        QDesktopServices.openUrl( QUrl("https://github.com/Leonardo2718/Quark_Note_Taker") );


    def displayAboutQt(self):
        """Display 'About Qt - Quark Note Taker' message box."""

        QMessageBox.aboutQt(self, "About Qt - Quark Note Taker")


    def renameNoteAction(self):
        """Open input dialog to rename the current note."""

        currentName = self.noteEditor.getNoteFileName()
        newName, ok = QInputDialog.getText(self, "Rename This Note - Quark Note Taker", "New note name: ", QLineEdit.Normal, currentName);

        if ok and newName is not None and len(newName) > 0:
            currentNotePath = self.noteEditor.getNotePath()
            noteDirPath = os.path.dirname(currentNotePath)
            newNotePath = os.path.join(noteDirPath, newName)
            os.rename(currentNotePath, newNotePath)

        self.noteManager.model().updateModel()
        self.noteEditor.openFileRequest(newNotePath)    #load the renamed file in the editor


    def renameItemInManager(self):
        """Open input dialog to rename a note selected from the note manager."""

        modelIndex = self.noteManager.selectedIndexes()[0]  #get the model index of the selected item
        item = modelIndex.internalPointer()                 #get the item
        currentName = item.getName()
        newName = ""
        ok = False
        if type(item) is QuarkNoteModel:
            newName, ok = QInputDialog.getText(self, "Rename Note - Quark Note Taker", "New note name: ", QLineEdit.Normal, currentName);
        elif type(item) is QuarkNotebookModel:
            newName, ok = QInputDialog.getText(self, "Rename Notebook - Quark Note Taker", "New notebook name: ", QLineEdit.Normal, currentName);


        if ok and newName is not None and len(newName) > 0:
            currentNotePath = item.getFilePath()
            noteDirPath = os.path.dirname(currentNotePath)
            newNotePath = os.path.join(noteDirPath, newName)
            os.rename(currentNotePath, newNotePath)

        self.noteManager.model().updateModel()
        self.noteEditor.openFileRequest(newNotePath)    #load the renamed file in the editor


    def showManagerItemMenu(self, position):
        """Show the right-click menu for an item in the note manager.  'position' is a QPoint which
defines the position of the item."""

        itemModelIndex = self.noteManager.indexAt(position)         #get the model index of the selected item
        if itemModelIndex == self.noteManager.selectedIndexes()[0]: #only process the request if the item was right-clicked (i.e. it is selected)
                                                                    #   note that only a single item may be selected at a time
            item = itemModelIndex.internalPointer()
            tempMenu = QMenu(self.noteManager)
            actionSet = []

            if type(item) is QuarkNoteModel:
                actionSet = self.managerNoteAction
            elif type(item) is QuarkNotebookModel:
                actionSet = self.managerNotebookAction

            for label, a in actionSet.items():
                tempMenu.addAction(a)

            p = self.noteManager.viewport().mapToGlobal(position)   #get the position of the menu
            tempMenu.move(p)                                        #set the menu to its position
            tempMenu.show()                                         #show the menu


    def openSelectedNote(self):
        """Open the note which is selected in the note manager."""

        indexes = self.noteManager.selectedIndexes()#get the indexes of all the selected notes (note that only one can actually be selected)
        self.openNoteFromManager(indexes[0])        #open the only note that is actually selected


    def removeItemInManager(self):
        """Remove an item (note or notebook) in the note manager."""

        modelIndex = self.noteManager.selectedIndexes()[0]  #get the model index of the selected item
        item = modelIndex.internalPointer()                 #get the item
        itemFilePath = item.getFilePath()                   #get the path to the item
        message = "You are about to remove:\n{0}\n\nAre you sure?".format(itemFilePath)
        buttonSelected = QMessageBox.warning(self, "Removing an Item - Quark Note Taker", message, QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
        if buttonSelected == QMessageBox.Ok:
            if type(item) is QuarkNoteModel:
                os.remove(itemFilePath)
            elif type(item) is QuarkNotebookModel:
                shutil.rmtree(itemFilePath)

        self.noteManager.model().updateModel()
