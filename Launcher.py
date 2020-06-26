import sys

from functools import partial

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

# Custom Imports
from gui.CodeEditor import CodeEditor
from gui.ProfileManager import ProfileManager
from gui.ResultTable import ResultTable
from logger import log
from modules.CodePainter import CodePainter
from modules.EngineManager import EngineManager
from modules.FileManager import FileManager
from modules.Profiler import Profiler
from modules.trigger_func import *


# All style for syntax highlighter
STYLES = {
    'keyword': fmt('blue'),
    'operator': fmt('red'),
    'brace': fmt('brown'),
    'string': fmt('magenta'),
    'comment': fmt('darkGreen', 'italic'),
    'numbers': fmt('brown'),
}


if __name__ == '__main__':
    log.getLogger(__name__)
    log.info('STARTED')
    app = QApplication(sys.argv)

    ############################################################################
    # RESULT TABLE
    result_table = ResultTable()

    ############################################################################
    # Modules Init
    profiler = Profiler()
    engine_manger = EngineManager(profiler, result_table)
    fileManager = FileManager()

    ############################################################################
    # EDITOR
    editor = CodeEditor()
    highlight = CodePainter(editor.document(), STYLES)

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

    editor.cursorLocation = QLabel(text='Ln 0, Col 0')
    editor.cursorLocation.setFont(statusFont)
    statusBarLayout.addWidget(editor.cursorLocation, alignment=Qt.AlignRight)

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
    manageProfileAction.triggered.connect(partial(open_profile_manager, profiler))
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

    layout.addWidget(editor, 40)
    layout.addWidget(result_table, 60)

    frame.setLayout(layout)

    window.setCentralWidget(frame)
    window.show()

    ############################################################################
    # END
    sys.exit(app.exec_())
