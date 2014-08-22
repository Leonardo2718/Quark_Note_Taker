#Getting Started with Quark Note Taker

##Installation
1. Install **all** of Quark's dependencies:
    - The latest version of [Python 3](https://www.python.org/downloads/)
    - The latest version of [PyQt5](http://www.riverbankcomputing.com/software/pyqt/download5)
    - The latest version of the Python module for [Markdown](https://pypi.python.org/pypi/Markdown)
    - *Note: make sure the python modules are installed correctly and that they are working*
2. Download Quark:
    - download and extract the [zip file](https://github.com/Leonardo2718/Quark_Note_Taker/archive/master.zip), or
    - download from the [GitHub page](https://github.com/Leonardo2718/Quark_Note_Taker) or
    - clone the repository: `git clone https://github.com/Leonardo2718/Quark_Note_Taker.git`
3. To run Quark, simply run the file named `quark.py`
    - *Note: on Windows, you may need to change the extension from `.py` to `.pyw`*
4. When you first run Quark, you will be prompted to create a new directory to store all your
Quark notes.  Files which are stored in this directory will be shown in the Quark notes
manager.  It is recommended that you keep this directory **for Quark notes only**.  If you
need to add files which are stored in a different directory, you should create a link to
those files inside you notes directory.
5. Once you've created the notes directory, you can start start using Quark normally.

##Using Quark
When you open Quark, by default, you are presented with a window divided into three
sections:

1. the Quark notes manager (leftmost section)
2. the note editor (middle section)
3. the note preview (rightmost section)

You can change which sections are displayed using the `View` menu. 

###Menus

The `View > Note Manager` option (or the `Ctrl+M` shortcut) controls the display of
the notes manager.  It can be useful to hide the notes manager so you have more space
to view and edit you note.

You can also control the "display mode", which controls how the note editor and preview
are displayed.  There are three possible display modes:

1. View Mode: only display the HTML/preview version of the note without the editor
2. Edit Mode: only display the note editor without the preview
(useful for distraction free editing)
3. View & Edit Mode: display both the note editor and preview side-by-side

You can use the `View > View Editor/Preview Vertically` option to control the layout of
the note editor and preview.  If this option is not checked, then the note preview will
be displayed *to the right* of the editor.  If this option is checked, then the note
preview will be displayed *below* the the editor.  Note that this option has no effect
on the notes manager.

Using the `File` menu you can do things such as saving, opening, renaming, and creating
new notes as well as notebooks.

###The Notes Manager

The notes manager is intended to provide a simple interface for managing notes and
notebooks within Quark.  It can be easily displayed or hidden using the `Ctrl+M`
short cut.

Any file in your notes directory is considered a note.  Any sub-directory to your notes
directory is considered a notebook.  Sub-directories inside notebooks are ignored as
it does not make sense to have notebooks within notebooks.  Notes and notebooks are
displayed in a tree structure where notebooks can be collapsed in order to hide the
contained notes.  Notebooks are (arbitrarily) always displayed after notes.

Double clicking on a note will open the note in the editor and preview.  Right clicking
on a note or notebook will provide some basic actions which can be performed.  These
actions include renaming and removing notes and notebooks.

###The Editor

The note editor in Quark is just simple plain text editor with some basic syntax
highlighting for Markdown.  Notes can be edited as they would be in any other plain
text editor.

By default, Quark will automatically save your note every five minutes.  This time 
interval can be changed in the config file.  Quark will also autos-ave your note when
you create a new note, open another existing note, or close the main window and exit
Quark.  This ensures that you do not lose any work.

###The Preview

The note preview shows you the HTML version of your note live as you are editing.
Scrolling the editor will auto-scroll the preview.  However, scrolling the preview
will *not* auto-scroll the editor.  There is currently a bug where every time you
type a change into the editor, the preview will scroll back to the top.  There
is no way around this (at this point).  However, the preview will automatically
scroll to the line you are editing whenever you save your note (even when it's an
auto-save).

Keep in mind that you do not need to display both the editor and the preview.  You
can select to only view one of the two by changing the display mode using the `View`
menu.
*(Note: I generally prefer to view the two separately so there is more room on my screen)*

The preview is generated by converting converting the note markdown to HTML (using
[Markdown](https://pypi.python.org/pypi/Markdown) for python) and inserting it into
an HTML template.  The two template files are:

- `html-template/htmlDoc_start.html` which contains the head of the final HTML document
- `html-template/htmlDoc_end.html` which contains the end/close of the final
HTML document

Quark generates the final HTML preview document by inserting the note's HTML form
between the contents of the two files.  The result is then displayed in the preview
section.

You can change the default template (or even create you own) by modifying the contents
of these two files.  The main file you will want to edit is `html-template/htmlDoc_start.html`
as this file contains all the CSS ahd Javascript used to display the HTML preview. The
`html-template/htmlDoc_end.html` file only contains some necessary closing tags to
make valid HTML.  However you could use this file to display a footer in all your notes.

If you do change any of these files, keep in mind that they will only affect how the 
note is *previewed* and not the note itself.  So if you add any special features (such
as a footer) they will not be displayed if you choose to open your note in a different
editor.