#Quark Note Taker
Quark Note Taker is an opensource, cross platform note taking application, written in python.
Notes are stored as plain-text/markdown files. Quark is highly customizable
as all files (including config files) are editable by the user.  It uses the
[PyQt](http://www.riverbankcomputing.com/software/pyqt/intro) framework to display
the user interface.  It also uses [Python Markdown](https://github.com/waylan/Python-Markdown)
to create a live preview of the note with support for [MathJax](http://www.mathjax.org/) syntax.

##Current features
* basic markdown syntax highlighting
* markdown live preview
* [MathJax](http://www.mathjax.org/) syntax support
* synchronized scrolling (sort of; see 'Known issues' section)

##Planed features
* auto-indenting
* note management
* auto-save
* session saving and loading
* more customization capabilities
* template support
* macro support

##Dependencies
Make sure you have these installed as **Quark needs them** in order to work:

* [Python 3.x.x](https://docs.python.org/3/)
* [PyQt5](http://pyqt.sourceforge.net/Docs/PyQt5/index.html)
* [Python Markdown](https://github.com/waylan/Python-Markdown)

##Quick start guide
1. Make sure you have all dependencies installed and that they all work correctly
2. Start Quark by running the file `quark.py`
3. Navigate to `File->Open` or type `Ctrl+O` to bring up the open file dialog
4. Open the file `README.md` (this file!)
5. If it opens and displays correctly, then Quark is working!
6. Optional: customize quark to your liking by modifying any of the following files
    - `config.json`
    - `themes/default.css`
    - `html-template/htmlDoc_start.html`
    - `html-template/htmlDoc_end.html`

##Known issues
1. When editing a note, every time a change is made, the live preview jumps to the
top of the document.  Scrolling the editor window will restore the preview to the
correct position.  You can also save the note (`Ctrl+S`)  to restore the preview.

##License
Quark Note Taker is licensed under the MIT License.

All documentation that goes with Quark Note Taker is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a>
