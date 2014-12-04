#Quark Note Taker
Quark Note Taker is an opensource, cross platform, Markdown based note taking application written in Python.
All notes are stored as plain-text/markdown files. Quark is highly customizable as all files are editable
by the user.  It uses the [PyQt](http://www.riverbankcomputing.com/software/pyqt/intro)
framework for the user interface and [Python Markdown](https://github.com/waylan/Python-Markdown)
to create a live preview of the note with support for [MathJax](http://www.mathjax.org/).

##Current features
* basic markdown syntax highlighting
* basic note management
* session saving and loading
* auto-saving
* markdown live preview
* [MathJax](http://www.mathjax.org/) syntax support
* synchronized scrolling

##Dependencies
Make sure you have these installed as **Quark needs them** in order to work:

* [Python 3.x.x](https://docs.python.org/3/)
* [PyQt5](http://pyqt.sourceforge.net/Docs/PyQt5/index.html)
* [Python Markdown](https://github.com/waylan/Python-Markdown)

##Quick start guide
1. Make sure you have all dependencies installed and that they all work correctly
2. Start Quark by running the file `quark.py`
3. Quark will prompt you to create a new notes directory.  By default, it will create
it as `[HOME_DIRECTORY]/QuarkNotes/`.  Once the notes directory is created, Quark
will make a cope of this file to your new directory. 
4. When Quark starts, if `README.md` is not opened by default, use `File->Open` (or
type `Ctrl+O`) to open the file/note
5. If the file opens and is displayed correctly, then Quark is working!
6. Optional: customize Quark to your liking by modifying any of the following files
	- `config.json`
	- `themes/default.css`
	- `html-template/htmlDoc_start.html`
	- `html-template/htmlDoc_end.html`
	- all source files (Quark is released under the MIT license)


##Known issues
1. There is a problem highlighting the syntax of nested emphasis when the same symbols
are used such as `_emphasized __and__ strong_` so use `_emphasized **and** strong_` 
instead if care about correct syntax highlighting.

##License
Quark Note Taker is licensed under the MIT License.

All documentation that goes with Quark Note Taker is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a>
