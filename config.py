from src.models.server import Server


class Config(object):
    DEBUG = False

    # Database configs
    DATABASE_URI = "mongodb://127.0.0.1:27017"
    DATABASE_NAME = "minecraft_logger"

    # Servers to log
    # Example with 2 Servers added
    '''
    LOGGING_SERVERS = [Server(name='Fighting Server', domain='play.server.com', port=25565),
                       Server(name='Testing Server', domain='test.server.com', port=25565)]
    '''
    LOGGING_SERVERS = [Server(name='Bonecrack', domain='connect.bonecrack.com', port=25565),
                       Server(name='Nationcraft', domain='play.nationmc.net', port=25565)]
