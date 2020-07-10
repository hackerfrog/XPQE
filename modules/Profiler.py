from PyQt5.QtCore import QSettings

from logger import log


class Profile:
    def __init__(self, profile, profile_type, host=None, port=None, database=None, username=None, password=None):
        """
        Keeps all information of server
        :param profile: name of profile
        :param profile_type: type of server ex: MySQL
        :param host: server host name
        :param port: server port number
        :param database: database name in server
        :param username: server username
        :param password: server password
        """
        self.profile = profile.lower()
        self.type = profile_type
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password

    def __repr__(self):
        """
        String representation of Profile object
        :return: String
        """
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

    def getProfile(self, profile_name):
        """
        Get profile when profile name is passed
        :param profile_name: name of profile
        :return: Profile / None
        """
        if self.checkProfileName(profile_name=profile_name):
            for profile in self.list:
                if profile.profile == profile_name:
                    return profile
            return None
        else:
            return None

    def save(self):
        """
        Hard save all profiles into file
        :return: None
        """
        self.setValue('profiler', self.list)

    def addProfile(self, profile):
        """
        Add new profile to profiler
        :param profile: object of Profie which need to added
        :return: None
        """
        if not self.checkProfileName(profile=profile):
            self.list.append(profile)
            self.setValue('profiler', self.list)
            self.log.info('New profile added')
        else:
            self.log.error("Profile Name already exist")

    def editProfile(self, profile_name, profile):
        """
        Replace existing profile with given new profile object
        :param profile_name: name of profile to identify profile which need to replaced by given profile
        :param profile: Profile object which need to be replaced with existing profile
        :return: None
        """
        if self.checkProfileName(profile_name=profile_name):
            index = self.getProfileIndex(profile_name=profile_name)
            self.list[index] = profile
            self.setValue('profiler', self.list)
        else:
            self.log.error("Given profile/profile_name doesn't exist")

    def removeProfile(self, index):
        """
        Remove profile from given profile index
        :param index: index of profile in profiler
        :return: Boolean
        """
        if index < len(self.list):
            del self.list[index]
            self.setValue('profiler', self.list)
            return True
        else:
            self.log.error('Index out of range, Unable to remove profile')
            return False

    def getProfileIndex(self, profile=None, profile_name=None):
        """
        Get profile index of give profile object or profile name
        :param profile: object of Profile
        :param profile_name: name of Profile
        :return: int
        """
        if profile:
            return self.list.index(profile)
        elif profile_name:
            return [_profile.profile for _profile in self.list].index(profile_name)
        else:
            self.log.error("No Profile object or Profile Name is passed to compare")
            return -1

    def checkProfileName(self, profile=None, profile_name=None):
        """
        Check given profile or profile with profile name exist in Profiler
        :param profile: object of Profile
        :param profile_name: name of profile
        :return: Boolean
        """
        if profile:
            profile_name = profile.profile
        elif profile_name:
            profile_name = profile_name
        else:
            self.log.error("No Profile object or Profile Name is passed to compare")
            return False

        if profile_name in [profile.profile for profile in self.list]:
            return True
        else:
            return False
