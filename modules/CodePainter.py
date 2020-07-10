from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QSyntaxHighlighter


class CodePainter(QSyntaxHighlighter):
    keywords = [
        # A
        'ACTION', 'ADD', 'ALL', 'ALTER', 'ANALYSE', 'ANALYZE', 'AND', 'ANY', 'ARRAY', 'AS', 'ASC', 'ASYMMETRIC',
        'AUTO_INCREMENT',
        # B
        'BDB', 'BERKELEYDB', 'BETWEEN', 'BIGINT', 'BINARY', 'BIT', 'BLOB', 'BOTH', 'BTREE', 'BY',
        # C
        'CASCADE', 'CASE', 'CAST', 'CHANGE', 'CHAR', 'CHARACTER', 'CHECK', 'COLLATE', 'COLUMN', 'COLUMNS', 'CONSTRAINT',
        'CREATE', 'CROSS', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_ROLE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP',
        'CURRENT_USER',
        # D
        'DATABASE', 'DATABASES', 'DATE', 'DAY_HOUR', 'DAY_MINUTE', 'DAY_SECOND', 'DEC', 'DECIMAL', 'DEFAULT',
        'DEFERRABLE', 'DELAYED', 'DELETE', 'DESC', 'DESCRIBE', 'DISTINCT', 'DISTINCTROW', 'DIV', 'DO', 'DOUBLE', 'DROP',
        # E
        'ELSE', 'ENCLOSED', 'END', 'ENUM', 'ERRORS', 'ESCAPED', 'EXCEPT', 'EXISTS', 'EXPLAIN',
        # F
        'FALSE', 'FETCH', 'FIELDS', 'FLOAT', 'FOR', 'FORCE', 'FOREIGN', 'FROM', 'FULLTEXT', 'FUNCTION',
        # G
        'GEOMETRY', 'GRANT', 'GROUP',
        # H
        'HASH', 'HAVING', 'HELP', 'HIGH_PRIORITY', 'HOUR_MINUTE', 'HOUR_SECOND',
        # I
        'IF', 'IGNORE', 'ILIKE', 'IN', 'INDEX', 'INFILE', 'INITIALLY', 'INNER', 'INNODB', 'INSERT', 'INT', 'INTEGER',
        'INTERSECT', 'INTERVAL', 'INTO', 'IS', 'ISNULL',
        # J
        'JOIN',
        # K
        'KEY', 'KEYS', 'KILL',
        # L
        'LATERAL', 'LEADING', 'LEFT', 'LIKE', 'LIMIT', 'LINES', 'LOAD', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCK', 'LONG',
        'LONGBLOB', 'LONGTEXT', 'LOW_PRIORITY',
        # M
        'MASTER_SERVER_ID', 'MATCH', 'MEDIUMBLOB', 'MEDIUMINT', 'MEDIUMTEXT', 'MIDDLEINT', 'MINUTE_SECOND', 'MOD',
        'MRG_MYISAM',
        # N
        'NATURAL', 'NEW', 'NO', 'NOT', 'NULL', 'NUMERIC',
        # O
        'OFF', 'OFFSET', 'OLD', 'ON', 'ONLY', 'OPTIMIZE', 'OPTION', 'OPTIONALLY', 'OR', 'ORDER', 'OUTER', 'OUTFILE',
        'OVERLAPS',
        # P
        'PLACING', 'PRECISION', 'PRIMARY', 'PRIVILEGES', 'PROCEDURE', 'PURGE',
        # Q
        # R
        'READ', 'REAL', 'REFERENCES', 'REGEXP', 'RENAME', 'REPLACE', 'REQUIRE', 'RESTRICT', 'RETURNING', 'RETURNS',
        'REVOKE', 'RIGHT', 'RLIKE', 'RTREE',
        # S
        'SELECT', 'SESSION_USER', 'SET', 'SHOW', 'SIMILAR', 'SMALLINT', 'SOME', 'SONAME', 'SPATIAL', 'SQL_BIG_RESULT',
        'SQL_CALC_FOUND_ROWS', 'SQL_SMALL_RESULT', 'SSL', 'STARTING', 'STRAIGHT_JOIN', 'STRIPED', 'SYMMETRIC',
        # T
        'TABLE', 'TABLES', 'TERMINATED', 'TEXT', 'THEN', 'TIME', 'TIMESTAMP', 'TINYBLOB', 'TINYINT', 'TINYTEXT', 'TO',
        'TRAILING', 'TRUE', 'TYPES',
        # U
        'UNION', 'UNIQUE', 'UNLOCK', 'UNSIGNED', 'UPDATE', 'USAGE', 'USE', 'USER', 'USER_RESOURCES', 'USING',
        # V
        'VALUES', 'VARBINARY', 'VARCHAR', 'VARCHARACTER', 'VARIADIC', 'VARYING', 'VERBOSE',
        # W
        'WARNINGS', 'WHEN', 'WHERE', 'WINDOW', 'WITH', 'WRITE',
        # X
        'XOR',
        # Y
        'YEAR_MONTH',
        # Z
        'ZEROFILL',
    ]

    operators = [
        '+', '-', '*', '/', '%', '<', '>', '=', '!=', '>=', '<=', '!<', '!>', '<>', '!!=', '!~', r'\|\|'
    ]

    braces = [r'\{', r'\}', r'\(', r'\)', r'\[', r'\]']

    def __init__(self, document, style):
        """
        Add syntax highlighter to editor text
        :param document: content of editor
        :param style: syntax highlighter styles
        """
        QSyntaxHighlighter.__init__(self, document)

        rules = []

        # Keyword, operator and brace rules
        rules += [(r'\b%s\b' % w, 0, style['keyword']) for w in CodePainter.keywords]
        rules += [(r'%s' % o, 0, style['operator']) for o in CodePainter.operators]
        rules += [(r'%s' % b, 0, style['brace']) for b in CodePainter.braces]

        # Other rules
        rules += [
            # Numeric values
            (r'\b[+-]?[0-9]+[lL]?\b', 0, style['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, style['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, style['numbers']),
            # Double-Quote String
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, style['string']),
            # Single-Quote String
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, style['string']),
            # Single line Comment
            (r'\-\- [^\n]*', 0, style['comment']),
        ]

        self.rules = [(QRegExp(pattern, cs=Qt.CaseInsensitive), index, fmt) for (pattern, index, fmt) in rules]

    def highlightBlock(self, text):
        """
        This functions paints all colors on editor text according to rules
        :param text: object of QTextBlock class
        :return: None
        """
        for exp, nth, fmt in self.rules:
            index = exp.indexIn(text, 0)

            while index >= 0:
                index = exp.pos(nth)
                length = len(exp.cap(nth))
                self.setFormat(index, length, fmt)
                index = exp.indexIn(text, index+length)

            self.setCurrentBlockState(0)
