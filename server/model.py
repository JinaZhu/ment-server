from .extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String, nullable=False)
    ethnic_background = db.Column(db.String, nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    link = db.Column(db.String, nullable=True)
    about_me = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<users={self.email}>"

class Mentors(db.Model):
    __tablename__ = 'mentors'

    mentor_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    company = db.Column(db.String, nullable=True)
    knowledge = db.Column(db.String, nullable=False)
    mentee_id = db.Column(db.Integer, db.ForeignKey('mentees.mentee_id'))

    #relationship
    user_mentor = db.relationship("User", backref='mentor')
    mentee = db.relationship("Mentees", backref='mentor')

    def __repr__(self):
        return f"<mentors={self.mentor_id}>"

class Mentees(db.Model):
    __tablename__ = 'mentees'

    mentee_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    need_help = db.Column(db.String, nullable=False)
    mentor_id = db.Column(db.Integer, db.ForeignKey('mentors.mentor_id'))

    #relationship
    user_mentee = db.relationship("User", backref="mentee")

    def __repr__(self):
        return f"<mentees={self.mentee_id}>"