from datetime import datetime
import os
from twilio.rest import Client
from flask import Flask
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from gardenhelper.db import get_db
from gardenhelper.gardener import water_plants
from gardenhelper import api_keys


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'gardenhelper.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import gardener
    app.register_blueprint(gardener.bp)
    app.add_url_rule('/', endpoint='index')

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    return app


def send_reminders():
    db = get_db()
    users = db.execute(
        'SELECT * FROM user WHERE reminder = ?', (True,)
    ).fetchall()
    for user in users:
        send_alert = water_plants(user)
        if send_alert:
            account_sid = os.environ[api_keys.twilio_sid]
            auth_token = os.environ[api_keys.twilio_token]
            client = Client(account_sid, auth_token)

            message = client.messages \
                            .create(
                                body="Hello, this is Garden Helper with a friendly reminder to water your plants! "
                                     "Afterwards, please log in to confirm watering and update your plant data."
                                     "Doing this will help improve our predictions so that future alerts are as accurate"
                                     "as possible.",
                                from_=api_keys.twilio_number,
                                to="+1"+user['phone']
                            )
            print(message.sid)


