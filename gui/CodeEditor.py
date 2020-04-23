from PyQt5.QtGui import QFontDatabase, QColor, QTextFormat, QPainter

from logger import log

from PyQt5.QtCore import QSize, QRect, Qt
from PyQt5.QtWidgets import QWidget, QPlainTextEdit, QTextEdit


class LineNumberArea(QWidget):
    def __init__(self, editor):
        """
        Add line number to given editor
        :param editor: object of editor
        """
        super().__init__(editor)
        self.editor = editor
        self.log = log.getLogger(self.__class__.__name__)

    def sizeHint(self):
        """
        Adjust width of area where line number are present
        :return: object of QSize class
        """
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        """
        On editor's paint event we are updating line number
        :param event: object of event
        :return: None
        """
        self.log.debug('paintEvent()')
        self.editor.lineNumberAreaPaintEvent(event)


class CodeEditor(QPlainTextEdit):
    def __init__(self):
        """
        Code Editor
        """
        super().__init__()
        self.log = log.getLogger(self.__class__.__name__)

        self.cursorLocation = None

        self.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))

        self.lineNumberArea = LineNumberArea(self)

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)

    def highlightCurrentLine(self):
        """
        Highlight current line with different background color
        :return: None
        """
        extra_selections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor(0, 0, 255, 50)

            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        self.setExtraSelections(extra_selections)

    def lineNumberAreaWidth(self):
        """
        Adjust width of line-number area
        :return: width of area
        """
        digits = 1
        count = max(1, self.blockCount())
        while count >= 10:
            count /= 10
            digits += 1
        space = 10 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        """
        Update line number area width
        :param _: event
        :return: None
        """
        self.log.debug('updateLineNumberAreaWidth(): margin = {}'.format(self.lineNumberAreaWidth()))
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        """
        Update Line number area
        :param rect: current viewport area
        :param dy: Scroll location
        :return: None
        """
        self.log.debug('updateLineNumberArea(): rect = {}, dy = {}'.format(rect, dy))

        cursor = self.textCursor()
        selected_text_details = '' if len(cursor.selectedText()) == 0 else ' ({} selected)'.format(
            len(cursor.selectedText())
        )
        self.cursorLocation.setText('Ln {}, Col {}{}'.format(
            cursor.blockNumber(),
            cursor.columnNumber(),
            selected_text_details)
        )

        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())

        self.log.debug('updateLineNumberArea(): rect.contains(self.viewport().rect()) = {}'.format(
            rect.contains(self.viewport().rect()))
        )
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        """
        Update line number area on resize event of editor
        :param event: object of event
        :return: None
        """
        super().resizeEvent(event)

        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        """
        Paint line number on editor event on editor
        :param event: object of event
        :return: None
        """
        self.log.debug('lineNumberAreaPaintEvent()')
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        height = self.fontMetrics().height()

        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(block_number + 1) + ' '
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.lineNumberArea.width(), height, Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1
