from .extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=True)
    gender = db.Column(db.String, nullable=False)
    ethnic_background = db.Column(db.String, nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    link = db.Column(db.String, nullable=True)
    about_me = db.Column(db.String, nullable=False)
    ment_type = db.Column(db.String, nullable=False)


    def __repr__(self):
        return f"<users={self.email}>"

class Mentor(db.Model):
    __tablename__ = 'mentors'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    company = db.Column(db.String, nullable=True)
    knowledge = db.Column(db.String, nullable=False)

    mentee_id = db.Column(db.Integer, db.ForeignKey('mentees.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    #relationship
    user = db.relationship("User", foreign_keys=[user_id])
    mentee = db.relationship("Mentee", backref='mentor')

    def __repr__(self):
        return f"<mentors={self.mentor_id}>"

class Mentee(db.Model):
    __tablename__ = 'mentees'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    need_help = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    #relationship
    user = db.relationship("User", foreign_keys=[user_id])

    def __repr__(self):
        return f"<mentees={self.mentee_id}>"