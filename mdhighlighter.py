#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
Project: Quark Note Taker
File: mdhighlighter.py
Author: Leonardo Banderali
Created: August 3, 2014
Last Modified: August 21, 2014

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
import enchant

#Qt objects
from PyQt5.QtCore import Qt, QRegularExpression, QRegularExpressionMatch
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont
#from PyQt5.QtWidgets import *



#~note editor~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class MDHighlighter(QSyntaxHighlighter):
    """Syntax highlighting class for markdown.
Text is highlighted in a plain text document/editor by
calling the function 'highlightBlock(self, text)'.  It is called automatically when the text in the
document/editor changes.  The text passed to this function is a single line (block) of the document
text.  This function will be called on each line/block of the document when its text is changed by
the user.
Highlighting is done by matching text in the document using regular expressions (rules).  These define
the exact text which will be highlighted.  When a match is found, the coresponding text (in the document)
is highlighted using the 'setFormat(start, count, format)' method."""

    def __init__(self, parentDocument):
        """Initializes rules (regexp) to find the text that needs to be highlighted"""
        super(MDHighlighter, self).__init__(parentDocument)

        # the language dictionary to be used
        self.dictionary = enchant.Dict("en_CA") # use this dictionary for now

        ########################################################################
        ### Rules are stored in dictionaries in order for each rule to have a ##
        ### label by which it can be identified.                              ##
        ########################################################################

        #rules that can span multiple lines (in the format '[start expression, end expression]')
        self.blockRules = {
            "quote": [QRegularExpression("^( {0,3})>"), QRegularExpression("^\\s*$") ],
            "code": [QRegularExpression("^```"), QRegularExpression("^```\\s*$") ],
            "blockMath": [QRegularExpression("\\$\\$"), QRegularExpression("\\$\\$") ]
        }

        #rules for single items (in the format 'expression')
        self.itemRules = {
            "list_item": QRegularExpression("^(( {0,3})>)?\\s*[\\*\\-\\+:]\\s"),
            "header": QRegularExpression("^(#{1,6}|\\-+|=+\\s*$)"),
            "hard_break": QRegularExpression("^( {1,3}(\\-\\s){3,}| {0,3}(\\s*\\*){3,}| {0,3}_{3,})\\s*$"),
            "toc": QRegularExpression("\\[TOC\\]")
        }

        #rules that span on one line (in the format 'expression')
        self.spanRules = {
            "link": QRegularExpression("!?\\[[^\\n)]*\\](\\([^\\n)]*\\)|\\[[^\\n)]*\\])"),
            "link_id": QRegularExpression("^( {0,3})\\[[^\\s]*\\]:\\s*[^\\s]+(\\s+(\"[^\"\\n]*\"|\'[^\"\\n]*\'|\([^\"\\n]*\)))?"),
            "emphasis": QRegularExpression("(\\s?\\*[^\\s])([^*]*)([^\\s]\\*\\s?)|(\\s?\\*{2}[^\\s])([^*]*)([^\\s]\\*{2}\\s?)|(\\s_[^\\s])([^_]*)([^\\s]_\\s?)|(\\s?_{2}[^\\s])([^_]*)([^\\s]\\_{2}\\s)"),
            "code": QRegularExpression("`[^\\n`]+`|``[^\\n]*``"),
            "math": QRegularExpression("\\$[^\\n\\$]+\\$")
        }


    def spellcheck(self, text):
        if not self.dictionary:
            return

        wordFinder = QRegularExpression("[A-Za-z]+");
        wordIterator = wordFinder.globalMatch(text)
        while wordIterator.hasNext():
            match = wordIterator.next()
            if not self.dictionary.check(match.captured()):
                # update the word's current format
                spellingErrorformat = self.format(match.capturedStart())
                spellingErrorformat.setUnderlineColor(Qt.red)
                spellingErrorformat.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)

                # set the new format
                self.setFormat(match.capturedStart(), match.capturedLength(), spellingErrorformat)


    def highlightBlock(self, text):
        """Finds and highlights text using regular expressions.  Is called on each
line/block of the document every time the text changes."""

        textFormat = QTextCharFormat()  #the format/highlighting to apply to text is stored here
        defaultOffset = 0               #stores an offset from which to start search for rule matches in the text

        #######################################################################
        ### Multi-line span rules are handled by asigning a 'block-state' to ##
        ### the current line/block of text being highlighted.  On the next   ##
        ### call to this function, the state of the previous line/block is   ##
        ### checked to see if the new current line is part of a multi-line   ##
        ### span.  If the end expression for this rule is matched, then the  ##
        ### function will highlight the line up to the end of the expression ##
        ### and continue highlighting the rest of the line normally.  Else,  ##
        ### it will highlight the whole line and assign the same block-state ##
        ### to it.                                                           ##
        #######################################################################

        #highlight text if inside a multi-line span
        textFormat.setForeground(Qt.darkRed)    #assign style for multi-line spans
        if self.previousBlockState() > 0:       #if inside a multi-line span
            rule = list(self.blockRules.values())[self.previousBlockState() - 1]#get the rule corresponding to the block-state
            ruleMatch = rule[1].match(text)
            if not ruleMatch.hasMatch():                                        #if the end expressions for the rule is not found
                self.setCurrentBlockState( self.previousBlockState() )              #continue inside the current multi-line span (block-state)
                self.setFormat(0, len(text), textFormat)                            #(no need to subtract one from the length as 'text' includes an extra '\n' ?)
                self.spellcheck(text)   # highlight spelling errors
                return                                                              #no need to highlight anything else so return
            else:                                                               #else
                self.setCurrentBlockState(0)                                        #set the normal block-state
                self.setFormat(0, ruleMatch.capturedEnd(), textFormat)              #apply highlighting to the end of the expression match
                defaultOffset = ruleMatch.capturedLength()                          #highlight normally from the end of the expression match

        #match and highlight start of a multi-line span
        counter = 1 #used to keep track of which rule is being checked
        for ruleName, rule in self.blockRules.items():          #for every rule
            if (not rule[0].isValid() ) or (not rule[1].isValid() ):#if the rule is not valid, print an error message and continue
                print(ruleName + ": rule is not valid.")
                continue
            ruleMatch = rule[0].match(text, defaultOffset)          #match the rule
            if not ruleMatch.hasMatch():                            #if the start expression is not matched, move on to the next rule
                counter += 1
                continue
            endMatch = rule[1].match(text, defaultOffset + ruleMatch.capturedLength() )
            start = ruleMatch.capturedStart()
            if endMatch.hasMatch():                                 #if the end expression is matched,
                self.setFormat(start, endMatch.capturedEnd() - start, textFormat)#highlight to the end of the match
                defaultOffset = endMatch.capturedEnd()                  #
                counter += 1                                            #
                continue                                                #move on to the next rule
            else:                                                   #else, highlight full line and set a block-state using 'counter'
                self.setCurrentBlockState(counter)
                self.setFormat(start, len(text) - start, textFormat)
                self.spellcheck(text)   # highlight spelling errors
                return

        #highlight single items
        textFormat.setFontWeight(QFont.Black)   #QFont.Black is heavier that QFont.Bold
        textFormat.setForeground(Qt.blue)
        for ruleName, rule in self.itemRules.items():
            if not rule.isValid():
                print(ruleName + ": rule is not valid.")
                continue
            ruleMatch = rule.match(text, defaultOffset)
            while ruleMatch.hasMatch():         #match all occurrences of the rule in the text line/block
                self.setFormat(ruleMatch.capturedStart(), ruleMatch.capturedLength(), textFormat)
                ruleMatch = rule.match(text, ruleMatch.capturedEnd() + 1)

        #highlight single-line spans
        textFormat.setFontWeight(QFont.Normal)
        textFormat.setForeground(Qt.darkMagenta)
        for ruleName, rule in self.spanRules.items():
            if not rule.isValid():
                print(ruleName + ": rule is not valid.")
                continue
            ruleMatch = rule.match(text, defaultOffset)
            while ruleMatch.hasMatch():
                self.setFormat(ruleMatch.capturedStart(), ruleMatch.capturedLength(), textFormat)
                ruleMatch = rule.match(text, ruleMatch.capturedEnd() + 1)

        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%% I have left the highlighting code "un-cleaned" because I %%
        #%% plan on implementing some major changes in the future.   %%
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        self.spellcheck(text) # highlight spelling errors
