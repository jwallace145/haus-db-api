import os

from flask import Flask

from database import db
from routes.auth.auth import auth_blueprint
from routes.songs.songs import songs_blueprint
from routes.users.users import users_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.getenv('APP_SETTINGS'))
    db.init_app(app)
    app.register_blueprint(auth_blueprint, url_prefix='/')
    app.register_blueprint(users_blueprint, url_prefix='/users')
    app.register_blueprint(songs_blueprint, url_prefix='/songs')
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
