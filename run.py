from src.user_logger import app
from src.logger import LoggerThread
from src.database import Database


def init_db():
    Database.initialize()


def start_logger_thread():
    logger = LoggerThread(1, 'Logger')
    logger.daemon = True
    logger.start()
    print('started logger thread')


init_db()
start_logger_thread()
app.run()
