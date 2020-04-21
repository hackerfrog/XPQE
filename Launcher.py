import hashlib
import sys

from functools import partial

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# Custom Imports
from Engines import EngineManager
from logger import log
from gui.ProfileManager import ProfileManager

# TODO : below line is only for dev, remove if not needed
testPath = ''


class FileManager:
    """
    FileManger class keeps track of current file opened in editor
    """
    def __init__(self, string='', location=None):
        self.hash = None
        self.location = None
        self.reset(string, location)

    def reset(self, string='', location=None):
        """
        When opening new empty file in editor
        :param string: content of editor
        :param location: location of file
        :return: None
        """
        self.hash = hashlib.md5(string.encode()).hexdigest()
        self.location = location

    def set_hash(self, string):
        """
        Used to calculate MD5 hash of given string
        :param string: content of editor
        :return: None
        """
        self.hash = hashlib.md5(string.encode()).hexdigest()

    def set_location(self, location):
        """
        Used to update location of currently opened file
        :param location: Path where file reside
        :return: None
        """
        self.location = location

    def compare_hash(self, string):
        """
        Compare hash of given string with hash saved in class
        :param string: content of editor
        :return: True if hash matches else False
        """
        return True if self.hash == hashlib.md5(string.encode()).hexdigest() else False


# Cursor location in editor
cursorLocation = None
# Object of FileManger class
fileManager = FileManager()


def open_profile_manager(parent):
    """
    Open Profile Manager dialog
    :param parent: object of PyQt parent window
    :return: None
    """
    profile_manger = ProfileManager()
    # profile_manager = ProfileManager(parent)
    # try:
    #     profile_manager.show()
    # except Exception as e:
    #     log.error(e)


def toggle_check(element, state):
    """
    Toggle function to Show/Hide given PyQt element
    :param element: PyQt element object
    :param state: current state of element
    :return: None
    """
    if state:
        element.show()
    else:
        element.hide()


def copy_cell():
    """
    Manual Copy function when Copy Menu Item is click
    :return: None
    """
    # TODO: Create manual copy feature
    log.info('Copy Cell')


def save_file(editor, file_manager):
    """
    Save file when Save Menu Item or Shortcut is triggered
    :param editor: PyQt editor element
    :param file_manager: object of FileManger class
    :return: None
    """
    editor_text = editor.toPlainText()

    if file_manager.location:
        # if location exisit in file manger then just overwrite file without opening save dialog
        log.debug('Had file location : {}, Overwriting on same path'.format(file_manager.location))
        with open(file_manager.location, 'w') as file:
            file.write(editor_text)
        log.info('File Saved @ {}'.format(file_manager.location))

        log.debug('Updating file context details')
        file_manager.set_hash(editor_text)
    else:
        # if location is None then it's a new file
        save_file_dialog = QFileDialog.getSaveFileName(None, 'Save', '/' + testPath, 'Cross SQL Files (*.xsql)')

        if save_file_dialog[0]:
            with open(save_file_dialog[0], 'w') as file:
                file.write(editor_text)
            log.info('File Saved @ {}'.format(save_file_dialog[0]))

            log.debug('Updating file context details')
            file_manager.set_hash(editor_text)
            file_manager.set_location(save_file_dialog[0])


def new_file(editor, file_manager):
    """
    Open new empty file on editor when New Menu Item or Shortcut is triggered
    :param editor: object of editor
    :param file_manager: object of FileManger class
    :return: None
    """
    editor_text = editor.toPlainText()
    # check change in content of editor before opening new empty file
    if file_manager.compare_hash(editor_text):
        # Hash matched means no changes, directly open new empty file
        log.debug('Clearing editor')
        editor.setPlainText('')
        log.debug('Resetting file context details')
        file_manager.reset()
    else:
        # Changes found open confirmation dialog
        alert_message = QMessageBox()
        alert_message.setIcon(QMessageBox.Warning)
        alert_message.setText('You are having unsaved changes...')
        alert_message.setWindowTitle('Unsaved Changes Alter!')
        alert_message.setStandardButtons(QMessageBox.Save | QMessageBox.Ignore | QMessageBox.Cancel)

        alert_action = alert_message.exec()
        if alert_action == QMessageBox.Save:
            save_file(editor, file_manager)
            new_file(editor, file_manager)
        elif alert_action == QMessageBox.Ignore:
            file_manager.reset(string=editor_text)
            new_file(editor, file_manager)
        elif alert_message == QMessageBox.Cancel:
            pass


def open_file(editor, file_manager):
    """
    Open file from user disk
    :param editor: object of editor
    :param file_manager: object of FileManger class
    :return: None
    """
    open_file_dialog = QFileDialog.getOpenFileName(None, 'Open', '/' + testPath)

    if open_file_dialog[0]:
        log.info('Opening File @ {}'.format(open_file_dialog[0]))
        with open(open_file_dialog[0], 'r') as file:
            file_text = file.read()

        editor.setPlainText(file_text)

        log.debug('Updating file context details')
        file_manager.set_hash(file_text)
        file_manager.set_location(open_file_dialog[0])
        log.debug('Complete File Openning @ {}'.format(open_file_dialog[0]))


def save_as_file(editor, file_manager):
    """
    Save file without checking any constrains
    :param editor: object of editor
    :param file_manager: object of FileManager class
    :return: None
    """
    save_as_file_dialog = QFileDialog.getSaveFileName(None, 'Save As', '/' + testPath, 'Cross SQL Files (*.xsql)')

    if save_as_file_dialog[0]:
        editor_text = editor.toPlainText()
        with open(save_as_file_dialog[0], 'w') as file:
            file.write(editor_text)
        log.info('File Saved @ {}'.format(save_as_file_dialog[0]))

        log.debug('Updating file context details')
        file_manager.set_hash(editor_text)
        file_manager.set_location(save_as_file_dialog[0])


def undo_text():
    """
    Undo feature of editor
    :return: None
    """
    # TODO: Create Manual UNDO feature
    log.info('Undo')


def redo_text():
    """
    Redo feature of editor
    :return: None
    """
    # TODO: Create Manual REDO feature
    log.info('Redo')


def cut_text():
    """
    Cut selected text from an editor
    :return: None
    """
    # TODO: Create Manual Cut feature
    log.info('Cut')


def copy_text():
    """
    Copy selected text from an editor
    :return: None
    """
    # TODO: Create Manual Copy feature
    log.info('Copy')


def paste_text():
    """
    Paste selected text from an editor
    :return: None
    """
    # TODO: Create Manual Paste feature
    log.info('Paste')


def toggle_line_comment(editor, file_manager):
    """
    Toggle comment on line with current location of editor cursor
    :param editor: object of editor
    :param file_manager: object og FileManager class
    :return:None
    """
    # TODO: Create Toggle line comment feature
    log.info('Toggle Line Comment [Arg: {}, {}]'.format(editor, file_manager))


def run_xsql(editor, result_table, engine_manager):
    """
    Run XSQL query
    :param editor: object of editor
    :param result_table: object of ResultTable class to populate XSQL result
    :param engine_manager: object of EngineManager class
    :return: None
    """
    cursor = editor.textCursor()
    xsql = cursor.selectedText()
    if len(xsql) == 0:
        xsql = editor.toPlainText()
    log.info(xsql)

    engine_manager.parse(xsql)

    # # TODO: Run process XSQL and then run
    # mysql = MySQLEngine(
    #     host='ensembldb.ensembl.org',
    #     port=5306,
    #     username='anonymous',
    #     password='').connect()
    # mysql.sql(xsql)
    # result_table.feed(mysql.result)
    # mysql.close()


def fmt(color, style=''):
    """
    Creates format for syntax highlighter
    :param color: color name or hex code of color
    :param style: text weight style
    :return: object of QTextCharFormat class
    """
    _color = QColor()
    _color.setNamedColor(color)

    _fmt = QTextCharFormat()
    _fmt.setForeground(_color)
    if 'bold' in style:
        _fmt.setFontWeight(QFont.Bold)
    if 'italic' in style:
        _fmt.setFontItalic(True)

    return _fmt


# All styles for syntax highlighter
STYLES = {
    'keyword': fmt('blue'),
    'operator': fmt('red'),
    'brace': fmt('brown'),
    'string': fmt('magenta'),
    'comment': fmt('darkGreen', 'italic'),
    'numbers': fmt('brown'),
}


class CodePainter(QSyntaxHighlighter):
    """
    Add syntax highlighter to editor text
    """
    keywords = [
        # A
        'ACTION', 'ADD', 'ALL', 'ALTER', 'ANALYZE', 'AND', 'AS', 'ASC', 'AUTO_INCREMENT',
        # B
        'BDB', 'BERKELEYDB', 'BETWEEN', 'BIGINT', 'BINARY', 'BIT', 'BLOB', 'BOTH', 'BTREE', 'BY',
        # C
        'CASCADE', 'CASE', 'CHANGE', 'CHAR', 'CHARACTER', 'CHECK', 'COLLATE', 'COLUMN', 'COLUMNS', 'CONSTRAINT',
        'CREATE', 'CROSS', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP',
        # D
        'DATABASE', 'DATABASES', 'DATE', 'DAY_HOUR', 'DAY_MINUTE', 'DAY_SECOND', 'DEC', 'DECIMAL', 'DEFAULT', 'DELAYED',
        'DELETE', 'DESC', 'DESCRIBE', 'DISTINCT', 'DISTINCTROW', 'DIV', 'DOUBLE', 'DROP',
        # E
        'ELSE', 'ENCLOSED', 'ENUM', 'ERRORS', 'ESCAPED', 'EXISTS', 'EXPLAIN',
        # F
        'FALSE', 'FIELDS', 'FLOAT', 'FOR', 'FORCE', 'FOREIGN', 'FROM', 'FULLTEXT', 'FUNCTION',
        # G
        'GEOMETRY', 'GRANT', 'GROUP',
        # H
        'HASH', 'HAVING', 'HELP', 'HIGH_PRIORITY', 'HOUR_MINUTE', 'HOUR_SECOND',
        # I
        'IF', 'IGNORE', 'IN', 'INDEX', 'INFILE', 'INNER', 'INNODB', 'INSERT', 'INT', 'INTEGER', 'INTERVAL', 'INTO',
        'IS',
        # J
        'JOIN',
        # K
        'KEY', 'KEYS', 'KILL',
        # L
        'LEADING', 'LEFT', 'LIKE', 'LIMIT', 'LINES', 'LOAD', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCK', 'LONG', 'LONGBLOB',
        'LONGTEXT', 'LOW_PRIORITY',
        # M
        'MASTER_SERVER_ID', 'MATCH', 'MEDIUMBLOB', 'MEDIUMINT', 'MEDIUMTEXT', 'MIDDLEINT', 'MINUTE_SECOND', 'MOD',
        'MRG_MYISAM',
        # N
        'NATURAL', 'NO', 'NOT', 'NULL', 'NUMERIC',
        # O
        'ON', 'OPTIMIZE', 'OPTION', 'OPTIONALLY', 'OR', 'ORDER', 'OUTER', 'OUTFILE',
        # P
        'PRECISION', 'PRIMARY', 'PRIVILEGES', 'PROCEDURE', 'PURGE',
        # Q
        # R
        'READ', 'REAL', 'REFERENCES', 'REGEXP', 'RENAME', 'REPLACE', 'REQUIRE', 'RESTRICT', 'RETURNS', 'REVOKE',
        'RIGHT', 'RLIKE', 'RTREE',
        # S
        'SELECT', 'SET', 'SHOW', 'SMALLINT', 'SOME', 'SONAME', 'SPATIAL', 'SQL_BIG_RESULT', 'SQL_CALC_FOUND_ROWS',
        'SQL_SMALL_RESULT', 'SSL', 'STARTING', 'STRAIGHT_JOIN', 'STRIPED',
        # T
        'TABLE', 'TABLES', 'TERMINATED', 'TEXT', 'THEN', 'TIME', 'TIMESTAMP', 'TINYBLOB', 'TINYINT', 'TINYTEXT', 'TO',
        'TRAILING', 'TRUE', 'TYPES',
        # U
        'UNION', 'UNIQUE', 'UNLOCK', 'UNSIGNED', 'UPDATE', 'USAGE', 'USE', 'USER_RESOURCES', 'USING',
        # V
        'VALUES', 'VARBINARY', 'VARCHAR', 'VARCHARACTER', 'VARYING',
        # W
        'WARNINGS', 'WHEN', 'WHERE', 'WITH', 'WRITE',
        # X
        'XOR',
        # Y
        'YEAR_MONTH',
        # Z
        'ZEROFILL',
    ]

    operators = []

    braces = [r'\{', r'\}', r'\(', r'\)', r'\[', r'\]']

    def __init__(self, document):
        """
        Add colors according syntax rules
        :param document: editor content
        """
        QSyntaxHighlighter.__init__(self, document)

        rules = []

        # Keyword, operator and brace rules
        rules += [(r'\b%s\b' % w, 0, STYLES['keyword']) for w in CodePainter.keywords]
        # rules += [ (r'%s' % o, 0, STYLES['operator']) for w in CodePainter.operators ]
        rules += [(r'%s' % b, 0, STYLES['brace']) for b in CodePainter.braces]

        # Other rules
        rules += [
            # Double-Quote String
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),
            # Single-Quote String
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),
            # Single line Comment
            (r'\-\- [^\n]*', 0, STYLES['comment']),
            # Numeric values
            (r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['numbers']),
        ]

        self.rules = [(QRegExp(pattern, cs=Qt.CaseInsensitive), index, fmt) for (pattern, index, fmt) in rules]

    def highlightBlock(self, text):
        """
        This functions paints all colors on editor text according to rules
        :param text:
        :return:
        """
        for exp, nth, fmt in self.rules:
            index = exp.indexIn(text, 0)

            while index >= 0:
                index = exp.pos(nth)
                length = len(exp.cap(nth))
                self.setFormat(index, length, fmt)
                index = exp.indexIn(text, index+length)

            self.setCurrentBlockState(0)


class LineNumberArea(QWidget):
    """
    Add line number to given editor
    """
    def __init__(self, editor):
        """
        class set-up
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
    """
    Code Editor
    """
    def __init__(self):
        """
        set-up of code editor
        """
        super().__init__()
        self.log = log.getLogger(self.__class__.__name__)

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
        cursorLocation.setText('Ln {}, Col {}{}'.format(
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


class ResultTable(QTableWidget):
    """
    Table used to display result of executed query
    """
    def __init__(self):
        """
        class set-up
        """
        super().__init__()
        self.log = log.getLogger(self.__class__.__name__)

        # Set Font Style and Size
        table_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        table_font.setPointSize(8)
        self.setFont(table_font)

        self.setStyleSheet('''
QHeaderView::section {
    background-color: #EEEEEE;
    border: 1px solid #DDDDDD;
}''')

    def contextMenuEvent(self, event):
        """
        Event handler for table content area
        :param event: object of event
        :return: None
        """
        index = self.indexAt(event.pos())
        menu = QMenu()
        copy_text_action = QAction('&Copy Cell', self)
        # TODO: Copy Event on Cell Right Click
        copy_text_action.triggered.connect()
        menu.addAction(copyEditAction)

    def feed(self, result):
        """
        Populate table with result of executed query
        :param result: Result of executed query
        :return: None
        """
        self.clear()
        sample = result[0]
        try:
            self.setColumnCount(len(sample.keys()))
            self.setRowCount(min(1000, len(result)))
            self.setHorizontalHeaderLabels(sample.keys())
            self.setSortingEnabled(True)

            for itr, column in enumerate(sample.keys()):
                self.horizontalHeaderItem(itr).setToolTip(column)

            for itr_r, row in enumerate(result[:1000] if len(result) >= 1000 else result):
                self.setRowHeight(itr_r, 18)
                for itr_c, cell in enumerate(row.items()):
                    item = QTableWidgetItem(str(cell[1]))
                    item.setToolTip(str(cell[1]))
                    self.setItem(itr_r, itr_c, item)

        except Exception as e:
            self.log.error(e)


if __name__ == '__main__':
    log.getLogger(__name__)
    log.info('STARTED')
    app = QApplication(sys.argv)

    ############################################################################
    # ENGINE MANAGER
    engine_manger = EngineManager()

    ############################################################################
    # EDITOR
    editor = CodeEditor()
    highlight = CodePainter(editor.document())

    ############################################################################
    # RESULT TABLE
    result_table = ResultTable()

    ############################################################################
    # APP INIT
    window = QMainWindow()
    window.setWindowTitle('XPQE')
    window.setWindowIcon(QIcon('assets/logo.png'))
    # window.setWindowFlags(window.windowFlags() & ~Qt.WindowMaximizeButtonHint)

    ############################################################################
    # CUSTOM SHORTCUT
    window.runXSQL_sc = QShortcut(QKeySequence('Ctrl+Return'), window)
    window.runXSQL_sc.activated.connect(partial(run_xsql, editor, result_table, engine_manger))

    ############################################################################
    # STATUS BAR
    statusBar = window.statusBar()
    statusBarWidget = QWidget()
    statusBarLayout = QHBoxLayout()
    statusBarLayout.setSpacing(0)
    statusBarLayout.setContentsMargins(0, 0, 0, 0)
    # statusBarWidget.setStyleSheet('border:1px solid red;')
    statusFont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
    statusFont.setPointSize(8)

    cursorLocation = QLabel(text='Ln 0, Col 0')
    cursorLocation.setFont(statusFont)
    statusBarLayout.addWidget(cursorLocation, alignment=Qt.AlignRight)

    statusBarWidget.setLayout(statusBarLayout)
    statusBar.addWidget(statusBarWidget, 1)

    window.setStatusBar(statusBar)

    ############################################################################
    # MENU BAR
    menuBar = window.menuBar()

    fileMenu = menuBar.addMenu('&File')
    # New Menu Item
    newFileAction = QAction('&New', window)
    newFileAction.setShortcut('Ctrl+N')
    newFileAction.triggered.connect(partial(new_file, editor, fileManager))
    fileMenu.addAction(newFileAction)
    # Open Menu Item
    openFileAction = QAction('&Open', window)
    openFileAction.setShortcut('Ctrl+O')
    openFileAction.triggered.connect(partial(open_file, editor, fileManager))
    fileMenu.addAction(openFileAction)
    # Separator
    fileMenu.addSeparator()
    # Save Menu Item
    saveFileAction = QAction('&Save', window)
    saveFileAction.setShortcut('Ctrl+S')
    saveFileAction.triggered.connect(partial(save_file, editor, fileManager))
    fileMenu.addAction(saveFileAction)
    # Save As Menu Item
    saveAsFileAction = QAction('&Save As', window)
    saveAsFileAction.setShortcut('Ctrl+Shift+S')
    saveAsFileAction.triggered.connect(partial(save_as_file, editor, fileManager))
    fileMenu.addAction(saveAsFileAction)
    # Separator
    fileMenu.addSeparator()
    # Exit Menu Item
    exitFileAction = QAction('&Exit', window)
    exitFileAction.triggered.connect(app.quit)
    fileMenu.addAction(exitFileAction)

    editMenu = menuBar.addMenu('&Edit')
    # Undo Menu Item
    undoEditAction = QAction('&Undo', window)
    undoEditAction.setShortcut('Ctrl+Z')
    undoEditAction.triggered.connect(undo_text)
    editMenu.addAction(undoEditAction)
    # Redo Menu Item
    redoEditAction = QAction('&Redo', window)
    redoEditAction.setShortcut('Ctrl+Y')
    redoEditAction.triggered.connect(redo_text)
    editMenu.addAction(redoEditAction)
    # Separator
    editMenu.addSeparator()
    # Cut Menu Item
    cutEditAction = QAction('&Cut', window)
    cutEditAction.setShortcut('Ctrl+X')
    cutEditAction.setDisabled(True)
    cutEditAction.triggered.connect(cut_text)
    editMenu.addAction(cutEditAction)
    # Copy Menu Item
    copyEditAction = QAction('&Copy', window)
    copyEditAction.setShortcut('Ctrl+C')
    copyEditAction.setDisabled(True)
    copyEditAction.triggered.connect(copy_text)
    editMenu.addAction(copyEditAction)
    # Paste Menu Item
    pasteEditAction = QAction('&Paste', window)
    pasteEditAction.setShortcut('Ctrl+V')
    pasteEditAction.setDisabled(True)
    pasteEditAction.triggered.connect(paste_text)
    editMenu.addAction(pasteEditAction)
    # Separator
    editMenu.addSeparator()
    # Toggle Line-Comment Menu Item
    undoEditAction = QAction('&Toggel Line Comment', window)
    undoEditAction.setShortcut('Ctrl+/')
    undoEditAction.triggered.connect(partial(toggle_line_comment, editor, fileManager))
    editMenu.addAction(undoEditAction)

    profileMenu = menuBar.addMenu('&Profile')
    # Manage Menu Item
    manageProfileAction = QAction('Manage', window)
    manageProfileAction.triggered.connect(partial(open_profile_manager, window))
    profileMenu.addAction(manageProfileAction)

    viewMenu = menuBar.addMenu('&View')
    # StatusBar Toggle Menu Item
    # noinspection PyArgumentList
    statusBarViewAction = QAction('Status Bar', window, checkable=True)
    statusBarViewAction.setChecked(True)
    statusBarViewAction.triggered.connect(partial(toggle_check, statusBar))
    viewMenu.addAction(statusBarViewAction)

    ############################################################################
    # BODY
    frame = QWidget()

    layout = QHBoxLayout()

    layout.addWidget(editor, 60)
    layout.addWidget(result_table, 40)

    frame.setLayout(layout)

    window.setCentralWidget(frame)
    window.show()

    ############################################################################
    # TESTING
    # mysql = MySQLEngine(host='db4free.net', username='xpqeuser', password='tooruser').connect()
    #
    # mysql.close()

    ############################################################################
    # END
    sys.exit(app.exec_())
