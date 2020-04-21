from logger import log


class EngineManager:
    """
    Engine Identifier
    """
    def __init__(self):
        """
        class set-up
        """
        self.log = log.getLogger(self.__class__.__name__)
        self.engines = dict()
        self.profile = None

    def parse(self, xsql):
        """
        parse give XSQL
        :param xsql: query need to execute
        :return: None
        """
        # TODO: 1. Identify profile from given XSQL
        #               Currently support only single profile in given query
        #               [FUTURE SCOOP]: if no profile given select default profile.

        # TODO: 2. Check that engine already exists in self.engines if not create one and add it
        # TODO: 3. Remove Profile identifier from XSQL and run on engine
        pass
