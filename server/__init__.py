from flask import Flask
import os

from .extensions import db 
from .api import api
from .commands import create_tables

def create_app(config_file="settings.py"):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)
    db.init_app(app)

    app.register_blueprint(api)

    app.cli.add_command(create_tables)

    return app
    