from PyQt5.QtCore import QSettings

from logger import log


class Profile:
    def __init__(self, profile, profile_type, host=None, port=None, username=None, password=None):
        """
        Keeps all information of server
        :param profile: name of profile
        :param host: server host name
        :param port: server port number
        :param username: server username
        :param password: server password
        """
        self.profile = profile
        self.type = profile_type
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def __repr__(self):
        return 'Profile Object: {profile} @ {type}'.format(profile=self.profile, type=self.type)


class Profiler(QSettings):
    def __init__(self):
        """
        Store all profile in single file and manages
        """
        super().__init__('profiler.ini', QSettings.IniFormat)
        self.log = log.getLogger(self.__class__.__name__)

        self.setFallbacksEnabled(False)
        self.log.info(self.fileName())

        self.list = self.value('profiler', [], list)

    def addProfile(self, profile):
        if self.__checkProfileName(profile):
            self.list.append(profile)
            self.setValue('profiler', self.list)
            self.log.info('New profile added')
        else:
            self.log.error("Profile Name already exist")

    def removeProfile(self, index):
        if index < len(self.list):
            del self.list[index]
            self.setValue('profiler', self.list)
            return True
        else:
            self.log.error('Index out of range, Unable to remove profile')
            return False

    def __checkProfileName(self, profile):
        if profile.profile in [profile.profile for profile in self.list]:
            return False
        else:
            return True
