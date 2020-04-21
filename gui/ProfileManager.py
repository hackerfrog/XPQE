from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Custom Imports
from qtconsole.qt import QtCore

from logger import log


class Profiler(QTableWidget):
    """
    Table of Profile Manager Dialog
    """
    COLUMNS_NAME = [
        'Profile', 'Engine Type'
    ]

    def __init__(self):
        """
        class set-up
        """
        super().__init__()
        self.log = log.getLogger(self.__class__.__name__)

        table_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        table_font.setPointSize(8)
        self.setFont(table_font)

        self.setStyleSheet('''
QHeaderView::section {
    background-color: #EEEEEE;
    border: 1px solid #DDDDDD;
}''')

        self.setColumnCount(len(self.COLUMNS_NAME))
        self.setHorizontalHeaderLabels(self.COLUMNS_NAME)

        for itr, column in enumerate(self.COLUMNS_NAME):
            self.horizontalHeaderItem(itr).setToolTip(column)

    def feed(self, info):
        """
        Populate table with profiles information
        :param info: profile infomations
        :return: None
        """
        self.clear()
        self.setColumnCount(len(self.COLUMNS_NAME))
        self.setHorizontalHeaderLabels(self.COLUMNS_NAME)

        for itr, column in enumerate(self.COLUMNS_NAME):
            self.horizontalHeaderItem(itr).setToolTip(column)

        try:
            pass
        except Exception as e:
            self.log.error(e)


class ProfileManager(QDialog):
    """
    Profile Manager Dialog
    """
    def __init__(self):
        """
        class set-up
        """
        super().__init__()
        self.log = log.getLogger(self.__class__.__name__)

        self.setWindowFlags(self.windowFlags() & ~ QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowTitle('Profile Manager')

        self.ui()

        self.exec()

    def ui(self):
        """
        UI of Profie Manager Dialog
        :return: None
        """
        frame = QVBoxLayout()

        profile_layout = QHBoxLayout()
        profiler = Profiler()
        profile_layout.addWidget(profiler, 85)
        profile_button_layout = QVBoxLayout()
        add_button = QPushButton('&Add')
        add_button.clicked.connect(self.__addServer)
        edit_button = QPushButton('&Edit')
        remove_button = QPushButton('&Remove')
        profile_button_layout.addWidget(add_button, alignment=Qt.AlignTop)
        profile_button_layout.addWidget(edit_button, alignment=Qt.AlignTop)
        profile_button_layout.addWidget(remove_button, alignment=Qt.AlignTop)
        profile_button_layout.addStretch()
        profile_layout.addLayout(profile_button_layout, 15)
        frame.addLayout(profile_layout)

        button_layout = QHBoxLayout()
        ok_button = QPushButton('&OK')
        cancel_button = QPushButton('&Cancel')
        apply_button = QPushButton('&Apply')
        button_layout.addStretch()
        button_layout.addWidget(ok_button, alignment=Qt.AlignRight)
        button_layout.addWidget(cancel_button, alignment=Qt.AlignRight)
        button_layout.addWidget(apply_button, alignment=Qt.AlignRight)
        frame.addLayout(button_layout)

        self.setLayout(frame)

    def __addServer(self):
        """
        Add new profile to Profile Manger
        :return: None
        """
        self.log.info('Add server')

