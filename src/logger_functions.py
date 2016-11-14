from mcstatus import MinecraftServer


def get_loggedin_users(mc_server, port):
    print('server {} port {}'.format(mc_server, port))
    mc = MinecraftServer(mc_server, port)
    query = mc.query()
    return query.players.names


def exist_in_mc(session_player, online_list):
    for p in online_list:
        if p['username'] == session_player.player_name:
            return True
    return False


def exist_in_mongo(online_player, sessions):
    for session in sessions:
        if session.player_name == online_player['username']:
            return True
    return False
