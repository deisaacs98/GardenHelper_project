import os

from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import gardener
    app.register_blueprint(gardener.bp)
    #app.add_url_rule('/', endpoint='search')

    from . import plants
    app.register_blueprint(plants.bp)
    #app.add_url_rule('/', endpoint='search')

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    return app
