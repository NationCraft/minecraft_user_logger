import threading
from time import sleep
from datetime import datetime
from mcstatus import MinecraftServer
from src.user_logger import app
from src.models.session import Session
from src.models.user import User


class LoggerThread(threading.Thread):

    def __init__(self, thread_id, name):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name

    def run(self):
        while True:
            for server in app.config['LOGGING_SERVERS']:
                logged_in_users = None
                try:
                    logged_in_users = LoggerThread.get_loggedin_users(server.domain, server.port)
                except Exception as e:
                    print('get_loggedin_users error:', e)
                sessions = Session.get_by_logout(server_name=server.name)

                # Updating and saving logout info
                if sessions:
                    for session in sessions:
                        if not LoggerThread.exist_in_mc(session, logged_in_users):
                            session.logout = datetime.utcnow()
                            length = session.logout - session.login
                            session.session_length = length.total_seconds()
                            session.update_by_id()
                # Saving new logged in user to database
                if logged_in_users:
                    for logged_in_user in logged_in_users:
                        if not LoggerThread.exist_in_mongo(logged_in_user, sessions):
                            now = datetime.utcnow()
                            new_session = Session(logged_in_user, server.name, now)
                            if not LoggerThread.user_exist(new_session.player_name):
                                new_user = User(new_session.player_name)
                                new_user.save_to_mongo()
                            new_session.save_to_mongo()

            sleep(60)

    @staticmethod
    def get_loggedin_users(mc_server, port):
        mc = MinecraftServer(mc_server, port)
        query = mc.query()
        return query.players.names

    @staticmethod
    def exist_in_mc(session_player, online_list):
        for p in online_list:
            if p == session_player.player_name:
                return True
        return False

    @staticmethod
    def exist_in_mongo(online_player, sessions):
        for session in sessions:
            if session.player_name == online_player:
                return True
        return False

    @staticmethod
    def user_exist(user):
        if user in User.get_usernames():
            return True
        else:
            return False
