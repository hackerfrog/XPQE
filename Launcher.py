import sys

from functools import partial

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

# Custom Imports
from gui.CodeEditor import CodeEditor
from gui.ResultTable import ResultTable
from modules.CodePainter import CodePainter
from modules.Context import Context
from modules.EngineManager import EngineManager
from modules.FileManager import FileManager
from modules.Profiler import Profiler
from modules.trigger_func import *
from gui.Main import Main


# All style for syntax highlighter
STYLES = {
    'keyword': fmt('blue'),
    'operator': fmt('red', 'bold'),
    'brace': fmt('brown'),
    'string': fmt('magenta'),
    'comment': fmt('darkGreen', 'italic'),
    'numbers': fmt('brown'),
}


if __name__ == '__main__':
    log.getLogger(__name__)
    log.info('STARTED')
    app = QApplication(sys.argv)

    ############################################################################
    # CONTEXT
    context = Context()

    ############################################################################
    # RESULT TABLE
    result_table = ResultTable()

    ############################################################################
    # Modules Init
    profiler = Profiler()
    engine_manager = EngineManager(context, profiler, result_table)
    file_manager = FileManager()

    ############################################################################
    # EDITOR
    editor = CodeEditor(context)
    highlight = CodePainter(editor.document(), STYLES)

    window = Main(context, app, editor, engine_manager, file_manager, profiler, result_table)
    if context.window['maximized']:
        window.showMaximized()
    else:
        window.show()

    ############################################################################
    # END
    sys.exit(app.exec_())
