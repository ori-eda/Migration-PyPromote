import yaml

from PyPromote.Utilities import DB
from PyPromote.Utilities import PySecrets


class ReadFile:
    """
    Process incoming YAML file and return appropriate dictionary
    """
    def __init__(self, file: str):
        self.file = file
        self.pySecret = PySecrets()
        self.stream = open(self.file, 'r')
        self.dictionary = yaml.load(self.stream, Loader=yaml.FullLoader)
        self.db = DB()

    @property
    def username(self):
        return self.username

    @username.setter
    def username(self, username: str):
        self.username = username

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, password):
        self.password = password

    def read_section(self, section: str) -> dict or str:
        _username = None
        _password = None
        if section in ('Server', 'Source', 'Target'):
            _secret = self.dictionary[section]['Secret']
            if self.db.secret_exists(secret=_secret):
                del self.dictionary[section]['Secret']
                results = self.db.retrieve_secrets(secret=_secret)
                for result in results:
                    _username = self.pySecret.make_public(result.username)
                    _password = self.pySecret.make_public(result.password)
                self.dictionary[section]['user'] = _username
                self.dictionary[section]['password'] = _password
            return self.dictionary[section]
        elif section == 'Deployment':
            return str(self.dictionary[section])
        else:
            return self.dictionary['Deployments']
