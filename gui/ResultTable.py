from functools import partial

from logger import log

from PyQt5.QtGui import QFontDatabase, QCursor
from PyQt5.QtWidgets import QTableWidget, QMenu, QAction, QApplication


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
        cells = self.selectedItems()

        popMenu = QMenu()
        copyPopAction = QAction('&Copy')
        popMenu.addAction(copyPopAction)
        popMenu.triggered.connect(partial(self.copy_select_cells, cells))
        popMenu.exec(QCursor.pos())
        event.accept()

    def copy_select_cells(self, cells):
        selected_text = ''
        track = {
            'row': -1,
            'col': -1
        }
        for cell in cells:
            if track['row'] == -1 or track['col'] == -1:
                track['row'] = cell.row()
                track['col'] = cell.column()
                selected_text += cell.text()
            else:
                if track['row'] == cell.row():
                    track['col'] = cell.column()
                    selected_text += ',' + cell.text()
                else:
                    track['row'] = cell.row()
                    track['col'] = cell.column()
                    selected_text += '\n' + cell.text()
        QApplication.clipboard().setText(selected_text)
        return self
