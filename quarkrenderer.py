#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Project: Quark Note Taker
File: quarkrenderer.py
Author: Leonardo Banderali
Created: June 9, 2016
Last Modified: June 10, 2016

Description:
    This file contains the class used to render the markdown into HTML.


Copyright (C) 2016 Leonardo Banderali

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

import misaka
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_style_by_name

import settings as quarkSettings



#~renderer~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class QuarkRenderer(misaka.HtmlRenderer):
    """A Markdown to HTML renderer for Quark.

This renderer is intended to work with the Misaka module, a python binding for Hoedown."""

    def __init__(self):
        super(QuarkRenderer, self).__init__()

        # get the document header and footer
        htmlFile = open(quarkSettings.start_html_template_file , "r")   # get the head of the HTML template document
        self.docHeader = htmlFile.read()
        htmlFile.close()

        htmlFile = open(quarkSettings.end_html_template_file, "r")      # get the tail of the HTML template document
        self.docFooter = htmlFile.read()
        htmlFile.close()

        # create a formater
        self.formatter = HtmlFormatter(style="monokai", cssclass="highlight") # format the text into HTML

        # fill in the document header
        cssFile = open("html-template/stylesheet.css", "r")
        css = cssFile.read()
        cssFile.close()
        self.docHeader = self.docHeader.format(stylesheet="<style>\n{}\n</style>".format(css),
                                               pygments_stylesheet="<style>\n{}\n</style>".format(self.formatter.get_style_defs()))

    # override code block rendering
    def blockcode(self, text, lang):
        """Given a codeblock, generates the HTLM code to pretty-print using a parser for the specified language."""

        if not lang:
            # if no language is specified, simply return the text as a plain code block
            return "<div class='highlight'><pre>{}</pre></div>".format(text)
        else:
            lexer = get_lexer_by_name(lang, stripall=False) # lexer for the specified language
            return highlight(text, lexer, self.formatter)   # return the formated text

    # override html document header
    def doc_header(self, inline):
        return self.docHeader

    # override html document footer
    def doc_footer(self, inline):
        return self.docFooter
