from .model import User, Mentor, Mentee
from .extensions import db, guard

from faker import Faker
import random

ethnicity = ['asian', 'black/african-american', 'caucasian', 'indigenous people', 'hispanic/latinx', 'native-american', 'middle eastern/northern african', 'native hawaiian/ pacific islander']
genders = ['agender', 'genderfluid', 'genderqueer', 'female', 'male', 'genderqueer', 'gender non-conforming', 'non-binary', 'I chose not to disclose']
topics = ['backend', 'frontend', 'database', 'full-stack']
ment_types = ["mentee", "mentor"]


fake = Faker()


def populate_db():
    for i in range(101):
        new_user = User(
                        email=fake.email(),
                        password=guard.hash_password(fake.password()),
                        roles='user',
                        name=fake.name(),
                        phone_number=fake.phone_number(),
                        gender=random.choice(genders),
                        ethnic_background=random.choice(ethnicity),
                        experience=random.randint(2, 40),
                        link=f"linkedin.com/_________",
                        about_me=fake.text(),
                        ment_type=random.choice(ment_types)
        )
        db.session.add(new_user)
        db.session.commit()

        if new_user.ment_type == "mentor":
            new_mentor = Mentor(user_id=new_user.id, company=fake.bs(), knowledge=random.choice(topics))
            db.session.add(new_mentor)
            db.session.commit()
        
        elif new_user.ment_type == "mentee":
            new_mentee = Mentee(user_id=new_user.id, need_help=random.choice(topics))
            db.session.add(new_mentee)
            db.session.commit()