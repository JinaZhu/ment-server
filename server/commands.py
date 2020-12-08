import click
from flask.cli import with_appcontext
from .extensions import db
from .model import User
from .seed import populate_db


@click.command(name="create_tables")
@with_appcontext
def create_tables():
    db.create_all()

@click.command(name="seed_db")
@with_appcontext
def seed_db():
    populate_db()