from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Custom Imports
from logger import log


class AboutDialog(QDialog):
    def __init__(self):
        """
        About Dialog
        """
        super().__init__()
        self.log = log.getLogger(self.__class__.__name__)

        # noinspection PyTypeChecker
        self.setWindowFlags(self.windowFlags() & ~ Qt.WindowContextHelpButtonHint)
        self.setWindowTitle('About')

        self.ui()

        self.exec()

    def ui(self):
        """
        UI of About Dialog
        :return: None
        """
        frame = QVBoxLayout()

        icon8_text = 'App icons by <a target="_blank" href="https://icons8.com">Icons8</a>'
        app_icon = QPixmap(QPixmap('assets/logo.png'))
        app_version_text = '0.1.0-alpha_01'
        license_text = '<a target="_blank" href="https://github.com/hackerfrog/XPQE/blob/master/LICENSE">' \
                       'GNU General Public License v3.0</a>'
        github_text = '<a target="_blank" href="https://github.com/hackerfrog/XPQE">GitHub</a>'

        logo_name_layout = QHBoxLayout()
        # App Logo
        app_logo = QLabel(self)
        app_icon = app_icon.scaled(64, 64, Qt.KeepAspectRatio)
        app_logo.setPixmap(app_icon)
        app_logo.setStyleSheet('padding-right:16px;')
        logo_name_layout.addWidget(app_logo, alignment=Qt.AlignRight)
        # Name + Version Layout
        name_version_layout = QVBoxLayout()
        # App Name
        app_name = QLabel('XPQE')
        app_name.setStyleSheet('font-size:32px;font-weight:bold;')
        name_version_layout.addWidget(app_name, alignment=Qt.AlignLeft)
        # App Version
        app_version = QLabel('v' + app_version_text)
        name_version_layout.addWidget(app_version, alignment=Qt.AlignLeft)
        logo_name_layout.addLayout(name_version_layout)
        frame.addLayout(logo_name_layout)
        # Stretch
        frame.addStretch()
        # Source Code
        source_code_header = QLabel('Source Code')
        source_code_header.setStyleSheet('font-size:12px;font-weight:bold;')
        frame.addWidget(source_code_header, alignment=Qt.AlignCenter)
        github_label = QLabel(github_text)
        github_label.setOpenExternalLinks(True)
        frame.addWidget(github_label, alignment=Qt.AlignCenter)
        # LICENSE
        license_header = QLabel('LICENSE')
        license_header.setStyleSheet('font-size:12px;font-weight:bold;')
        frame.addWidget(license_header, alignment=Qt.AlignCenter)
        license_label = QLabel(license_text)
        license_label.setOpenExternalLinks(True)
        frame.addWidget(license_label, alignment=Qt.AlignCenter)
        # Stretch
        frame.addStretch()
        # Icon8 credit
        label_icon8 = QLabel(icon8_text)
        label_icon8.setOpenExternalLinks(True)
        frame.addWidget(label_icon8, alignment=Qt.AlignCenter)

        self.setLayout(frame)
