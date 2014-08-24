#Configuring Quark Note Taker

Quark can be configured by simply editing some files plain text files.  Note that any
changes to any config files will not take effect untill quark is restarted.


##General Configuration

The most basic configurations can be set by editing the `config.json` file.
This simple [JSON](http://json.org/) file containes some key-value pairs which define
the properties and behaviour of Quark.  The following is a list of the supported
properties:

* `"autosave_every"`: 
    - type: string
    - description: defines the time interval between autosaves in seconds (how long to
wait before the next autosave)
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

You can change the value of any of these properties to custumize Quark.  If you change
the value of any property which defines a file or directory path,
*make sure the path actually exists*!


##Quark Themes

The file `themes/default.css` is a CSS file which defines the look of the user
interface.  When quark starts up, the contents of the file are loaded and used to style
the Qt app.  You have two options if you want to change how Quark looks.  First, you
can simple edit this file.  Or, second, you can create your own CSS file and change the
`"theme_file"` property in `config.json` (see section above).

For instructions on how to write CSS for Qt, see the
[Qt documentation](http://qt-project.org/doc/qt-5/stylesheet.html) pages.


#Quark Note Preview/Export Template

The files `html-template/htmlDoc_start.html` and `html-template/htmlDoc_end.html`
contain some [HTML](http://www.w3.org/html/) which is used to convert a Markdown note
to HTML.  The final HTML document is structured as follows:

    contents of html-template/htmlDoc_start.html + 
    HTML generated from a Markdown note + 
    contents of html-template/htmlDoc_start.html

This document is used to generate the note previews as well as for exporting notes to
HTML.  You should therefore *only* edit these files if you want to change the way
notes are converted to HTML.  The only thing you should keep in mind when doing these
edits is the structure of the final document as explained in the "code" snippet
above.  Here are some *suggested* guidelines for structuring the files:

* `html-template/htmlDoc_start.html` should contain the "head" of the final HTML
document.  This file should contain the HTML `head` element, which further contains
the document's CSS and Javascript as well as any other relavent HTML elements.
Because an HTML note (generated from Markdown) will be appended to this
file's content, you should end the file with the `<body>` openning tag.

* `html-template/htmlDoc_end.html` should contain the "tail" of the final HTML
document.  This file should begin with the `</body>` closing tag.  Unless you
*explicitely* want to add some extra elements to your HTML notes, the only other
items present in this file should be the closing tags for tags that are opened in the 
`html-template/htmlDoc_start.html` file.