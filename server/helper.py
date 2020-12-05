from .model import User, Mentor, Mentee, db


def create_user(form_data, ment_type):
    """ helper function to add new user to User table """
    new_email = form_data['email']
    new_password = form_data['password']
    new_name = form_data['name']
    new_phone_number = form_data['phone_number']
    new_gender = form_data['gender']
    new_ethnic_background = form_data['ethnic_background']
    new_experience = form_data['experience']
    new_link = form_data['link']
    new_about_me = form_data['about_me']
    ment_type = ment_type


    new_user = User(email=new_email, 
                    password=new_password, 
                    name=new_name, 
                    phone_number=new_phone_number,
                    gender=new_gender,
                    ethnic_background=new_ethnic_background,
                    experience=new_experience,
                    link=new_link,
                    about_me=new_about_me,
                    ment_type=ment_type)
    db.session.add(new_user)
    db.session.commit()
    return new_user
