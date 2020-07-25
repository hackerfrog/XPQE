from pylatex import *
from pylatex.utils import bold


class PdfMaker:
    def __init__(self, context):
        """
        Make Export PDF file
        :param context: shared properties in application
        """
        self.context = context
        self.document = None

        self.create()

    def create(self):
        """
        Create LaTex code which will be used to generate PDF
        :return: None
        """
        self.document = Document(geometry_options={
            "margin": "0.3in"
        })

        self.document.preamble.append(Command('title', 'XPQE PDF Export'))
        self.document.preamble.append(Command('author', ''))
        self.document.preamble.append(Command('date', NoEscape(r'\today')))
        self.document.append(NoEscape(r'\maketitle'))

        # self.document.append(NoEscape(r'\tableofcontents'))
        # self.document.append(NoEscape(r'\newpage'))

        with self.document.create(Section('Server Info')) as server_info:
            with server_info.create(Tabu('||X|X||')) as table:
                table.add_hline()
                table.add_row(['Server', self.context.xpqe['execute.server']])
                table.add_hline()
                table.add_row(['Host', self.context.xpqe['execute.host']])
                table.add_hline()
                table.add_row(['Execution Timestamp', self.context.xpqe['execute.timestamp']])
                table.add_hline()

        with self.document.create(Section('XSQL Query')) as xsql:
            xsql.append(Command('texttt', self.context.xpqe['execute.xsql']))

        with self.document.create(Section('SQL Query')) as xsql:
            xsql.append(Command('texttt', self.context.xpqe['execute.sql']))

        col_names = self.context.xpqe['execute.header']

        with self.document.create(Section('Result Table')) as result:
            with result.create(LongTabu('|' + '|'.join(['X'] * len(col_names)) + '|')) as table:
                table.add_hline()
                table.add_row(col_names, mapper=[bold])
                for row in self.context.xpqe['execute.result']:
                    # cells = row.items()
                    table.add_hline()
                    table.add_row(['' if cell is None else cell for cell in row])
                table.add_hline()

    def generate_pdf(self, file_path):
        """
        Save PDF file to given location
        :param file_path: file location
        :return: None
        """
        file_path = '.'.join(file_path.split('.')[:-1])
        self.document.generate_pdf(file_path, compiler='pdfLaTeX')
