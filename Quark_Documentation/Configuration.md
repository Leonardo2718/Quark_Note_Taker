#Configuring Quark Note Taker

Quark can be configured by simply editing some plain text files.  Any
changes to config files will not take effect until Quark is restarted.


##General Configuration

The most basic configurations can be done by editing the file `config.json`.
This simple [JSON](http://json.org/) file contains some key-value pairs that define
the properties and behavior of Quark.  Here is a list of all supported properties:

* `"autosave_every"`: 
    - type: string
    - description: defines the time interval between auto-saves in seconds (how long to
wait before the next auto-save)
    - default value: `"300000"` (300000 seconds = 5 minutes)
* `"end_html_template_file"`  
    - type: string
    - description: defines which file to use as "tail" for the Markdown to HTML conversion
    - default value: `"html-template/htmlDoc_end.html"`
* `"notes_dir"`:
    - type: string
    - description: defines the path to your Quark notes directory.
    - default value: `"~/QuarkNotes"` (where "~" is your home directory)
* `"start_html_template_file"`:
    - type: string
    - description: defines which file to use as "head" for the Markdown
to HTML conversion
    - default value: `"html-template/htmlDoc_start.html"`
* `"theme_file"`:
    - type: string
    - description: defines the path to a [CSS](http://www.w3.org/Style/CSS/) styling
file which is used to style the Quark user interface (not the note preview)
    - default value: `"themes/default.css"`

You can change the value of any of these properties to customize Quark.  If you change
the value of a property that holds a file or directory path,
*make sure the path actually exists*!


##Quark Themes

The file `themes/default.css` is a CSS file which defines the look of the user
interface.  When quark starts up, the contents of the file are loaded and used to style
the Qt app.  You have two options if you want to change how Quark looks.  First, you
can just edit this file.  Or, second, you can create your own CSS file and change the
`"theme_file"` property in `config.json` (see section above).

For instructions on how to write CSS for Qt, see the
[Qt documentation](http://qt-project.org/doc/qt-5/stylesheet.html) pages.


#Quark Note Preview/Export Template

The files `html-template/htmlDoc_start.html` and `html-template/htmlDoc_end.html`
contain some [HTML](http://www.w3.org/html/) that's used to convert a Markdown note
to HTML.  A complete HTML document is constructed from the different files as follows:

    contents of html-template/htmlDoc_start.html + 
    HTML generated from a Markdown note + 
    contents of html-template/htmlDoc_start.html

This document is used to generate the note previews as well as for exporting notes to
HTML.  You should therefore *only* edit these files if you want to change the way
notes are converted to HTML.  Here are some *suggested* guidelines for structuring the files:

* `html-template/htmlDoc_start.html` should *only contain the "head"* of the complete HTML
document.  It should contain the HTML `head` element, which further contains
the document's CSS and Javascript as well as any other relevant HTML elements.
Because the HTML note (generated from Markdown) is appended to this
file's content, the file should be ended with the `<body>` opening tag.

* `html-template/htmlDoc_end.html` should *only contain the "tail"* of the complete HTML
document.  It should always begin with the `</body>` closing tag.  Unless you
explicitly want to add some extra elements to *all your HTML notes*, the only other
elements in this file should be the closing tags corresponding to the ones opened in
`html-template/htmlDoc_start.html`.