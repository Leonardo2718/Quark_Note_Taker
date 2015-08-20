#Getting Started with Quark Note Taker

##Installation
1. Install the latest versions of **all** Quark dependencies:
    - [Python 3](https://www.python.org/downloads/)
    - [PyQt5](http://www.riverbankcomputing.com/software/pyqt/download5)
    - [Markdown](https://pypi.python.org/pypi/Markdown)
	- [Pygments](http://pygments.org/)
    - *Note: make sure that all python modules are installed correctly and that they are working*
2. Download Quark, this can be done in three different ways:
    1. download and extract the [zip file](https://github.com/Leonardo2718/Quark_Note_Taker/archive/master.zip), or
    2. download from the [GitHub page](https://github.com/Leonardo2718/Quark_Note_Taker) or
    3. clone the repository: `git clone https://github.com/Leonardo2718/Quark_Note_Taker.git`
3. Set where your notes directory is going to be.  This is were Quark's notes manager is going
to store and look for your notes.  If your ok with using the default (`~/QuarkNotes`), you can
skip this step. Otherwise:
	1. open the file `settings.py`
	2. look for the property named `notes_dir`
	3. set its value to whatever you want
	4. (see the `Configuration.md` file for more details) 
	5. Note: if you run Quark and it's unable to find the notes directory you specified, it will
ask you if it should create it for you. If you choose *No*, Quark will refuse to run (in which
case you should create the directory yourself or specify a different directory in `settings.py`).
If you choose *Yes*, Quark will create the directory and ask you if it should put a copy of the
main `README.md` and documentation files in it.
4. Run Quark by running the file named `quark.py`
    - *Note: on Windows, you may need to change the file extension from `.py` to `.pyw`*
5. Write, veiw, and edit notes!

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

1. View Mode: only display the HTML/preview version of the note without the editor (use `Ctrl+R`)
2. Edit Mode: only display the note editor without the preview (use `Ctrl+E`)
3. View & Edit Mode: display both the note editor and preview side-by-side (use `Ctrl+Shift+E`)

You can use the `View > View Editor/Preview Vertically` option to control the layout of
the note editor and preview.  If this option is not checked, the note preview will
be displayed **to the right** of the editor.  If this option is checked, then the note
preview will be displayed **below** the the editor.  Note that this option has no effect
on the notes manager.

Using the `File` menu you can do things such as saving, opening, renaming, and creating
new notes as well as notebooks.

You can export your Markdown note to an HTML file by using `File > Export to HTML`.  When
you click on this option, Quark will prompt you for the name and location of the file in
which you want to export your note.  The exported HTML will be the same as the HTML used
to display the note preview.

###The Notes Manager

The notes manager is intended to provide a simple interface for managing notes and
notebooks within Quark.  It can be easily displayed or hidden using the `Ctrl+M`
short cut.

The manager reflects the state of your notes directory in a tree-structure display.
All (non-hidden) files in your notes directory are shown as notes, and all sub-directory
are notebooks.  Sub-directories inside notebooks are ignored because it doesn't make 
sense to have notebooks within notebooks.  Note that notebooks are (arbitrarily)
always displayed after notes.

Double clicking on a note will open the note in *both* the editor and preview.  
Right-clicking on a note or notebook will show an action menu for the particular
item.  Some of the actions shown include the ability to rename or remove the item.

###The Editor

The note editor in Quark is just a simple plain text editor with some basic syntax
highlighting for Markdown.  Notes can be edited as they would be in any other plain
text editor.

By default, Quark will automatically save your note every five minutes.  This time 
interval can be changed in the config file.  Quark will also autos-ave your note when
you create a new note, open another existing note, or close the main window and exit
Quark.  This ensures that you do not lose any work.

###The Preview

The note preview shows you the HTML version of your note as you are editing. To
enable/disable synchronized scrolling, check/uncheck the menu item
`View > Synchronized Scrolling`. The way this feature is currently implemented,
scrolling the editor will automatically scroll the preview, but scrolling the 
preview **will not** scroll the editor.  

The preview is generated by converting the note's markdown to HTML (using
[Markdown](https://pypi.python.org/pypi/Markdown) for python) and inserting the
output into a template.  Two HTML files are used to define the template:

1. `html-template/htmlDoc_start.html`: contains the head portion of the HTML
2. `html-template/htmlDoc_end.html`: contains the end portion of the HTML

Once the note is converted to HTML, the output is inserted between the contents of
the two files.  The result is then displayed in the preview section.

If you wish to change how notes are displayed in the preview, you can do so by
modifying the two template files.  The main file you will want to
edit is  `html-template/htmlDoc_start.html` because it contains all the CSS and
Javascript used in the HTML preview. The `html-template/htmlDoc_end.html` file only
contains some closing tags necessary for valid HTML.  You could edit this
file to create a footer for your preview.  Keep in mind, however, that any changes to
these files will only affect how the note is *previewed* and *not* the note itself.
So if you add any special features (such as a footer) they will not be displayed if
you choose to open your note in a different editor (unless you export your note to an
HTML file).