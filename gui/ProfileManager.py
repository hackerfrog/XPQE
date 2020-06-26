from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Custom Imports
from qtconsole.qt import QtCore

from logger import log
from modules.Profiler import Profile


class ProfileTable(QTableWidget):
    COLUMNS_NAME = [
        'Profile', 'Engine Type', 'Host', 'Port', 'Username'
    ]

    def __init__(self, profiler):
        """
        Table of Profile Manager Dialog
        :param profiler: object of class Profiler
        """
        super().__init__()
        self.log = log.getLogger(self.__class__.__name__)
        self.profiler = profiler

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

        self.feed()

    def feed(self):
        """
        Populate table with profiler information
        :return: None
        """
        self.clear()
        self.setColumnCount(len(self.COLUMNS_NAME))
        self.log.info('Profiler length : ' + str(len(self.profiler.list)))
        self.setRowCount(len(self.profiler.list))
        self.setHorizontalHeaderLabels(self.COLUMNS_NAME)

        for itr, column in enumerate(self.COLUMNS_NAME):
            self.horizontalHeaderItem(itr).setToolTip(column)

        try:
            self.log.info(self.profiler.list)
            for itr_r, profile in enumerate(self.profiler.list):
                self.setRowHeight(itr_r, 18)
                cell_profile = QTableWidgetItem(str(profile.profile))
                self.setItem(itr_r, 0, cell_profile)
                cell_type = QTableWidgetItem(str(profile.type))
                self.setItem(itr_r, 1, cell_type)
                cell_host = QTableWidgetItem(str(profile.host))
                self.setItem(itr_r, 2, cell_host)
                cell_port = QTableWidgetItem(str(profile.port))
                self.setItem(itr_r, 3, cell_port)
                cell_username = QTableWidgetItem(str(profile.username))
                self.setItem(itr_r, 4, cell_username)
        except Exception as e:
            self.log.error(e)


class ProfileManager(QDialog):
    def __init__(self, profiler):
        """
        Profile Manager Dialog
        :param profiler: object of class Profiler
        """
        super().__init__()
        self.log = log.getLogger(self.__class__.__name__)
        self.profiler = profiler
        self.profileTable = ProfileTable(self.profiler)

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

        profile_layout.addWidget(self.profileTable, 85)
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
        try:
            add_profile = AddProfile()
            # self.profiler.addProfile(Profile(
            #     profile='genome',
            #     profile_type='MySQL',
            #     host='ensembldb.ensembl.org',
            #     port=5306,
            #     username='anonymous',
            #     password=''
            # ))
        except Exception as e:
            self.log.error(e)


class AddProfile(QDialog):
    def __init__(self):
        super(AddProfile, self).__init__()
        self.log = log.getLogger(self.__class__.__name__)

        self.setWindowFlags(self.windowFlags() & ~ QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowTitle('Add New Profile')

        self.ui()

        self.exec()

    def ui(self):
        pass
