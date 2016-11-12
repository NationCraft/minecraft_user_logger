from uuid import uuid4


class Server(object):
    COLLECTION_NAME = 'servers'

    def __init__(self, name, domain, port, _id=None):
        self.name = name
        self.domain = domain
        self.port = port
        self._id = _id if _id is not None else uuid4().hex
