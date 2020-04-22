from logger import log

from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QTableWidget, QMenu, QAction, QTableWidgetItem


class ResultTable(QTableWidget):
    """
    Table used to display result of executed query
    """
    def __init__(self):
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

    def feed(self, result):
        """
        Populate table with result of executed query
        :param result: Result of executed query
        :return: None
        """
        self.clear()
        sample = result[0]
        try:
            self.setColumnCount(len(sample.keys()))
            self.setRowCount(min(1000, len(result)))
            self.setHorizontalHeaderLabels(sample.keys())
            self.setSortingEnabled(True)

            for itr, column in enumerate(sample.keys()):
                self.horizontalHeaderItem(itr).setToolTip(column)

            for itr_r, row in enumerate(result[:1000] if len(result) >= 1000 else result):
                self.setRowHeight(itr_r, 18)
                for itr_c, cell in enumerate(row.items()):
                    item = QTableWidgetItem(str(cell[1]))
                    item.setToolTip(str(cell[1]))
                    self.setItem(itr_r, itr_c, item)

        except Exception as e:
            self.log.error(e)
