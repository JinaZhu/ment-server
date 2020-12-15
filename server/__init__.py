from flask import Flask

from .extensions import db, guard
from .api import api
from .commands import create_tables, seed_db
from .model import User

def create_app(config_file="settings.py"):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)
    app.config['JWT_ACCESS_LIFESPAN'] = {'hours': 24}
    app.config['JWT_REFRESH_LIFESPAN'] = {'days': 30}
    db.init_app(app)
    guard.init_app(app, User)

    app.register_blueprint(api)

    app.cli.add_command(create_tables)

    app.cli.add_command(seed_db)
    
    return app