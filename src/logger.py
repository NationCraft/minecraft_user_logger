import threading
import time
from datetime import datetime
from mcstatus import MinecraftServer
from pymongo import MongoClient
from src.user_logger import app
from src.models.session import Session


class LoggerThread(threading.Thread):

    def __init__(self, thread_id, name):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name

    def run(self):
        while True:
            for server in app.config['LOGGING_SERVERS']:
                try:
                    logged_in_users = LoggerThread.get_loggedin_users(server.name, server.port)
                except Exception as e:
                    print(e)

                sessions = Session.get_by_logout(None, server_name=server.name)


    @staticmethod
    def get_loggedin_users(mc_server, port):
        mc = MinecraftServer(mc_server, port)
        query = mc.query()
        return query.players.names

    @staticmethod
    def exist_in_mc(session_player, online_list):
        for p in online_list:
            if p['username'] == session_player.player_name:
                return True
        return False

    @staticmethod
    def exist_in_mongo(online_player, sessions):
        for session in sessions:
            if session.player_name == online_player['username']:
                return True
        return False
