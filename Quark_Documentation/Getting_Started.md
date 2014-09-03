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
manager.  I recommended you keep this directory **for Quark notes only**.  If you need
to add files which are stored in a different directory, you should create a link to
those files inside you notes directory.  Once the directory has been created, Quark will
copy this program's main `README.md` file to it.  
*(Note: In the event that you do not specify a notes directory,*
*Quark will default to use the source code's directory as your notes directory.)*
5. Once you've created your notes directory, Quark will start and automatically open the
`README.md` file. If this does not happen, you can manualy open any file you want by using
`File->Open` of typing `Ctrl+O` on your keyboard.

##Using Quark
When you open Quark for the first time, by default, you are presented with a window
divided into three sections:

1. the Quark notes manager (leftmost section)
2. the note editor (middle section)
3. the note preview (rightmost section)

You can change which sections are displayed using the `View` menu. 

###Menus

The `View > Note Manager` option (or the `Ctrl+M` shortcut) controls the display of
the notes manager.  It can be useful to hide the notes manager so you have more space
to view and edit your note.

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

You can export your Markdown note to an HTML file by using `File->Export to HTML`.  When
you click on this option, Quark will prompt you for the name and location of the file to
which you want to export your note.  The exported HTML will be the same as the HTML used
to display the note preview.

###The Notes Manager

The notes manager is intended to provide a simple interface for managing notes and
notebooks within Quark.  It can be easily displayed or hidden using the `Ctrl+M`
short cut.

The manager reflects the state of your notes directory in a tree-structure display.
All (non-hidden) files in your notes directory are shown as notes, and all sub-directory
are notebooks.  Sub-directories inside notebooks are ignored as it does not make sense
to have notebooks within notebooks.  Note that notebooks are (arbitrarily)
always displayed after notes.

Double clicking on a note will open the note in *both* the editor and preview.  
Right-clicking on a note or notebook will show an action menu for the particular
item.  Some of the actions shown include the ability to renaming and removing a
note or notebook.

###The Editor

The note editor in Quark is just a simple plain text editor with some basic syntax
highlighting for Markdown.  Notes can be edited as they would be in any other plain
text editor.

By default, Quark will automatically save your note every five minutes.  This time 
interval can be changed in the config file.  Quark will also autos-ave your note when
you create a new note, open another existing note, or close the main window and exit
Quark.  This ensures that you do not lose any work.

###The Preview

The note preview shows you the HTML version of your note live as you are editing.
Scrolling the editor will auto-scroll the preview.  However, scrolling the preview
*will not* auto-scroll the editor.  There is currently a bug where every time you
type a change into the editor, the preview will scroll back to the top.  At the
moment, there is no way around this.  However, the preview will automatically
scroll to the line you are editing whenever you save your note (even when it's an
auto-save).  Keep in mind that you do not need to display both the editor and the
preview.  You can select to only view one of the two by changing the display mode
using the `View` menu.
*(Note: I generally prefer to view the two separately so there is more room on my screen)*

The preview is generated by converting the note's markdown to HTML (using
[Markdown](https://pypi.python.org/pypi/Markdown) for python) and inserting the
output into a template.  Two HTML files are used to define the template:

1. `html-template/htmlDoc_start.html`: contains the head portion of the HTML
2. `html-template/htmlDoc_end.html`: contains the end portion of the HTML

Once the note is converted to HTML, the output is inserted between the contents of
the two files.  The result is then displayed in the preview section.

If you wish to change how notes are displayed in the preview, you can do so by
modifying the two template files (mentioned above).  The main file you will want to
edit is  `html-template/htmlDoc_start.html` because it contains all the CSS and
Javascript used in the HTML preview. The `html-template/htmlDoc_end.html` file only
contains some closing tags necessary for valid HTML.  You could edit this
file to create a footer for your preview.  Keep in mind, however, that any changes to
these files will only affect how the note is *previewed* and *not* the note itself.
So if you add any special features (such as a footer) they will not be displayed if
you choose to open your note in a different editor (unless you export your note to an
HTML file).

To enable/disable synchronized scrolling, you check/uncheck the menu item
`View > Synchronized Scrolling`.