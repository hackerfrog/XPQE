import re

from logger import log


class EngineManager:
    def __init__(self):
        """
        Engine Identifier
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
        # Identify profile from given XSQL
        profiles = [profile.lower() for profile in re.findall(r'@.+?\.', xsql, re.IGNORECASE)]
        self.log.info('Query profile(s): {}'.format(profiles))

        if len(set(profiles)) > 1:
            # Currently support only single profile in given query
            #       [FUTURE SCOOP]: if no profile given select default profile.
            self.log.error('With current version we only support single profile query')
        else:
            # TODO: 2. Check that engine already exists in self.engines if not create one and add it
            # TODO: 3. Remove Profile identifier from XSQL and run on engine
            pass
