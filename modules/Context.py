# Custom Imports
from modules.Settings import Settings
from logger import log


class Context:
    def __init__(self):
        """
        Context class to keep track of all shared properties
        """
        self.log = log.getLogger(self.__class__.__name__)

        self.settings = Settings()
        self.log.info('Settings File Path: {}'.format(self.settings.fileName()))

        self.editor = dict()
        self.server = dict()
        self.window = dict()
        self.xpqe = dict()

        self.loadSettings()

    def loadSettings(self):
        """
        Fetch all settings into application
        :return: None
        """
        # EDITOR
        self.editor['autoClosing.brackets'] = self.settings.value('editor.autoClosing.brackets', 'Always', str)
        self.editor['autoClosing.quotes'] = self.settings.value('editor.autoClosing.quotes', 'Always', str)
        self.editor['editorToResultRatio'] = self.settings.value('editor.editorToResultRatio', [50, 50], int)
        self.editor['font.family'] = self.settings.value('editor.font.family', 'Courier New', str)
        self.editor['font.pointSize'] = self.settings.value('editor.font.pointSize', 9, int)
        self.editor['font.stretch'] = self.settings.value('editor.font.stretch', 0, int)
        self.editor['font.weight'] = self.settings.value('editor.font.weight', 50, int)
        self.editor['result.renderCount'] = self.settings.value('editor.result.renderCount', 1000, int)

        # SERVER
        self.server['autoCommit'] = self.settings.value('server.autoCommit', False, bool)

        # WINDOW
        self.window['maximized'] = self.settings.value('window.maximized', False, bool)
        self.window['position'] = self.settings.value('window.position', [0, 0], int)
        self.window['size'] = self.settings.value('window.size', [480, 320], int)

        # XPQE
        self.xpqe['execute.host'] = None
        self.xpqe['execute.header'] = None
        self.xpqe['execute.result'] = None
        self.xpqe['execute.server'] = None
        self.xpqe['execute.sql'] = None
        self.xpqe['execute.timestamp'] = None
        self.xpqe['execute.xsql'] = None

    def saveSettings(self):
        """
        Save settings properties
        :return: None
        """
        # EDITOR
        self.settings.setValue('editor.autoClosing.brackets', self.editor['autoClosing.brackets'])
        self.settings.setValue('editor.autoClosing.quotes', self.editor['autoClosing.quotes'])
        self.settings.setValue('editor.editorToResultRatio', self.editor['editorToResultRatio'])
        self.settings.setValue('editor.font.family', self.editor['font.family'])
        self.settings.setValue('editor.font.pointSize', self.editor['font.pointSize'])
        self.settings.setValue('editor.font.stretch', self.editor['font.stretch'])
        self.settings.setValue('editor.font.weight', self.editor['font.weight'])
        self.settings.setValue('editor.result.renderCount', self.editor['result.renderCount'])

        # SERVER
        self.settings.setValue('server.autoCommit', self.server['autoCommit'])

        # WINDOW
        self.settings.setValue('window.maximized', self.window['maximized'])
        self.settings.setValue('window.position', self.window['position'])
        self.settings.setValue('window.size', self.window['size'])
