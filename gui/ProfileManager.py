from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Custom Imports
from Engines.MySQLEngine import MySQLEngine
from Engines.PostgreSQLEngine import PostgreSQLEngine
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

        self.setFocusPolicy(Qt.NoFocus)
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

    def refresh(self):
        self.clear()
        self.feed()


class ProfileManager(QDialog):
    def __init__(self, context, profiler):
        """
        Profile Manager Dialog
        :param context: shared properties in application
        :param profiler: object of class Profiler
        """
        super().__init__()
        self.log = log.getLogger(self.__class__.__name__)
        self.context = context
        self.profiler = profiler
        self.profileTable = ProfileTable(self.profiler)

        # noinspection PyTypeChecker
        self.setWindowFlags(self.windowFlags() & ~ Qt.WindowContextHelpButtonHint)
        self.setWindowTitle('Profile Manager')

        self.ui()

        self.exec()

    def ui(self):
        """
        UI of Profile Manager Dialog
        :return: None
        """
        frame = QVBoxLayout()

        profile_layout = QHBoxLayout()

        profile_layout.addWidget(self.profileTable, 85)
        profile_button_layout = QVBoxLayout()
        add_button = QPushButton('&Add')
        add_button.clicked.connect(self.__add_server)
        edit_button = QPushButton('&Edit')
        edit_button.clicked.connect(self.__edit_server)
        remove_button = QPushButton('&Remove')
        remove_button.clicked.connect(self.__remove_server)
        profile_button_layout.addWidget(add_button, alignment=Qt.AlignTop)
        profile_button_layout.addWidget(edit_button, alignment=Qt.AlignTop)
        profile_button_layout.addWidget(remove_button, alignment=Qt.AlignTop)
        profile_button_layout.addStretch()
        profile_layout.addLayout(profile_button_layout, 15)
        frame.addLayout(profile_layout)

        button_layout = QHBoxLayout()
        cancel_button = QPushButton('&Cancel')
        cancel_button.clicked.connect(self.close)
        ok_button = QPushButton('&OK')
        ok_button.clicked.connect(self.__save_and_close)
        button_layout.addStretch()
        button_layout.addWidget(cancel_button, alignment=Qt.AlignRight)
        button_layout.addWidget(ok_button, alignment=Qt.AlignRight)
        frame.addLayout(button_layout)

        self.setLayout(frame)

    def __save_and_close(self):
        """
        Save profiler and close ProfileManager Dialog
        :return:
        """
        self.profiler.save()
        self.close()

    def __add_server(self):
        """
        Add new profile to profiler
        :return: None
        """
        self.log.info('Add server')
        try:
            AddEditProfile(self.context, self.profiler)
            self.profileTable.refresh()
        except Exception as e:
            self.log.error(e)

    def __edit_server(self):
        """
        Edit profile properties and save in profiler
        :return: None
        """
        selected = self.profileTable.currentRow()
        if selected > -1:
            profile_name = self.profileTable.item(selected, 0).text()
            if self.profiler.checkProfileName(profile_name=profile_name):
                profile = self.profiler.getProfile(profile_name)
                AddEditProfile(self.context, self.profiler, mode='edit', profile=profile)
                self.profileTable.refresh()
            else:
                self.log.error("Profile: {} no longer exists in settings".format(profile_name))
        else:
            self.log.warn('Please select row before pressing edit button')

    def __remove_server(self):
        """
        Remove existing server from server profiler
        :return: None
        """
        selected = self.profileTable.currentRow()
        print(selected)
        if selected > -1:
            profile = self.profileTable.item(selected, 0).text()
            self.profiler.removeProfile(selected)
            self.profileTable.removeRow(selected)
            self.log.info('Profile: {} is been removed'.format(profile))
        else:
            self.log.warn('Please select row before pressing remove button')


class AddEditProfile(QDialog):
    def __init__(self, context, profiler, mode='add', profile=None):
        """
        Dialog to Add new or Edit existing server info in profiler
        :param context: shared properties in application
        :param profiler: object of profiler, keep track of each profile
        :param mode: determine to open dialog in Add/Edit mode.
        :param profile: profile which need changes, passed only when mode='edit'
        """
        super().__init__()
        self.log = log.getLogger(self.__class__.__name__)
        self.context = context
        self.profiler = profiler
        self.mode = mode
        self.profile = profile

        self.profile_name_input = None
        self.server_type_items = ['MySQL', 'PostgreSQL']
        self.server_type_combobox = None
        self.host_input = None
        self.port_input = None
        self.database_input = None
        self.username_input = None
        self.password_input = None

        # noinspection PyTypeChecker
        self.setWindowFlags(self.windowFlags() & ~ Qt.WindowContextHelpButtonHint)
        self.setWindowTitle('Add New Profile')

        self.ui()

        self.exec()

    def ui(self):
        """
        UI for AddEditDialog
        :return: None
        """
        frame = QVBoxLayout()

        container_layout = QFormLayout()
        profile_name_label = QLabel("Profile Name")
        self.profile_name_input = QLineEdit()
        container_layout.addRow(profile_name_label, self.profile_name_input)
        server_type_label = QLabel("Server")
        self.server_type_combobox = QComboBox()
        self.server_type_combobox.addItems(self.server_type_items)
        self.server_type_combobox.currentIndexChanged.connect(self.__server_type_change)
        container_layout.addRow(server_type_label, self.server_type_combobox)
        host_label = QLabel('Host')
        self.host_input = QLineEdit()
        container_layout.addRow(host_label, self.host_input)
        port_label = QLabel('Port')
        self.port_input = QLineEdit()
        self.port_input.setText('3306')
        container_layout.addRow(port_label, self.port_input)
        default_db_label = QLabel('Database')
        self.database_input = QLineEdit()
        container_layout.addRow(default_db_label, self.database_input)
        username_label = QLabel('Username')
        self.username_input = QLineEdit()
        container_layout.addRow(username_label, self.username_input)
        password_label = QLabel('Password')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        container_layout.addRow(password_label, self.password_input)

        if self.mode == 'edit':
            try:
                print(self.profile)
                self.profile_name_input.setText(self.profile.profile)
                self.server_type_combobox.setCurrentIndex(self.server_type_items.index(self.profile.type))
                self.host_input.setText(self.profile.host)
                self.port_input.setText(str(self.profile.port))
                self.database_input.setText(self.profile.database if self.profile.database else '')
                self.username_input.setText(self.profile.username)
                self.password_input.setText(self.profile.password)
            except Exception as e:
                print(e)

        button_layout = QHBoxLayout()
        test_button = QPushButton('&Test Connection')
        test_button.clicked.connect(self.__test_connection)
        cancel_button = QPushButton('&Cancel')
        cancel_button.clicked.connect(self.close)
        save_button = QPushButton('&Save')
        save_button.clicked.connect(self.__save_profile)
        button_layout.addWidget(test_button, alignment=Qt.AlignLeft)
        button_layout.addStretch()
        button_layout.addWidget(cancel_button, alignment=Qt.AlignRight)
        button_layout.addWidget(save_button, alignment=Qt.AlignRight)

        frame.addLayout(container_layout)
        frame.addStretch()
        frame.addLayout(button_layout)

        self.setLayout(frame)

    def __test_connection(self):
        """
        Test connectivity to server with give details in AddEditDialog
        :return: None
        """
        server_type = str(self.server_type_combobox.currentText()).lower()
        profile = Profile(
            self.profile_name_input.text(),
            server_type,
            host=self.host_input.text(),
            port=self.port_input.text(),
            database=self.database_input.text(),
            username=self.username_input.text(),
            password=self.password_input.text()
        )

        dialog = QMessageBox()
        if server_type == 'mysql':
            engine = MySQLEngine(self.context, profile)
            test_info = engine.test_connection()
            if test_info['status']:
                dialog.setIcon(QMessageBox.Information)
                dialog.setWindowTitle('Success')
                dialog.setText('Connection successful')
                dialog.setInformativeText("MySQL " + test_info['version'])
            else:
                dialog.setIcon(QMessageBox.Critical)
                dialog.setWindowTitle('Error')
                dialog.setText('Unable to connect')
                dialog.setInformativeText("Please check you detail, it seems something is wrong.")
        elif server_type == 'postgresql':
            dialog = QMessageBox()
            engine = PostgreSQLEngine(self.context, profile)
            test_info = engine.test_connection()
            if test_info['status']:
                dialog.setIcon(QMessageBox.Information)
                dialog.setWindowTitle('Success')
                dialog.setText('Connection successful')
                dialog.setInformativeText("PostgreSQL " + str(test_info['version']))
            else:
                dialog.setIcon(QMessageBox.Critical)
                dialog.setWindowTitle('Error')
                dialog.setText('Unable to connect')
                dialog.setInformativeText("Please check you detail, it seems something is wrong.")
        dialog.exec_()

    def __save_profile(self):
        """
        Save given details to profiler.
        :return: None
        """
        profile = Profile(
            self.profile_name_input.text(),
            str(self.server_type_combobox.currentText()),
            host=self.host_input.text(),
            port=self.port_input.text(),
            database=self.database_input.text(),
            username=self.username_input.text(),
            password=self.password_input.text()
        )
        if self.mode == 'add':
            self.profiler.addProfile(profile)
        elif self.mode == 'edit':
            self.profiler.editProfile(self.profile.profile, profile)
        self.close()

    def __server_type_change(self, index):
        """
        Change other elements properties on event
        :param index: index of QComboBox selected item
        :return: None
        """
        server_type = str(self.server_type_combobox.itemText(index)).lower()
        if server_type == 'mysql':
            self.port_input.setText('3306')
        elif server_type == 'postgresql':
            self.port_input.setText('5432')
            self.database_input.setText(
                'postgres' if self.database_input.text() == '' else self.database_input.text()
            )
