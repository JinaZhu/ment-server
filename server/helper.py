from .model import User
from .extensions import db, guard

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
    
    #check to see if user(email) exists
    if db.session.query(User).filter_by(email=new_email).count() < 1:
        try:
            new_user = User(email=new_email,
                            password=guard.hash_password(new_password),
                            roles='user',
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
            print('successfully added user')
        except:
            return "There was a problem signin up", 400
        
        user = guard.authenticate(User.email, User.password)
        res = {'access_toke': guard.encode_jwt_token(user)}

        return res, 200
    
    else:
        return "That user already exists", 400