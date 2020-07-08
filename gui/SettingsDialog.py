from functools import partial

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Custom Imports
from logger import log


class SettingsDialog(QDialog):
    def __init__(self, context, editor):
        """
        Settings Dialog
        :param context: shared properties in application
        :param editor: object of CodeEditor class
        """
        super().__init__()
        self.log = log.getLogger(self.__class__.__name__)

        self.context = context
        self.editor = editor

        self.tab_widget = None
        self.font_size_input = None
        self.font_family_input = None
        self.font_family_temp_select = self.context.editor['font.family']
        self.font_weight_input = None
        self.font_weight_types = [
            QFont.Light, QFont.ExtraLight, QFont.Light, QFont.Normal, QFont.Medium, QFont.DemiBold, QFont.Bold,
            QFont.ExtraBold, QFont.Black
        ]
        self.font_weight_type_names = [
            'Light', 'Extra Light', 'Light', 'Normal', 'Medium', 'Demi Bold', 'Bold', 'ExtraBold', 'Black'
        ]
        self.font_stretch_input = None
        self.font_stretch_types = [
            QFont.UltraCondensed, QFont.ExtraCondensed, QFont.Condensed, QFont.SemiCondensed, QFont.Unstretched,
            QFont.SemiExpanded, QFont.Expanded, QFont.ExtraExpanded, QFont.UltraExpanded
        ]
        self.font_stretch_type_names = [
            'Ultra Condensed', 'Extra Condensed', 'Condensed', 'Semi Condensed', 'Unstretched', 'Semi Expanded',
            'Expanded', 'Extra Expanded', 'Ultra Expanded'
        ]
        self.auto_close_brackets_input = None
        self.auto_close_brackets_types = [
            'Always', 'Never'
        ]
        self.auto_close_quotes_input = None
        self.auto_close_quotes_types = [
            'Always', 'Never'
        ]
        self.result_render_count_input = None

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
        # Font Family
        font_family_label = QLabel('Font Family')
        self.font_family_input = QFontComboBox()
        self.font_family_input.setCurrentFont(QFont(self.context.editor['font.family']))
        self.font_family_input.currentFontChanged.connect(self.__font_change)
        font_layout.addRow(font_family_label, self.font_family_input)
        # Font Size
        font_size_label = QLabel('Font Size')
        self.font_size_input = QSpinBox()
        self.font_size_input.setMinimum(8)
        self.font_size_input.setMaximum(128)
        self.font_size_input.setValue(self.context.editor['font.pointSize'])
        font_layout.addRow(font_size_label, self.font_size_input)
        # Font Weight
        font_weight_label = QLabel('Weight')
        self.font_weight_input = QComboBox()
        self.font_weight_input.addItems(self.font_weight_type_names)
        self.font_weight_input.setCurrentIndex(self.font_weight_types.index(self.context.editor['font.weight']))
        font_layout.addRow(font_weight_label, self.font_weight_input)
        # Font Stretch
        font_stretch_label = QLabel('Stretch')
        self.font_stretch_input = QComboBox()
        self.font_stretch_input.addItems(self.font_stretch_type_names)
        self.font_stretch_input.setCurrentIndex(self.font_stretch_types.index(self.context.editor['font.stretch']))
        font_layout.addRow(font_stretch_label, self.font_stretch_input)
        font_group.setLayout(font_layout)
        editor_layout.addWidget(font_group)
        # Auto Close Group
        auto_close_group = QGroupBox('Auto Closing')
        auto_close_layout = QFormLayout()
        # Auto Close Brackets
        auto_close_brackets_label = QLabel('Brackets')
        self.auto_close_brackets_input = QComboBox()
        self.auto_close_brackets_input.addItems(self.auto_close_brackets_types)
        self.auto_close_brackets_input.setCurrentIndex(self.auto_close_brackets_types.index(
            self.context.editor['autoClosing.brackets']
        ))
        auto_close_layout.addRow(auto_close_brackets_label, self.auto_close_brackets_input)
        # Auto Close Quotes
        auto_close_quotes_label = QLabel('Quotes')
        self.auto_close_quotes_input = QComboBox()
        self.auto_close_quotes_input.addItems(self.auto_close_quotes_types)
        self.auto_close_quotes_input.setCurrentIndex(self.auto_close_quotes_types.index(
            self.context.editor['autoClosing.quotes']
        ))
        auto_close_layout.addRow(auto_close_quotes_label, self.auto_close_quotes_input)
        auto_close_group.setLayout(auto_close_layout)
        editor_layout.addWidget(auto_close_group)
        # Result Group
        result_group = QGroupBox('Result')
        result_layout = QFormLayout()
        result_render_count_label = QLabel('Max records render')
        self.result_render_count_input = QSpinBox()
        self.result_render_count_input.setMinimum(10)
        self.result_render_count_input.setMaximum(100000)
        self.result_render_count_input.setValue(self.context.editor['result.renderCount'])
        result_layout.addRow(result_render_count_label, self.result_render_count_input)
        result_group.setLayout(result_layout)
        editor_layout.addWidget(result_group)
        editor_layout.addStretch()
        editor_tab.setLayout(editor_layout)
        self.tab_widget.addTab(editor_tab, 'Editor')

        # Exports Tab
        export_tab = QWidget()
        export_layout = QVBoxLayout()
        export_layout.addWidget(QLabel('Export Body'))
        export_layout.addStretch()
        export_tab.setLayout(export_layout)
        self.tab_widget.addTab(export_tab, 'Export')
        frame.addWidget(self.tab_widget)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        ok_button = QPushButton('&OK')
        ok_button.clicked.connect(partial(self.__save_settings, terminate=True))
        button_layout.addWidget(ok_button)
        cancel_button = QPushButton('&Cancel')
        cancel_button.clicked.connect(self.close)
        button_layout.addWidget(cancel_button)
        apply_button = QPushButton('&Apply')
        apply_button.clicked.connect(self.__apply_settings)
        button_layout.addWidget(apply_button)
        frame.addLayout(button_layout)

        self.setLayout(frame)
        return self

    def __apply_settings(self):
        """
        Save all settings to context
        :return: None
        """
        current_tab = self.tab_widget.tabText(self.tab_widget.currentIndex())
        if current_tab.lower() == 'editor':
            self.context.editor['autoClosing.brackets'] = str(self.auto_close_brackets_input.currentText())
            self.context.editor['autoClosing.quotes'] = str(self.auto_close_quotes_input.currentText())
            self.context.editor['font.pointSize'] = self.font_size_input.value()
            self.context.editor['font.family'] = self.font_family_temp_select
            self.context.editor['font.weight'] = self.font_weight_types[self.font_weight_input.currentIndex()]
            self.context.editor['font.stretch'] = self.font_stretch_types[self.font_stretch_input.currentIndex()]
            self.context.editor['result.renderCount'] = self.result_render_count_input.value()
            self.__save_settings(terminate=False)
        elif current_tab.lower() == 'export':
            print('Exp')

    def __save_settings(self, terminate=True):
        """
        Make changes live on app window
        :param terminate: True to close settings dialog on call else False
        :return: None
        """
        font = QFont()
        font.setPointSize(self.context.editor['font.pointSize'])
        font.setFamily(self.context.editor['font.family'])
        font.setWeight(self.context.editor['font.weight'])
        font.setStretch(self.context.editor['font.stretch'])
        self.editor.setFont(font)
        if terminate:
            self.close()

    def __font_change(self, font):
        """
        Event function on change of font selection
        :param font: object of QFont passed by event function
        :return: None
        """
        self.font_family_temp_select = font.family()
