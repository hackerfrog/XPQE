from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
import psycopg2

from logger import log

from datetime import datetime


class PostgreSQLEngine:
    def __init__(self, context, profile, result_table=None):
        """
        Query Engine of PostgreSQL database
        :param context: shared properties in application
        :param profile: object of Profile class, contain all information regarding server connection
        :param result_table: object of ResultTable class, to populate result into table
        """
        self.log = log.getLogger(self.__class__.__name__)

        self.context = context
        self.profile = profile
        self.resultTable = result_table

        self.con = None
        self.cursor = None     # Cursor
        self.result = None

    def test_connection(self):
        """
        Test connection to server
        :return: dict
        """
        import psycopg2

        test_info = dict()

        try:
            self.con = psycopg2.connect(
                host=self.profile.host,
                port=self.profile.port,
                database=self.profile.database,
                user=self.profile.username,
                password=self.profile.password
            )
            self.con.autocommit = self.context.server['autoCommit']
            self.log.info('Connect to PostgreSQL server, server version: {}'.format(self.con.server_version))
            test_info['status'] = True
            test_info['version'] = self.con.server_version
            self.cursor = self.con.cursor()
            self.log.info('Cursor is Created')

        except psycopg2.Error as e:
            test_info['status'] = False
            self.log.error('Error while connecting to PostgreSQL, {}'.format(e))

        return test_info

    def connect(self):
        """
        Build connection with server
        :return: self
        """
        self.test_connection()
        return self

    def displayError(self, error):
        """
        :param error: Exception occurred while running XSQL
        :return: self
        """
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle('SQL Error')
        error_dialog.setText(str(error))
        error_dialog.exec_()
        return self

    def sql(self, query):
        """
        Query executor
        :param query: PostgreSQL query
        :return: self
        """
        self.log.info(r'{}'.format(query))
        try:
            self.cursor.execute(query)
            self.result = self.cursor.fetchall()
            self.context.xpqe['execute.sql'] = query
            self.context.xpqe['execute.result'] = self.result
            self.context.xpqe['execute.server'] = self.profile.type
            self.context.xpqe['execute.host'] = self.profile.host
            self.context.xpqe['execute.timestamp'] = str(datetime.fromtimestamp(datetime.now().timestamp()).isoformat())
        except psycopg2.Error as e:
            self.log.error(e)
            self.displayError(e)
            return None
        return self

    def feed(self):
        """
        Populate table with result of executed query
        :return: None
        """
        self.resultTable.clear()
        self.resultTable.maxRenderRecords = self.context.editor['result.renderCount']
        column_names = [col[0] for col in self.cursor.description]
        try:
            self.resultTable.setColumnCount(len(self.cursor.description))
            self.resultTable.setRowCount(min(self.resultTable.maxRenderRecords, len(self.result)))
            self.resultTable.setHorizontalHeaderLabels(column_names)
            self.resultTable.setSortingEnabled(True)

            for itr, column in enumerate(column_names):
                self.resultTable.horizontalHeaderItem(itr).setToolTip(column)

            for itr_r, row in enumerate(self.result[:self.resultTable.maxRenderRecords]
                                        if len(self.result) >= self.resultTable.maxRenderRecords else self.result):
                self.resultTable.setRowHeight(itr_r, 18)
                for itr_c, cell in enumerate(row):
                    cell_value = str('' if cell is None else cell)
                    cell_value_4tooltip = str('NULL' if cell is None else cell)
                    item = QTableWidgetItem(cell_value)
                    item.setToolTip(cell_value_4tooltip)
                    self.resultTable.setItem(itr_r, itr_c, item)

            self.resultTable.resultCount.setText('Showing {:,} of {:,} records'.format(
                self.resultTable.maxRenderRecords if self.cursor.rowcount > self.resultTable.maxRenderRecords else self.cursor.rowcount,
                self.cursor.rowcount
            ))
        except Exception as e:
            self.log.error(e)

    def close(self):
        """
        Close PostgreSQL connection
        :return: True if connection is closed else False
        """
        self.cursor.close()
        self.log.info('PostgreSQL connection is closed')
        return self.cursor.closed
