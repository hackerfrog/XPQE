from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox

from logger import log


class MySQLEngine:
    def __init__(self, context, profile, result_table=None):
        """
        Query Engine of MuSQL database
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
        import mysql.connector
        from mysql.connector import Error

        test_info = dict()

        try:
            self.con = mysql.connector.connect(
                host=self.profile.host,
                port=self.profile.port,
                user=self.profile.username,
                password=self.profile.password
            )
            self.con.autocommit = self.context.server['autoCommit']
            if self.con.is_connected():
                db_info = self.con.get_server_info()
                self.log.info('Connect to MySQL server, server version: {}'.format(db_info))
                test_info['status'] = True
                test_info['version'] = str(db_info)
                self.cursor = self.con.cursor(dictionary=True)
                self.log.info('Cursor is Created')
        except Error as e:
            test_info['status'] = False
            self.log.error('Error while connecting to MySQL, {}'.format(e))

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
        :param query: MySQL query
        :return: self
        """
        self.log.info(r'{}'.format(query))
        try:
            self.cursor.execute(query)
            self.result = self.cursor.fetchall()
            self.context.xpqe['execute.sql'] = query
            self.context.xpqe['execute.result'] = self.result
            self.context.xpqe['execute.server'] = self.profile.type
        except Exception as e:
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
        sample = self.result[0]
        try:
            self.resultTable.setColumnCount(len(sample.keys()))
            self.resultTable.setRowCount(min(self.resultTable.maxRenderRecords, len(self.result)))
            self.resultTable.setHorizontalHeaderLabels(sample.keys())
            self.resultTable.setSortingEnabled(True)

            for itr, column in enumerate(sample.keys()):
                self.resultTable.horizontalHeaderItem(itr).setToolTip(column)

            for itr_r, row in enumerate(self.result[:1000] if len(self.result) >= self.resultTable.maxRenderRecords else self.result):
                self.resultTable.setRowHeight(itr_r, 18)
                for itr_c, cell in enumerate(row.items()):
                    cell_value = str('' if cell[1] is None else cell[1])
                    cell_value_4tooltip = str('NULL' if cell[1] is None else cell[1])
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
        Close MySQL connection
        :return: True if connection is closed else False
        """
        if self.con.is_connected():
            if self.cursor:
                self.cursor.close()
            self.con.close()
            self.log.info('MySQL connection is closed')
            return True
        return False
