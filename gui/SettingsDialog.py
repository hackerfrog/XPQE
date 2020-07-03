from functools import partial

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Custom Imports
from logger import log


class SettingsDialog(QDialog):
    def __init__(self, context):
        """
        Settings Dialog
        :param context: shared properties in application
        """
        super().__init__()
        self.log = log.getLogger(self.__class__.__name__)

        self.context = context

        self.tab_widget = None
        self.font_size_input = None

        # noinspection PyTypeChecker
        self.setWindowFlags(self.windowFlags() & ~ Qt.WindowContextHelpButtonHint)
        self.setWindowTitle('Settings')

        self.ui()

        self.exec()

    def ui(self):
        """
        UI of Settings Dialog
        :return: None
        """
        frame = QVBoxLayout()

        self.tab_widget = QTabWidget()
        # Editor Tab
        editor_tab = QWidget()
        editor_layout = QVBoxLayout()
        # Font Group
        font_group = QGroupBox('Font')
        font_layout = QFormLayout()
        font_size_label = QLabel('Font Size')
        self.font_size_input = QSpinBox()
        self.font_size_input.setMinimum(8)
        self.font_size_input.setMaximum(128)
        self.font_size_input.setValue(self.context.editor['font.pointSize'])
        font_layout.addRow(font_size_label, self.font_size_input)
        font_group.setLayout(font_layout)
        editor_layout.addWidget(font_group)
        editor_tab.setLayout(editor_layout)
        self.tab_widget.addTab(editor_tab, 'Editor')
        # Exports Tab
        export_tab = QWidget()
        export_layout = QVBoxLayout()
        export_layout.addWidget(QLabel('Export Body'))
        export_tab.setLayout(export_layout)
        self.tab_widget.addTab(export_tab, 'Export')
        frame.addWidget(self.tab_widget)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        ok_button = QPushButton('&OK')
        ok_button.clicked.connect(self.__save_settings)
        button_layout.addWidget(ok_button)
        cancel_button = QPushButton('&Cancel')
        button_layout.addWidget(cancel_button)
        apply_button = QPushButton('&Apply')
        apply_button.clicked.connect(self.__apply_settings)
        button_layout.addWidget(apply_button)
        frame.addLayout(button_layout)

        self.setLayout(frame)
        return self

    def __apply_settings(self):
        current_tab = self.tab_widget.tabText(self.tab_widget.currentIndex())
        if current_tab.lower() == 'editor':
            self.context.editor['font.pointSize'] = self.font_size_input.value()
        elif current_tab.lower() == 'export':
            print('Exp')

    def __save_settings(self):
        pass
