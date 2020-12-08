from .extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    hashed_password = db.Column(db.Text, nullable=False)
    name = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=True)
    gender = db.Column(db.String, nullable=False)
    ethnic_background = db.Column(db.String, nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    link = db.Column(db.String, nullable=True)
    about_me = db.Column(db.String, nullable=False)
    ment_type = db.Column(db.String, nullable=False)
    roles = db.Column(db.String)
    is_active = db.Column(db.Boolean, default=True, server_default="true")

    @property
    def identity(self):
        return self.id

    @property
    def rolenames(self):
        try:
            return self.roles.split(",")
        except Exception:
            return []

    @property
    def password(self):
        return self.hashed_password
    
    @classmethod
    def lookup(cls, email):
        return cls.query.filter_by(email=email).one_or_none()
    
    @classmethod
    def identify(cls, id):
        return cls.query.filter_by(id=id).one_or_none()
    
    def is_valid(self):
        return self.is_active

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