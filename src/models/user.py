from uuid import uuid4
from src.database import Database


class User(object):
    COLLECTION_NAME = 'users'

    def __init__(self, username, _id=None):
        self.username = username
        self._id = _id if _id is not None else uuid4().hex

    def dict(self):
        return {
            'username': self.username,
            '_id': self._id
        }

    def save_to_mongo(self):
        Database.insert(User.COLLECTION_NAME, self.dict())

    @classmethod
    def get_all(cls):
        return [cls(**user) for user in Database.find(User.COLLECTION_NAME, {})]

    @staticmethod
    def get_usernames():
        users = []
        for user in User.get_all():
            users.append(user.username)
        return users
