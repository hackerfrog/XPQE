from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from functools import partial

# Custom Imports
from logger import log

from modules.trigger_func import *


class Main(QMainWindow):
    def __init__(self, context,  app, editor, engine_manager, file_manager, profiler, result_table):
        """
        :param context: shared properties in application
        :param app: object of QApplication
        :param editor: object of CodeEditor class
        :param engine_manager: object of EngineManager class
        :param file_manager: object of FileManger class
        :param profiler: object of Profiler class
        :param result_table: object of ResultTable class
        """
        super().__init__()
        self.log = log.getLogger(self.__class__.__name__)

        # ARGUMENTS
        self.context = context
        self.app = app
        self.editor = editor
        self.engine_manager = engine_manager
        self.file_manager = file_manager
        self.profiler = profiler
        self.result_table = result_table

        # APP INIT
        self.setWindowTitle('XPQE')
        self.setWindowIcon(QIcon('assets/logo.png'))
        self.move(self.context.window['position'][0], self.context.window['position'][1])
        self.resize(self.context.window['size'][0], self.context.window['size'][1])
        # self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        # CUSTOM SHORTCUT
        self.runXSQL_sc = QShortcut(QKeySequence('Ctrl+Return'), self)
        self.runXSQL_sc.activated.connect(partial(run_xsql, self.editor, self.engine_manager))

        # CUSTOM VARIABLES
        self.status_bar = None

        # UI-Build Functions call
        self.ui_status_bar()
        self.ui_menu_bar()

        # BODY
        frame = QWidget()

        layout = QHBoxLayout()

        self.editor_and_result_splitter = QSplitter(Qt.Horizontal)
        self.editor_and_result_splitter.addWidget(self.editor)
        self.editor_and_result_splitter.addWidget(self.result_table)
        self.editor_and_result_splitter.setSizes(self.context.editor['editorToResultRatio'])

        layout.addWidget(self.editor_and_result_splitter)

        frame.setLayout(layout)

        self.setCentralWidget(frame)

    def ui_status_bar(self):
        """
        UI elements of Status Bar
        :return:
        """
        self.status_bar = self.statusBar()
        statusBarWidget = QWidget()
        statusBarLayout = QHBoxLayout()
        statusBarLayout.setSpacing(0)
        statusBarLayout.setContentsMargins(8, 0, 8, 8)
        statusFont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        statusFont.setPointSize(8)

        self.result_table.resultCount = QLabel(text='Welcome User 😉')
        self.result_table.resultCount.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.result_table.resultCount.setFont(statusFont)
        statusBarLayout.addWidget(self.result_table.resultCount, alignment=Qt.AlignLeft)
        statusBarLayout.addStretch()
        self.editor.cursorLocation = QLabel(text='Ln 0, Col 0')
        self.editor.cursorLocation.setFont(statusFont)
        statusBarLayout.addWidget(self.editor.cursorLocation, alignment=Qt.AlignRight)

        statusBarWidget.setLayout(statusBarLayout)
        self.status_bar.addWidget(statusBarWidget, 1)

        self.setStatusBar(self.status_bar)

    def ui_menu_bar(self):
        """
        UI elements of Menu Bar
        :return:
        """
        menuBar = self.menuBar()

        fileMenu = menuBar.addMenu('&File')
        # New Menu Item
        newFileAction = QAction('&New', self)
        newFileAction.setIcon(QIcon('assets/icons/icon_new-file_100.png'))
        newFileAction.setShortcut('Ctrl+N')
        newFileAction.triggered.connect(partial(new_file, self.editor, self.file_manager))
        fileMenu.addAction(newFileAction)
        # Open Menu Item
        openFileAction = QAction('&Open', self)
        openFileAction.setIcon(QIcon('assets/icons/icon_open-file_100.png'))
        openFileAction.setShortcut('Ctrl+O')
        openFileAction.triggered.connect(partial(open_file, self.editor, self.file_manager))
        fileMenu.addAction(openFileAction)
        # Separator
        fileMenu.addSeparator()
        # Save Menu Item
        saveFileAction = QAction('&Save', self)
        saveFileAction.setIcon(QIcon('assets/icons/icon_save_100.png'))
        saveFileAction.setShortcut('Ctrl+S')
        saveFileAction.triggered.connect(partial(save_file, self.editor, self.file_manager))
        fileMenu.addAction(saveFileAction)
        # Save As Menu Item
        saveAsFileAction = QAction('&Save As', self)
        saveAsFileAction.setIcon(QIcon('assets/icons/icon_save-as_100.png'))
        saveAsFileAction.setShortcut('Ctrl+Shift+S')
        saveAsFileAction.triggered.connect(partial(save_as_file, self.editor, self.file_manager))
        fileMenu.addAction(saveAsFileAction)
        # Separator
        fileMenu.addSeparator()
        # Settings Menu Item
        settingsFileAction = QAction('&Settings', self)
        settingsFileAction.setIcon(QIcon('assets/icons/icon_settings_100.png'))
        settingsFileAction.setShortcut('Ctrl+,')
        settingsFileAction.triggered.connect(partial(open_settings_dialog, self.context, self.editor))
        fileMenu.addAction(settingsFileAction)
        # Separator
        fileMenu.addSeparator()
        # Export Sub-Menu
        exportFileSubMenu = QMenu('&Export', self)
        exportFileSubMenu.setIcon(QIcon('assets/icons/icon_export_100.png'))
        fileMenu.addMenu(exportFileSubMenu)
        # Export As CSV Action
        csvExportFileAction = QAction('&As CSV', self)
        csvExportFileAction.setIcon(QIcon('assets/icons/icon_csv_100.png'))
        csvExportFileAction.triggered.connect(partial(export_result, self.context, 'csv', header=True))
        exportFileSubMenu.addAction(csvExportFileAction)
        # Export As CSV without header Action
        csvWoHeaderExportFileAction = QAction('&As CSV w/o Header', self)
        csvWoHeaderExportFileAction.setIcon(QIcon('assets/icons/icon_csv_100.png'))
        csvWoHeaderExportFileAction.triggered.connect(partial(export_result, self.context, 'csv', header=False))
        exportFileSubMenu.addAction(csvWoHeaderExportFileAction)
        # Export As HTML
        htmlExportFileAction = QAction('&As HTML', self)
        htmlExportFileAction.setIcon(QIcon('assets/icons/icon_html_100.png'))
        htmlExportFileAction.triggered.connect(partial(export_result, self.context, 'html'))
        exportFileSubMenu.addAction(htmlExportFileAction)
        # Export As PDF
        pdfExportFileAction = QAction('&As PDF', self)
        pdfExportFileAction.setIcon(QIcon('assets/icons/icon_pdf_100.png'))
        pdfExportFileAction.triggered.connect(partial(export_result, self.context, 'pdf'))
        exportFileSubMenu.addAction(pdfExportFileAction)
        # Separator
        fileMenu.addSeparator()
        # Exit Menu Item
        exitFileAction = QAction('&Exit', self)
        exitFileAction.setIcon(QIcon('assets/icons/icon_exit_100.png'))
        exitFileAction.triggered.connect(self.app.quit)
        fileMenu.addAction(exitFileAction)

        editMenu = menuBar.addMenu('&Edit')
        # Undo Menu Item
        undoEditAction = QAction('&Undo', self)
        undoEditAction.setIcon(QIcon('assets/icons/icon_undo_100.png'))
        undoEditAction.setShortcut('Ctrl+Z')
        undoEditAction.triggered.connect(partial(undo_text, self.editor))
        editMenu.addAction(undoEditAction)
        # Redo Menu Item
        redoEditAction = QAction('&Redo', self)
        redoEditAction.setIcon(QIcon('assets/icons/icon_redo_100.png'))
        redoEditAction.setShortcut('Ctrl+Y')
        redoEditAction.triggered.connect(partial(redo_text, self.editor))
        editMenu.addAction(redoEditAction)
        # Separator
        editMenu.addSeparator()
        # Cut Menu Item
        cutEditAction = QAction('&Cut', self)
        cutEditAction.setIcon(QIcon('assets/icons/icon_cut_100.png'))
        cutEditAction.setShortcut('Ctrl+X')
        cutEditAction.triggered.connect(partial(cut_text, self.editor))
        editMenu.addAction(cutEditAction)
        # Copy Menu Item
        copyEditAction = QAction('&Copy', self)
        copyEditAction.setIcon(QIcon('assets/icons/icon_copy_100.png'))
        copyEditAction.setShortcut('Ctrl+C')
        copyEditAction.triggered.connect(partial(copy_text, self.editor))
        editMenu.addAction(copyEditAction)
        # Paste Menu Item
        pasteEditAction = QAction('&Paste', self)
        pasteEditAction.setIcon(QIcon('assets/icons/icon_paste_100.png'))
        pasteEditAction.setShortcut('Ctrl+V')
        pasteEditAction.triggered.connect(partial(paste_text, self.editor))
        editMenu.addAction(pasteEditAction)
        # Delete Menu Item
        deleteEditAction = QAction('&Delete', self)
        deleteEditAction.setIcon(QIcon('assets/icons/icon_delete_100.png'))
        deleteEditAction.setShortcut('Delete')
        deleteEditAction.triggered.connect(partial(delete_text, self.editor))
        editMenu.addAction(deleteEditAction)
        # Separator
        editMenu.addSeparator()
        # Toggle Line-Comment Menu Item
        toggleCommentEditAction = QAction('&Toggle Line Comment', self)
        toggleCommentEditAction.setIcon(QIcon('assets/icons/icon_comment_100.png'))
        toggleCommentEditAction.setShortcut('Ctrl+/')
        toggleCommentEditAction.triggered.connect(partial(toggle_line_comment, self.editor))
        editMenu.addAction(toggleCommentEditAction)

        queryMenu = menuBar.addMenu('&Query')
        # Execute Menu Item
        executeQueryAction = QAction('&Execute', self)
        executeQueryAction.setIcon(QIcon('assets/icons/icon_play_100.png'))
        executeQueryAction.triggered.connect(partial(run_xsql, self.editor, self.engine_manager))
        queryMenu.addAction(executeQueryAction)
        # Separator
        queryMenu.addSeparator()
        # Toggle Auto-Commit Menu Item
        # noinspection PyArgumentList
        toggleAutoCommitQueryAction = QAction('&Auto Commit', self, checkable=True)
        toggleAutoCommitQueryAction.setChecked(self.context.server['autoCommit'])
        toggleAutoCommitQueryAction.triggered.connect(partial(toggle_auto_commit, self.context))
        queryMenu.addAction(toggleAutoCommitQueryAction)

        profileMenu = menuBar.addMenu('&Profile')
        # Manage Menu Item
        manageProfileAction = QAction('&Manage', self)
        manageProfileAction.setIcon(QIcon('assets/icons/icon_manage_100.png'))
        manageProfileAction.triggered.connect(partial(open_profile_manager, self.context, self.profiler))
        profileMenu.addAction(manageProfileAction)

        viewMenu = menuBar.addMenu('&View')
        # StatusBar Toggle Menu Item
        # noinspection PyArgumentList
        statusBarViewAction = QAction('&Status Bar', self, checkable=True)
        statusBarViewAction.setChecked(True)
        statusBarViewAction.triggered.connect(partial(toggle_check, self.status_bar))
        viewMenu.addAction(statusBarViewAction)

        helpMenu = menuBar.addMenu('&Help')
        # About Menu Item
        aboutHelpAction = QAction('&About', self)
        aboutHelpAction.setIcon(QIcon('assets/icons/icon_about_100.png'))
        aboutHelpAction.triggered.connect(open_about_dialog)
        helpMenu.addAction(aboutHelpAction)

    def resizeEvent(self, event):
        """
        Event function called when window is resized
        :param event: object of QEvent class
        :return: None
        """
        size = self.size()
        self.context.window['size'] = [size.width(), size.height()]

    def moveEvent(self, event):
        """
        Event function called when window position is changed
        :param event: object of QEvent class
        :return: None
        """
        position = self.pos()
        self.context.window['position'] = [position.x(), position.y()]

    def closeEvent(self, event):
        """
        Event function called just before closing Application/Window
        :param event: object of QEvent class
        :return: None
        """
        self.context.editor['maximized'] = self.isMaximized()
        self.context.editor['editorToResultRatio'] = self.editor_and_result_splitter.sizes()
        self.context.saveSettings()
