from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QSyntaxHighlighter


class CodePainter(QSyntaxHighlighter):
    """
    Add syntax highlighter to editor text
    :param document: editor content
    """
    keywords = [
        # A
        'ACTION', 'ADD', 'ALL', 'ALTER', 'ANALYZE', 'AND', 'AS', 'ASC', 'AUTO_INCREMENT',
        # B
        'BDB', 'BERKELEYDB', 'BETWEEN', 'BIGINT', 'BINARY', 'BIT', 'BLOB', 'BOTH', 'BTREE', 'BY',
        # C
        'CASCADE', 'CASE', 'CHANGE', 'CHAR', 'CHARACTER', 'CHECK', 'COLLATE', 'COLUMN', 'COLUMNS', 'CONSTRAINT',
        'CREATE', 'CROSS', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP',
        # D
        'DATABASE', 'DATABASES', 'DATE', 'DAY_HOUR', 'DAY_MINUTE', 'DAY_SECOND', 'DEC', 'DECIMAL', 'DEFAULT', 'DELAYED',
        'DELETE', 'DESC', 'DESCRIBE', 'DISTINCT', 'DISTINCTROW', 'DIV', 'DOUBLE', 'DROP',
        # E
        'ELSE', 'ENCLOSED', 'ENUM', 'ERRORS', 'ESCAPED', 'EXISTS', 'EXPLAIN',
        # F
        'FALSE', 'FIELDS', 'FLOAT', 'FOR', 'FORCE', 'FOREIGN', 'FROM', 'FULLTEXT', 'FUNCTION',
        # G
        'GEOMETRY', 'GRANT', 'GROUP',
        # H
        'HASH', 'HAVING', 'HELP', 'HIGH_PRIORITY', 'HOUR_MINUTE', 'HOUR_SECOND',
        # I
        'IF', 'IGNORE', 'IN', 'INDEX', 'INFILE', 'INNER', 'INNODB', 'INSERT', 'INT', 'INTEGER', 'INTERVAL', 'INTO',
        'IS',
        # J
        'JOIN',
        # K
        'KEY', 'KEYS', 'KILL',
        # L
        'LEADING', 'LEFT', 'LIKE', 'LIMIT', 'LINES', 'LOAD', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCK', 'LONG', 'LONGBLOB',
        'LONGTEXT', 'LOW_PRIORITY',
        # M
        'MASTER_SERVER_ID', 'MATCH', 'MEDIUMBLOB', 'MEDIUMINT', 'MEDIUMTEXT', 'MIDDLEINT', 'MINUTE_SECOND', 'MOD',
        'MRG_MYISAM',
        # N
        'NATURAL', 'NO', 'NOT', 'NULL', 'NUMERIC',
        # O
        'ON', 'OPTIMIZE', 'OPTION', 'OPTIONALLY', 'OR', 'ORDER', 'OUTER', 'OUTFILE',
        # P
        'PRECISION', 'PRIMARY', 'PRIVILEGES', 'PROCEDURE', 'PURGE',
        # Q
        # R
        'READ', 'REAL', 'REFERENCES', 'REGEXP', 'RENAME', 'REPLACE', 'REQUIRE', 'RESTRICT', 'RETURNS', 'REVOKE',
        'RIGHT', 'RLIKE', 'RTREE',
        # S
        'SELECT', 'SET', 'SHOW', 'SMALLINT', 'SOME', 'SONAME', 'SPATIAL', 'SQL_BIG_RESULT', 'SQL_CALC_FOUND_ROWS',
        'SQL_SMALL_RESULT', 'SSL', 'STARTING', 'STRAIGHT_JOIN', 'STRIPED',
        # T
        'TABLE', 'TABLES', 'TERMINATED', 'TEXT', 'THEN', 'TIME', 'TIMESTAMP', 'TINYBLOB', 'TINYINT', 'TINYTEXT', 'TO',
        'TRAILING', 'TRUE', 'TYPES',
        # U
        'UNION', 'UNIQUE', 'UNLOCK', 'UNSIGNED', 'UPDATE', 'USAGE', 'USE', 'USER_RESOURCES', 'USING',
        # V
        'VALUES', 'VARBINARY', 'VARCHAR', 'VARCHARACTER', 'VARYING',
        # W
        'WARNINGS', 'WHEN', 'WHERE', 'WITH', 'WRITE',
        # X
        'XOR',
        # Y
        'YEAR_MONTH',
        # Z
        'ZEROFILL',
    ]

    operators = []

    braces = [r'\{', r'\}', r'\(', r'\)', r'\[', r'\]']

    def __init__(self, document, style):
        QSyntaxHighlighter.__init__(self, document)

        rules = []

        # Keyword, operator and brace rules
        rules += [(r'\b%s\b' % w, 0, style['keyword']) for w in CodePainter.keywords]
        # rules += [ (r'%s' % o, 0, style['operator']) for w in CodePainter.operators ]
        rules += [(r'%s' % b, 0, style['brace']) for b in CodePainter.braces]

        # Other rules
        rules += [
            # Double-Quote String
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, style['string']),
            # Single-Quote String
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, style['string']),
            # Single line Comment
            (r'\-\- [^\n]*', 0, style['comment']),
            # Numeric values
            (r'\b[+-]?[0-9]+[lL]?\b', 0, style['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, style['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, style['numbers']),
        ]

        self.rules = [(QRegExp(pattern, cs=Qt.CaseInsensitive), index, fmt) for (pattern, index, fmt) in rules]

    def highlightBlock(self, text):
        """
        This functions paints all colors on editor text according to rules
        :param text:
        :return:
        """
        for exp, nth, fmt in self.rules:
            index = exp.indexIn(text, 0)

            while index >= 0:
                index = exp.pos(nth)
                length = len(exp.cap(nth))
                self.setFormat(index, length, fmt)
                index = exp.indexIn(text, index+length)

            self.setCurrentBlockState(0)