#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Project: Quark Note Taker
File: mainwindow.py
Author: Leonardo Banderali
Created: August 3, 2014
Last Modified: December 21, 2015

Description:
    This file contains the class wich defines the main application window for Quark.


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
import sys
import os
import shutil

#extra modules
import misaka

#Qt objects
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebKit import *
from PyQt5.QtWebKitWidgets import *

#Quark specific
import quarkExtra
import settings as quarkSettings
from quarkrenderer import QuarkRenderer
from noteeditor import NoteEditor
from quarknotemanagermodel import QuarkNoteManagerModel
from quarknotemodel import QuarkNoteModel
from quarknotebookmodel import QuarkNotebookModel



#~main window setup~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MainWindow(QMainWindow):
    """The main window class contains all the components of the app"""

    def __init__(self):
        super(MainWindow, self).__init__()

        #initialize private variables

        self._syncScroll = False    #variable to hold the state of synchronized scrolling (not synchronized)

        # create markdown parser
        renderer = QuarkRenderer()
        self.htmlRenderer = misaka.Markdown(renderer, extensions=misaka.EXT_FENCED_CODE | misaka.EXT_MATH | misaka.EXT_MATH_EXPLICIT | misaka.EXT_TABLES)

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
        self.action["Export to HTML"] = self.menu["File"].addAction("&Export to HTML")

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
        self.action["Synchronized Scrolling"] = self.menu["View"].addAction("&Synchronized Scrolling")
        self.menu["View"].addSeparator()
        self.action["Note Manager"] = self.menu["View"].addAction("&Note Manager")
        self.menu["View"].addSeparator()
        self.actionGroup["wrap mode"] = QActionGroup(self)
        self.action["No Wrap"] = self.actionGroup["wrap mode"].addAction("N&o Wrap")
        self.menu["View"].addAction( self.action["No Wrap"] )
        self.action["Word Wrap"] = self.actionGroup["wrap mode"].addAction("&Word Wrap")
        self.menu["View"].addAction( self.action["Word Wrap"] )
        self.action["Line Wrap"] = self.actionGroup["wrap mode"].addAction("&Line Wrap")
        self.menu["View"].addAction( self.action["Line Wrap"] )

        #create shorcuts for actions in 'View' menu
        self.action["Note Manager"].setShortcut( QKeySequence("Ctrl+M") )
        self.action["View Mode"].setShortcut( QKeySequence("Ctrl+R") )
        self.action["Edit Mode"].setShortcut( QKeySequence("Ctrl+E") )
        self.action["View & Edit Mode"].setShortcut( QKeySequence("Ctrl+Shift+E") )

        #set check state for actions in 'View' menu
        self.action["View Mode"].setCheckable(True)
        self.action["Edit Mode"].setCheckable(True)
        self.action["View & Edit Mode"].setCheckable(True)
        self.action["View Editor/Preview Vertically"].setCheckable(True)
        self.action["Note Manager"].setCheckable(True)
        self.action["Synchronized Scrolling"].setCheckable(True)
        self.action["No Wrap"].setCheckable(True)
        self.action["Word Wrap"].setCheckable(True)
        self.action["Line Wrap"].setCheckable(True)

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
        self.managerNotebookAction["Add a Note"] = QAction("Add a Note", self.noteManager)

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
        self.menu["Dictionary"] = self.menuBar().addMenu(self.noteEditor.getDictionarySelector())

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
        self.action["Export to HTML"].triggered.connect(self.exportToHTMLAction)

        #connect signals in 'View' menu to slots
        self.action["Note Manager"].toggled.connect(self.noteManager.setVisible)
        self.actionGroup["display mode"].triggered.connect(self.changeLayoutModeOnAction)
        self.action["View Editor/Preview Vertically"].toggled.connect(self.changeNoteDirectionOnAction)
        self.action["Synchronized Scrolling"].toggled.connect(self.setSyncScroll)
        self.actionGroup["wrap mode"].triggered.connect(self.setWrapModeOnAction)

        #connect signals in 'Help' menu to slots
        self.action["About Quark Note Taker"].triggered.connect(self.displayAboutQuark)
        self.action["View GitHub Page"].triggered.connect(self.openGithubPage)
        self.action["About Qt"].triggered.connect(self.displayAboutQt)

        # setup timer that delays the editor view update when editing a note
        self.updateDelayTimer = QTimer(self)
        self.updateDelayTimer.setSingleShot(True)
        updateDelay = int(quarkSettings.update_delay)   # get the delay time (in milliseconds) from the config file
        self.updateDelayTimer.setInterval(updateDelay)
        self.updateDelayTimer.timeout.connect(self.updateSlot)

        #connect signals from the note editor to slots
        #self.noteEditor.textChanged.connect(self.updatePreview)
        #self.noteEditor.textChanged.connect(self.updateSlot)
        self.noteEditor.textChanged.connect(self.updateDelayTimer.start)
        self.noteEditor.noteFileChanged.connect(self.changeTitle)
        self.noteEditor.verticalScrollBar().valueChanged.connect(self.syncPreviewScroll)

        #connect signals from the note previewer to slots
        self.notePreview.page().linkClicked.connect(self.linkClickHandler)
        self.notePreview.page().mainFrame().contentsSizeChanged.connect(self.syncPreviewScroll)
            #this connection is made to prevent the previewer from scrolling to the top on every edit

        #connect signals from the note manager to slots
        self.noteManager.doubleClicked.connect(self.openNoteFromManager)
        self.noteManager.customContextMenuRequested.connect(self.showManagerItemMenu)
        self.managerNoteAction["Open Note"].triggered.connect(self.openSelectedNote)
        self.managerNoteAction["Rename Note"].triggered.connect(self.renameItemInManager)
        self.managerNoteAction["Remove Note"].triggered.connect(self.removeItemInManager)
        self.managerNotebookAction["Rename Notebook"].triggered.connect(self.renameItemInManager)
        self.managerNotebookAction["Remove Notebook"].triggered.connect(self.removeItemInManager)
        self.managerNotebookAction["Add a Note"].triggered.connect(self.addNoteToNotebook)

        #last minute configs
        self.changeTitle("")        #set default window title
        self.loadSession()

        #setup timer to trigger autosave
        self.autosaveTimer = QTimer(self)                           #create the timer
        self.autosaveTimer.timeout.connect(self.saveFileAction)     #connect the timer to the save method
        #autosave_interval = int(quarkExtra.config["autosave_every"])#get the time interval from the config file (in milliseconds)
        #self.autosaveTimer.start(autosave_interval)                 #set the interval and start the timer
        self.autosaveTimer.start(quarkSettings.autosave_interval)   #set the interval and start the timer


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
            self.updatePreview()

        elif action == self.action["Edit Mode"] :       #if the user choses to only display the note editor
            self.noteEditor.setVisible(True)
            self.notePreview.setVisible(False)

        elif action == self.action["View & Edit Mode"] :  #if the user choses to display both the note editor and note preview
            self.noteEditor.setVisible(True)
            self.notePreview.setVisible(True)
            self.updatePreview()


    def setWrapModeOnAction(self, action):
        """Changes the wrapping mode of the editor based on the 'view' menu action triggered."""

        if action == self.action["No Wrap"]:
            self.noteEditor.setWrapMode(QTextOption.NoWrap)

        elif action == self.action["Word Wrap"]:
            self.noteEditor.setWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)

        elif action == self.action["Line Wrap"]:
            self.noteEditor.setWrapMode(QTextOption.WrapAnywhere)


    def changeNoteDirectionOnAction(self, isVertical):
        """Changes direction (horizontal/vertical) of the note editor and previewer."""

        if not isVertical:
            self.noteArea.setOrientation(Qt.Horizontal)
        elif isVertical:
            self.noteArea.setOrientation(Qt.Vertical)


    def updatePreview(self):
        """Converts the Markdown note to HTML and loads it into the previewer."""

        htmlDocument = self.htmlRenderer( self.noteEditor.toPlainText() )
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%% Some debug code that outputs the HTML to a file %%
        #htmlFile = open("_output.html", "w+")
        #htmlFile.close()
        #self.exportToHTMLFile("_output.html")
        #%%                                                 %%
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        self.notePreview.setHtml(htmlDocument,  QUrl("file://" + os.getcwd() + "/" + quarkSettings.start_html_template_file) )


    def updateSlot(self):
        """Slot called to update the previewer when the text in the note editor changes."""

        if self.notePreview.isVisible() :
            self.updatePreview()


    def openFileAction(self):
        """Open an existing file by getting its path from a dialog."""

        self.saveFileAction()   #save the current note

        p = quarkExtra.makeAbsoluteFromHome(quarkSettings.notes_dir)     #get the search directory
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


    def saveAsFileAction(self):
        """Save text in editor to a new note and load it."""

        p = quarkExtra.makeAbsoluteFromHome(quarkSettings.notes_dir)     #get the search directory
        searchPath = os.path.abspath(p)                                         #
        filePath = QFileDialog.getSaveFileName(self, "Save As File", searchPath)#prompt the use for the new file path
        if filePath[0] != "":                                                   #do not perform the save if the user pressed the 'cancel' button
            self.noteEditor.saveAsRequested(filePath[0])

        self.noteManager.model().updateModel()                                          #update the note manager


    def saveCopyAsAction(self):
        """Save text in editor to a new note but do not load it."""

        p = quarkExtra.makeAbsoluteFromHome(quarkSettings.notes_dir)
        searchPath = os.path.abspath(p)
        filePath = QFileDialog.getSaveFileName(self, "Save Copy As", searchPath)
        if filePath[0] != "":
            self.noteEditor.saveCopyAsRequested(filePath[0])

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

        p = quarkExtra.makeAbsoluteFromHome(quarkSettings.notes_dir)
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

        notebookName, ok = QInputDialog.getText(self, "Create New Notebook - Quark Note Taker", "Notebook name: ", QLineEdit.Normal, "New Notebook")

        if ok and notebookName is not None and len(notebookName) > 0:
            p = quarkExtra.makeAbsoluteFromHome(quarkSettings.notes_dir)
            rootPath = os.path.abspath(p)
            os.makedirs( os.path.join(rootPath, notebookName) )

        self.noteManager.model().updateModel()


    def linkClickHandler(self, url):
        """Handles links clicked (in note preview) which do not point to local files."""

        QDesktopServices.openUrl( url )


    def syncPreviewScroll(self):
        """Scrolles note preview when editor is scrolled ('scrollPosition' is not used)."""

        if self._syncScroll == True:
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


    def syncEditScroll(self):
        """Scrolles note editor when previewer is scrolled ('scrollPosition' is not used)."""
        #This method is not currently used as I haven't found an appropriate signal to connect it to

        if self._syncScroll == True:
            viewVal = self.notePreview.page().mainFrame().scrollBarValue(Qt.Vertical)
            if viewVal == 0:
                editorVal = 0
            else:
                viewMax = self.notePreview.page().mainFrame().scrollBarMaximum(Qt.Vertical)
                viewMin = self.notePreview.page().mainFrame().scrollBarMinimum(Qt.Vertical)
                editorMax = self.noteEditor.verticalScrollBar().maximum()
                editorMin = self.noteEditor.verticalScrollBar().minimum()
                editorVal = viewVal/(viewMax - viewMin)*(editorMax - editorMin)

            self.noteEditor.verticalScrollBar().setValue(editorVal)


    def loadSession(self):
        """Load a session based on the saved session data."""

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

        #set the note viewing mode
        viewMode = self.action[ quarkExtra.session["default_view_mode"] ]
        viewMode.setChecked(True)
        self.changeLayoutModeOnAction(viewMode)

        #set wrap mode
        wrapMode = self.action[ quarkExtra.session["wrap_mode"] ]
        wrapMode.setChecked(True)
        self.setWrapModeOnAction(wrapMode)

        #set the notes manager's visibility
        if quarkExtra.session["display_note_manager"] == "true":
            self.action["Note Manager"].setChecked(True)
            self.noteManager.setVisible(True)
            self.updatePreview()
        elif quarkExtra.session["display_note_manager"] == "false":
            self.action["Note Manager"].setChecked(False)
            self.noteManager.setVisible(False)

        #set synchronized scrolling state
        if quarkExtra.session["synchronized_scrolling"] == "true":
            self.action["Synchronized Scrolling"].setChecked(True)
            self._syncScroll = True
        elif quarkExtra.session["synchronized_scrolling"] == "false":
            self.action["Synchronized Scrolling"].setChecked(False)
            self._syncScroll = False


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

        #save the path of the currently open note
        quarkExtra.session["opened_note"] = self.noteEditor.getNotePath()

        #save the note viewing mode
        for key, value in self.action.items():  # TODO: this loop should really be optimized
            if value == self.actionGroup["display mode"].checkedAction():
                quarkExtra.session["default_view_mode"] = key
            elif value == self.actionGroup["wrap mode"].checkedAction():
                quarkExtra.session["wrap_mode"] = key

        #save synchronized scrolling state
        if self.action["Synchronized Scrolling"].isChecked() and self._syncScroll == True :
            quarkExtra.session["synchronized_scrolling"] = "true"
        else:
            quarkExtra.session["synchronized_scrolling"] = "false"

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

<p>Copyright &copy; 2015 Leonardo Banderali</p>

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

        QDesktopServices.openUrl( QUrl("https://github.com/Leonardo2718/Quark_Note_Taker") )


    def displayAboutQt(self):
        """Display 'About Qt - Quark Note Taker' message box."""

        QMessageBox.aboutQt(self, "About Qt - Quark Note Taker")


    def renameNoteAction(self):
        """Open input dialog to rename the current note."""

        currentName = self.noteEditor.getNoteFileName()
        newName, ok = QInputDialog.getText(self, "Rename This Note - Quark Note Taker", "New note name: ", QLineEdit.Normal, currentName)

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
            newName, ok = QInputDialog.getText(self, "Rename Note - Quark Note Taker", "New note name: ", QLineEdit.Normal, currentName)
        elif type(item) is QuarkNotebookModel:
            newName, ok = QInputDialog.getText(self, "Rename Notebook - Quark Note Taker", "New notebook name: ", QLineEdit.Normal, currentName)

        if ok and newName is not None and len(newName) > 0:
            currentItemPath = item.getFilePath()
            itemDirPath = os.path.dirname(currentItemPath)
            newItemPath = os.path.join(itemDirPath, newName)
            os.rename(currentItemPath, newItemPath)

        self.noteManager.model().updateModel()
        if type(item) is QuarkNoteModel:
            self.noteEditor.openFileRequest(newItemPath)    #load the renamed file in the editor
        elif type(item) is QuarkNotebookModel:
            #prevent editing a file that no longer exists because it's directory was renamed
            currentNoteName = self.noteEditor.getNoteFileName()
            newCurrentNotePath = os.path.join(newItemPath,currentNoteName)  #if the open note is in the renamed directory, this would be its path
            if os.path.exists(newCurrentNotePath):
                self.noteEditor.openFileRequest(newCurrentNotePath)    #load the file in the renamed directory in the editor


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


    def addNoteToNotebook(self):
        """Add a note to the selected notebook."""

        modelIndex = self.noteManager.selectedIndexes()[0]  #get the model index of the selected item
        item = modelIndex.internalPointer()                 #get the item
        if type(item) is QuarkNotebookModel:                #check that the selected item actually is a notebook
            noteName, ok = QInputDialog.getText(self, "Add a Note - Quark Note Taker", "New note file name: ", QLineEdit.Normal) #get a file name for the new note
            if ok and noteName != "":                       #if the user entered a file name it's valid
                newNotePath = os.path.join(item.getFilePath(),noteName)     #get create a path for the note
                if not os.path.exists(newNotePath):                         #only if the new note does not already exists
                    newNote = open(newNotePath, "w+")                           #create the new note
                    newNote.close()                                             #
                    self.noteEditor.openFileRequest(newNotePath)                #open the newly created note
                    self.noteManager.model().updateModel()                      #reload the notes manager


    def exportToHTMLFile(self, filePath):
        """Exports the note to an HTML file.  The HTML will reflect what is displayed in the note preview."""

        if os.path.exists(filePath) and os.path.isfile(filePath):           #if the file path provided exists
            htmlDocument = self.htmlRenderer( self.noteEditor.toPlainText() )   #convert the note to HTML
            htmlFile = open(filePath, "w")                                      #open the provided file path
            htmlFile.write(htmlDocument)                                        #write the HTML content to the file
            htmlFile.close()                                                    #close the file after writing to it


    def exportToHTMLAction(self):
        """Action to export the note as an HTML file."""

        searchPath = os.path.expanduser("~")    #offer to export in the user's home directory
        filePath, fileType = QFileDialog.getSaveFileName(self, "Export to HTML", searchPath, "HTML (*.html *.htm)") #request the file name/path to export to

        if not filePath == "":                  #if the file path returned by the user is valid
            exportFile = open(filePath, "w+")       #create the file
            exportFile.close()                      #
            self.exportToHTMLFile(filePath)         #export HTML to the file
            self.noteManager.model().updateModel()  #update the notes manager in case the exported file was saved in the user's notes directory


    def setSyncScroll(self, state):
        """Toggles flag which controles the synchronized scrolling."""

        self._syncScroll = state
