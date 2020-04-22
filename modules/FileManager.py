import hashlib


class FileManager:
    """
    FileManger class keeps track of current file opened in editor
    :param string: content of editor
    :param location: path of current file
    """
    def __init__(self, string='', location=None):
        self.hash = None
        self.location = None
        self.reset(string, location)

    def reset(self, string='', location=None):
        """
        When opening new empty file in editor
        :param string: content of editor
        :param location: location of file
        :return: None
        """
        self.hash = hashlib.md5(string.encode()).hexdigest()
        self.location = location

    def set_hash(self, string):
        """
        Used to calculate MD5 hash of given string
        :param string: content of editor
        :return: None
        """
        self.hash = hashlib.md5(string.encode()).hexdigest()

    def set_location(self, location):
        """
        Used to update location of currently opened file
        :param location: Path where file reside
        :return: None
        """
        self.location = location

    def compare_hash(self, string):
        """
        Compare hash of given string with hash saved in class
        :param string: content of editor
        :return: True if hash matches else False
        """
        return True if self.hash == hashlib.md5(string.encode()).hexdigest() else False
