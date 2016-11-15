from flask import Flask, render_template, redirect, url_for
from config import Config
app = Flask(__name__)
app.config.from_object(Config)
from datetime import datetime, timedelta
from src.models.session import Session


date = datetime.utcnow()
new = date.strftime('%Y-%m-%d %H:%M:%S')
print(new)
print(type(new))


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


@app.route('/player_log')
@app.route('/player_log/<dif>')
def player_log(dif=None):
    if dif is not None:
        now = datetime.utcnow()
        client = datetime(year=now.year, month=now.month, day=now.day, hour=int(dif), minute=now.minute, second=now.second,
                          microsecond=now.microsecond)
        hour = now - client
        print(type(hour.total_seconds()))
        return redirect(url_for('player_log_latest', sec=hour.total_seconds()))
    return render_template('get_date.html',
                           dt=datetime.utcnow())


@app.route('/player_log/latest')
@app.route('/player_log/<sec>/latest')
def player_log_latest(sec=None):
    if sec is None:
        redirect(url_for('player_log'))
    latest = Session.get_latest()
    dif = timedelta(seconds=float(sec))
    return render_template('player_log.html',
                           sessions=latest,
                           dif=dif)
