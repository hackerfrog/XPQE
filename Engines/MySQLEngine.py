from logger import log


class MySQLEngine:
    def __init__(self, host=None, port=3306, username=None, password=None):
        """
        Query Engine of MuSQL database
        :param host: server host name or ip address
        :param port: server port
        :param username: username for database access
        :param password: password for database access
        """
        self.log = log.getLogger(self.__class__.__name__)

        self.host = host
        self.port = port
        self.username = username
        self.password = password

        self.con = None
        self.cursor = None     # Cursor
        self.result = None

    def connect(self):
        """
        Build connection with server
        :return: self
        """
        import mysql.connector
        from mysql.connector import Error

        try:
            self.con = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.username,
                password=self.password
            )
            if self.con.is_connected():
                db_info = self.con.get_server_info()
                self.log.info('Connect to MySQL server, server version: {}'.format(db_info))
                self.cursor = self.con.cursor(dictionary=True)
                self.log.info('Cursor is Created')
        except Error as e:
            self.log.error('Error while connecting to MySQL, {}'.format(e))

        return self

    def sql(self, query):
        """
        Query executor
        :param query: MySQL query
        :return: self
        """
        try:
            self.cursor.execute(query)
            self.result = self.cursor.fetchall()
        except Exception as e:
            self.log.error(e)
        return self

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
