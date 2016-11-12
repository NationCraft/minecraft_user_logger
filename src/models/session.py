from uuid import uuid4
from src.database import Database


class Session(object):
    COLLECTION_NAME = 'sessions'

    def __init__(self, player_name, server_name, login, logout=None, session_length=None, _id=None):
        self.player_name = player_name
        self.server_name = server_name
        self.login = login
        self.logout = logout
        self.session_length = session_length
        self._id = _id if _id is not None else uuid4().hex

    def dict(self):
        return {
            'player_name': self.player_name,
            'server_name': self.server_name,
            'login': self.login,
            'logout': self.logout,
            'session_length': self.session_length,
            '_id': self._id
        }

    def save_to_mongo(self):
        Database.insert(Session.COLLECTION_NAME, self.dict())

    def update_by_id(self):
        Database.update(Session.COLLECTION_NAME, {'_id': self._id}, self.dict())

    @classmethod
    def get_by_login(cls, login):
        return cls(**Database.find_one(Session.COLLECTION_NAME, {'login': login}))

    @classmethod
    def get_by_logout(cls, logout, server_name):
        return [cls(**session) for session in Database.find(Session.COLLECTION_NAME, {'logout': logout, 'server_name': server_name})]

    @classmethod
    def get_all(cls):
        return [cls(**session) for session in Database.find(Session.COLLECTION_NAME, {})]
