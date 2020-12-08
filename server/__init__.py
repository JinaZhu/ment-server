from flask import Flask
import os

from .extensions import db, guard
from .api import api
from .commands import create_tables, seed_db

def create_app(config_file="settings.py"):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)
    db.init_app(app)
    guard.init_app(app, User)

    app.register_blueprint(api)

    app.cli.add_command(create_tables)

    app.cli.add_command(seed_db)
    

    return app
    
