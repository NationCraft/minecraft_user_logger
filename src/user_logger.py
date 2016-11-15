from flask import Flask, render_template, redirect, url_for
from config import Config
app = Flask(__name__)
app.config.from_object(Config)
from datetime import datetime, timedelta
from src.models.session import Session
from src.models.user import User


@app.route('/')
def index():
    servers = []
    for server in app.config['LOGGING_SERVERS']:
        server.get_mc_data()
        servers.append(server)
    return render_template('main.html',
                           servers=servers,
                           dt=datetime.utcnow(),
                           test='Hello World')


@app.route('/player_log/')
@app.route('/player_log/<dif>')
def player_log(dif=None):
    if dif is not None:
        dif = int(dif) * 60
        return redirect(url_for('player_log_latest', sec=dif, quantity='latest', server='all', player='all'))
    return render_template('get_date.html',
                           dt=datetime.utcnow())


@app.route('/player_log/<sec>/<quantity>/<server>/<player>/')
def player_log_latest(sec=None, quantity='latest', server='all', player='all'):
    if sec is None:
        return redirect(url_for('player_log'))

    sessions = Session.get_latest(quantity=quantity, server=server, player=player)

    dif = timedelta(seconds=int(sec))
    server_list = app.config['LOGGING_SERVERS']
    player_list = User.get_all()
    return render_template('player_log.html',
                           sessions=sessions,
                           quantity=quantity,
                           server=server,
                           player=player,
                           server_list=server_list,
                           player_list=player_list,
                           sec=sec,
                           dif=dif)
