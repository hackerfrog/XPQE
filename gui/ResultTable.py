from logger import log

from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QTableWidget, QMenu, QAction


class ResultTable(QTableWidget):
    def __init__(self):
        """
        Table used to display result of executed query
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
        menu.addAction(copy_text_action)
