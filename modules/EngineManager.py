import re

from Engines.MySQLEngine import MySQLEngine
from logger import log


class EngineManager:
    def __init__(self, profiler, result_table):
        """
        Engine Identifier
        :param profiler: object of Profiler class
        """
        self.log = log.getLogger(self.__class__.__name__)
        self.profiler = profiler
        self.resultTable = result_table

        self.engines = dict()

    def parse(self, xsql):
        """
        parse give XSQL
        :param xsql: query need to execute
        :return: None
        """
        xsql = xsql.replace('\n', ' ')

        # Identify profile from given XSQL
        profiles = [profile.lower() for profile in re.findall(r'@.+?:', xsql, re.IGNORECASE)]
        self.log.info('Query profile(s): {}'.format(profiles))

        if len(set(profiles)) > 1:
            # Currently support only single profile in given query
            #       [FUTURE SCOOP]: if no profile given select default profile.
            self.log.error('With current version we only support single profile query')
        elif len(set(profiles)) == 1:
            xsql = xsql.replace(profiles[0], '')
            print(">:" + xsql + ":<")
            profile_name = (profiles[0][1:-1]).lower()
            try:
                # TODO: 2. Check that engine already exists in self.engines if not create one and add it
                if profile_name in self.engines.keys():
                    # TODO 2.1 : Use existing engine to run query
                    self.executeEngine(profile_name, xsql)
                else:
                    # Check of profile exists in profiler
                    self.log.info(profile_name)
                    profile = self.profiler.getProfile(profile_name)
                    if profile:
                        self.log.info(self.engines)
                        self.createEngine(profile)
                        self.log.info(self.engines)
                        self.executeEngine(profile_name, xsql)
                    else:
                        self.log.error('Wrong Profile given, Unable to execute query')
            except Exception as e:
                import sys, traceback
                self.log.error(traceback.print_tb(sys.exc_info()[2]))
        else:
            self.log.error('Invalid query')

    def executeEngine(self, profile_name, xsql):
        engine = self.engines[profile_name]
        if engine.sql(xsql):
            engine.feed()

    def createEngine(self, profile):
        profile_type = profile.type
        engine = None
        if profile_type.lower() == 'mysql':
            engine = MySQLEngine(profile, self.resultTable)
            engine.connect()
        # Add to engines list
        if engine:
            self.engines[profile.profile] = engine
