#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Project: Quark Note Taker
File: mdhighlighter.py
Author: Leonardo Banderali
Created: August 3, 2014
Last Modified: August 3, 2014

Description:
    This file contains the class used to perform syntax highlighting on the markdown note editor.


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


#~import modules~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#python modules
import sys
import os
import copy

#Qt objects
from PyQt5.QtCore import Qt, QRegularExpression, QRegularExpressionMatch
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont
#from PyQt5.QtWidgets import *


#~note editor~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MDHighlighter(QSyntaxHighlighter):
    """Syntax highlighting class for markdown."""

    def __init__(self, parentDocument):
        """Initializes rules (regexp) to find the text that needs to be highlighted"""
        super(MDHighlighter, self).__init__(parentDocument)
        self.blockRules = {
            "quote": [QRegularExpression("^( {0,3})>"), QRegularExpression("^\\s*$") ],
            "code": [QRegularExpression("^```"), QRegularExpression("^```\\s*$") ]
        }
        self.itemRules = {
            "list_item": QRegularExpression("^(( {0,3})>)?\\s*[\\*\\-:]\\s"),
            "header": QRegularExpression("^(#{1,6}|\\-+|=+\\s*$)"),
            "hard_break": QRegularExpression("^( {1,3}(\\-\\s){3,}| {0,3}(\\s*\\*){3,}| {0,3}_{3,})\\s*$"),
        }
        self.spanRules = {
            "link": QRegularExpression("!?\\[[^\\n]*\\](\\([^\\n]*\\)|\\[[^\\n]*\\])"),
            "link_id": QRegularExpression("^( {0,3})\\[[^\\s]*\\]:\\s*[^\\s]+(\\s+(\"[^\"\\n]*\"|\'[^\"\\n]*\'|\([^\"\\n]*\)))?"),
            "emphasis": QRegularExpression("\\s((\\*)[^\\n\\s]+(\\*)|(\\*)(\\*)[^\\n\\s]*(\\*)(\\*)|_[^\\n\\s]*_|__[^\\n\\s]*__)\\s"),
            "code": QRegularExpression("`[^\\n`]+`|``[^\\n]*``"),
            "math": QRegularExpression("\\$[^\\n]*\\$|\\$\\$[^\\n]*\\$\\$")
        }


    def highlightBlock(self, text):
        """Finds and highlights text.  Is called on each line/block of the document every time the text changes."""
        textFormat = QTextCharFormat()

        textFormat.setForeground(Qt.darkRed)
        defaultOffset = 0
        if self.previousBlockState() > 0:
            rule = list(self.blockRules.values())[self.previousBlockState() - 1]
            ruleMatch = rule[1].match(text)
            if not ruleMatch.hasMatch():
                self.setCurrentBlockState( self.previousBlockState() )
                self.setFormat(0, len(text), textFormat)    #no need to subtract one from the length as 'text' includes an extra '\n' (?)
                return
            self.setCurrentBlockState(0)
            self.setFormat(0, ruleMatch.capturedLength(), textFormat)
            defaultOffset = ruleMatch.capturedLength()

        counter = 1
        for ruleName, rule in self.blockRules.items():
            if (not rule[0].isValid() ) or (not rule[1].isValid() ):
                print(ruleName + " rule is not valid.")
            ruleMatch = rule[0].match(text, defaultOffset)
            if not ruleMatch.hasMatch():
                counter += 1
                continue
            self.setCurrentBlockState(counter)
            start = ruleMatch.capturedStart()
            self.setFormat(start, len(text) - start, textFormat)
            return

        textFormat.setFontWeight(QFont.Black)   #QFont.Black is heavier that QFont.Bold
        textFormat.setForeground(Qt.blue)
        for ruleName, rule in self.itemRules.items():
            if not rule.isValid():
                print(ruleName + " rule is not valid.")
            ruleMatch = rule.match(text, defaultOffset)
            while ruleMatch.hasMatch():
                self.setFormat(ruleMatch.capturedStart(), ruleMatch.capturedLength(), textFormat)
                ruleMatch = rule.match(text, ruleMatch.capturedEnd() + 1)

        textFormat.setFontWeight(QFont.Normal)
        textFormat.setForeground(Qt.darkMagenta)
        for ruleName, rule in self.spanRules.items():
            if not rule.isValid():
                print(ruleName + " is not valid.")
            ruleMatch = rule.match(text, defaultOffset)
            while ruleMatch.hasMatch():
                self.setFormat(ruleMatch.capturedStart(), ruleMatch.capturedLength(), textFormat)
                ruleMatch = rule.match(text, ruleMatch.capturedEnd() + 1)
