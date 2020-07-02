import sys

from functools import partial

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

# Custom Imports
from gui.CodeEditor import CodeEditor
from gui.ResultTable import ResultTable
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
    # CONTEXT
    context = dict()
    context['server.autocommit'] = False

    ############################################################################
    # RESULT TABLE
    result_table = ResultTable()

    ############################################################################
    # Modules Init
    profiler = Profiler()
    engine_manger = EngineManager(context, profiler, result_table)
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
    window.runXSQL_sc.activated.connect(partial(run_xsql, editor, engine_manger))

    ############################################################################
    # STATUS BAR
    statusBar = window.statusBar()
    statusBarWidget = QWidget()
    statusBarLayout = QHBoxLayout()
    statusBarLayout.setSpacing(0)
    statusBarLayout.setContentsMargins(0, 0, 0, 0)
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
    newFileAction.setIcon(QIcon('assets/icons/icon_new-file_100.png'))
    newFileAction.setShortcut('Ctrl+N')
    newFileAction.triggered.connect(partial(new_file, editor, fileManager))
    fileMenu.addAction(newFileAction)
    # Open Menu Item
    openFileAction = QAction('&Open', window)
    openFileAction.setIcon(QIcon('assets/icons/icon_open-file_100.png'))
    openFileAction.setShortcut('Ctrl+O')
    openFileAction.triggered.connect(partial(open_file, editor, fileManager))
    fileMenu.addAction(openFileAction)
    # Separator
    fileMenu.addSeparator()
    # Save Menu Item
    saveFileAction = QAction('&Save', window)
    saveFileAction.setIcon(QIcon('assets/icons/icon_save_100.png'))
    saveFileAction.setShortcut('Ctrl+S')
    saveFileAction.triggered.connect(partial(save_file, editor, fileManager))
    fileMenu.addAction(saveFileAction)
    # Save As Menu Item
    saveAsFileAction = QAction('&Save As', window)
    saveAsFileAction.setIcon(QIcon('assets/icons/icon_save-as_100.png'))
    saveAsFileAction.setShortcut('Ctrl+Shift+S')
    saveAsFileAction.triggered.connect(partial(save_as_file, editor, fileManager))
    fileMenu.addAction(saveAsFileAction)
    # Separator
    fileMenu.addSeparator()
    # Export Sub-Menu
    exportFileSubMenu = QMenu('&Export', window)
    exportFileSubMenu.setIcon(QIcon('assets/icons/icon_export_100.png'))
    fileMenu.addMenu(exportFileSubMenu)
    # Export As CSV Action
    csvExportFileAction = QAction('&As CSV', window)
    csvExportFileAction.setIcon(QIcon('assets/icons/icon_csv_100.png'))
    csvExportFileAction.triggered.connect(partial(export_result, context, 'csv', header=True))
    exportFileSubMenu.addAction(csvExportFileAction)
    # Export As CSV without header Action
    csvWoHeaderExportFileAction = QAction('&As CSV w/o Header', window)
    csvWoHeaderExportFileAction.setIcon(QIcon('assets/icons/icon_csv_100.png'))
    csvWoHeaderExportFileAction.triggered.connect(partial(export_result, context, 'csv', header=False))
    exportFileSubMenu.addAction(csvWoHeaderExportFileAction)
    # Export As HTML
    htmlExportFileAction = QAction('&As HTML', window)
    htmlExportFileAction.setIcon(QIcon('assets/icons/icon_html_100.png'))
    htmlExportFileAction.triggered.connect(partial(export_result, context, 'html'))
    exportFileSubMenu.addAction(htmlExportFileAction)
    # Separator
    fileMenu.addSeparator()
    # Exit Menu Item
    exitFileAction = QAction('&Exit', window)
    exitFileAction.setIcon(QIcon('assets/icons/icon_exit_100.png'))
    exitFileAction.triggered.connect(app.quit)
    fileMenu.addAction(exitFileAction)

    editMenu = menuBar.addMenu('&Edit')
    # Undo Menu Item
    undoEditAction = QAction('&Undo', window)
    undoEditAction.setIcon(QIcon('assets/icons/icon_undo_100.png'))
    undoEditAction.setShortcut('Ctrl+Z')
    undoEditAction.triggered.connect(partial(undo_text, editor))
    editMenu.addAction(undoEditAction)
    # Redo Menu Item
    redoEditAction = QAction('&Redo', window)
    redoEditAction.setIcon(QIcon('assets/icons/icon_redo_100.png'))
    redoEditAction.setShortcut('Ctrl+Y')
    redoEditAction.triggered.connect(partial(redo_text, editor))
    editMenu.addAction(redoEditAction)
    # Separator
    editMenu.addSeparator()
    # Cut Menu Item
    cutEditAction = QAction('&Cut', window)
    cutEditAction.setIcon(QIcon('assets/icons/icon_cut_100.png'))
    cutEditAction.setShortcut('Ctrl+X')
    cutEditAction.triggered.connect(partial(cut_text, editor))
    editMenu.addAction(cutEditAction)
    # Copy Menu Item
    copyEditAction = QAction('&Copy', window)
    copyEditAction.setIcon(QIcon('assets/icons/icon_copy_100.png'))
    copyEditAction.setShortcut('Ctrl+C')
    copyEditAction.triggered.connect(partial(copy_text, editor))
    editMenu.addAction(copyEditAction)
    # Paste Menu Item
    pasteEditAction = QAction('&Paste', window)
    pasteEditAction.setIcon(QIcon('assets/icons/icon_paste_100.png'))
    pasteEditAction.setShortcut('Ctrl+V')
    pasteEditAction.triggered.connect(partial(paste_text, editor))
    editMenu.addAction(pasteEditAction)
    # Delete Menu Item
    deleteEditAction = QAction('&Delete', window)
    deleteEditAction.setIcon(QIcon('assets/icons/icon_delete_100.png'))
    deleteEditAction.setShortcut('Delete')
    deleteEditAction.triggered.connect(partial(delete_text, editor))
    editMenu.addAction(deleteEditAction)
    # Separator
    editMenu.addSeparator()
    # Toggle Line-Comment Menu Item
    toggleCommentEditAction = QAction('&Toggle Line Comment', window)
    toggleCommentEditAction.setIcon(QIcon('assets/icons/icon_comment_100.png'))
    toggleCommentEditAction.setShortcut('Ctrl+/')
    toggleCommentEditAction.triggered.connect(partial(toggle_line_comment, editor))
    editMenu.addAction(toggleCommentEditAction)

    queryMenu = menuBar.addMenu('&Query')
    # Execute Menu Item
    executeQueryAction = QAction('&Execute', window)
    executeQueryAction.setIcon(QIcon('assets/icons/icon_play_100.png'))
    executeQueryAction.triggered.connect(partial(run_xsql, editor, engine_manger))
    queryMenu.addAction(executeQueryAction)
    # Separator
    queryMenu.addSeparator()
    # Toggle Auto-Commit Menu Item
    # noinspection PyArgumentList
    toggleAutoCommitQueryAction = QAction('&Auto Commit', window, checkable=True)
    toggleAutoCommitQueryAction.setChecked(False)
    toggleAutoCommitQueryAction.triggered.connect(partial(toggle_auto_commit, context))
    queryMenu.addAction(toggleAutoCommitQueryAction)

    profileMenu = menuBar.addMenu('&Profile')
    # Manage Menu Item
    manageProfileAction = QAction('&Manage', window)
    manageProfileAction.setIcon(QIcon('assets/icons/icon_manage_100.png'))
    manageProfileAction.triggered.connect(partial(open_profile_manager, profiler))
    profileMenu.addAction(manageProfileAction)

    viewMenu = menuBar.addMenu('&View')
    # StatusBar Toggle Menu Item
    # noinspection PyArgumentList
    statusBarViewAction = QAction('&Status Bar', window, checkable=True)
    statusBarViewAction.setChecked(True)
    statusBarViewAction.triggered.connect(partial(toggle_check, statusBar))
    viewMenu.addAction(statusBarViewAction)

    helpMenu = menuBar.addMenu('&Help')
    # About Menu Item
    aboutHelpAction = QAction('&About', window)
    aboutHelpAction.setIcon(QIcon('assets/icons/icon_about_100.png'))
    aboutHelpAction.triggered.connect(open_about_dialog)
    helpMenu.addAction(aboutHelpAction)

    ############################################################################
    # BODY
    frame = QWidget()

    layout = QHBoxLayout()

    editor_and_result_splitter = QSplitter(Qt.Horizontal)
    editor_and_result_splitter.addWidget(editor)
    editor_and_result_splitter.addWidget(result_table)
    editor_and_result_splitter.setSizes([50, 50])

    layout.addWidget(editor_and_result_splitter)

    frame.setLayout(layout)

    window.setCentralWidget(frame)
    window.show()

    ############################################################################
    # END
    sys.exit(app.exec_())
