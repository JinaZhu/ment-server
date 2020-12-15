import click
from flask.cli import with_appcontext
from .extensions import db, guard
from .seed import populate_db
from .model import User

@click.command(name="create_tables")
@with_appcontext
def create_tables():
    db.create_all()

@click.command(name="seed_db")
@with_appcontext
def seed_db():
    populate_db()

@click.command(name='create_users')
@with_appcontext
def create_users():
    one = User(email='one@gmail.com',
        password=guard.hash_password('one'),
        roles='user',
        name='User One',
        phone_number='808.555.5555',
        gender='female',
        ethnic_background='native-american',
        experience='8',
        link='linkedin.com/_________',
        about_me='Brother agreement my. Think expert office guess news least weight.',
        ment_type='mentor')
    
    two = User(email='two@gmail.com',
            password=guard.hash_password('two'),
            roles='user',
            name='User Two',
            phone_number='808.555.5555',
            gender='male',
            ethnic_background='caucasian',
            experience='2',
            link='linkedin.com/_________',
            about_me='Discussion court tough least body worry. Deep in cup individual thought admit into.',
            ment_type='mentee')
    
    db.session.add_all([one, two])
    db.session.commit()