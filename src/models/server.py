from uuid import uuid4
from mcstatus import MinecraftServer


class Server(object):
    COLLECTION_NAME = 'servers'

    def __init__(self, name, domain, port, _id=None):
        self.name = name
        self.domain = domain
        self.port = port
        self._id = _id if _id is not None else uuid4().hex

    def get_mc_data(self):
        mc = MinecraftServer(self.domain, self.port)
        try:
            self.server_online = True
            self.online_players = mc.status().players.online
            self.player_list = mc.query().players.names
        except Exception:
            self.server_online = False
            self.online_players = 0
            self.player_list = []
