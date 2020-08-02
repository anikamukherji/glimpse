from __future__ import absolute_import

from flask import Flask

from flask_sqlalchemy import SQLAlchemy

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

    db.init_app(app)

    # blueprint for auth
    from main.v1.auth_handlers import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    # blueprint for user operations
    from main.v1.user_handlers import user as user_blueprint

    app.register_blueprint(user_blueprint)

    # blueprint for landing pages
    from main.v1.page_handlers import pages as pages_blueprint

    app.register_blueprint(pages_blueprint)

    # blueprint for chat room operations
    from main.v1.chat_room_handlers import chat_room as chat_room_blueprint

    app.register_blueprint(chat_room_blueprint)

    # blueprint for chat operationss
    from main.v1.chat_handlers import chat as chat_blueprint

    app.register_blueprint(chat_blueprint)

    return app
