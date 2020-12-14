from flask import (Blueprint, jsonify, request)
from flask_praetorian import auth_required, current_user
from flask_cors import CORS
from .extensions import db, guard
from .helper import create_user
from .model import User, Mentor, Mentee

api = Blueprint("api", __name__)
CORS(api)

@api.route("/mentor/signup", methods=["POST"])
def mentor_signup():
    """ Adds new user to User table and new mentor to mentor table """
    
    form_data = request.get_json()
    new_user = create_user(form_data, "mentor")
    # add new mentor to Mentor table
    new_company = form_data["company"]
    new_knowledge = form_data["knowledge"]
    new_mentor = Mentor(user_id=new_user.id, company=new_company, knowledge=new_knowledge)
    
    db.session.add(new_mentor)
    db.session.commit()

    #CREATE SESSION HERE
    # session['id'] = guard.current_user().id
    # session['email'] = guard.current_user().email

    return jsonify({"success": True, "user_id": new_user.id}), 200
        
@api.route("/mentee/signup", methods=["POST"])
def mentee_signup():
    """ Adds new user to User table and new mentee to mentor table """

    form_data = request.get_json()
    new_user = create_user(form_data, "mentee")
    # add mentee to Mentee table
    new_need_help = form_data["need_help"]
    new_mentee = Mentee(user_id=new_user.id, need_help=new_need_help)
    db.session.add(new_mentee)
    db.session.commit()

    #CREATE SESSION HERE

    return jsonify({"success": True, "user_id": new_user.id}), 200

@api.route("/login", methods=["POST"])
def handle_login():
    """ Logs in existent User """
    """
    Logs a user in by parsing a POST request containing user credentials and
    issuing a JWT token.
    .. example::
       $ curl http://localhost:5000/login -X POST \
         -d '{"username":"Walter","password":"calmerthanyouare"}'
    """
    form_data = request.get_json(force=True)

    email = form_data["email"]
    password = form_data["password"]

    # user = User.query.filter_by(email=email).first()
    user = guard.authenticate(email, password)
    token = guard.encode_jwt_token(user)
    print(token)

    #CREATE SESSION HERE
    
    # if password == user.password:

    #     return jsonify({"success":True, "user_id" : user.id},), 200
    # else:
    #     return jsonify({"message": "Incorrect email or password", "user_id": ""}), 401

    #return user id
    return (jsonify({'access_token': token}), 200)

@api.route('/open')
def open():
    return jsonify({'result': 'Hello'})

@api.route('/refresh', methods=['POST'])
def refresh():
    """
    Refreshes an existing JWT by creating a new one that is a copy of the old
    except that it has a refreshed access expiration.
    .. example::
    $ curl http://localhost:5000/api/refresh -X GET \
        -H "Authorization: Bearer <your_token>"
    """
    print('refresh request')
    old_token = request.get_data()
    new_token = guard.refresh_jwt_token(old_token)
    ret = {'access_token': new_token}

    return ret, 200

@api.route('/protected')
@auth_required
def protected():
    """
    A protected endpoint. The auth_required decorate will require a header
    containing a valid JWT
    .. example::
    $ curl http://loclahost:5000/api/protected -X GET \
        -H "Authorization: Bearer <your_token>"
    """
    return jsonify(message="protected endpoint (allowed user {})".format(
        current_user().email,))

@api.route("/matching", methods=["POST"])
def matching():

    form_data = request.get_json()
    user_id = form_data["user_id"]

    if user_id is not None:
        user = User.query.filter_by(id=user_id).first()
    else:
        return jsonify({"message": "failed"}), 401
        
    if user.ment_type == "mentor":
        mentor = db.session.query(Mentor).filter_by(user_id=user_id).first()
        user_mentee = db.session.query(User).join(Mentee).filter(User.ethnic_background != user.ethnic_background, Mentee.need_help == mentor.knowledge, Mentee.mentor == None).first()

        return jsonify({"success": True,
                        "user_id": user_mentee.id,
                        "user_name": user_mentee.name,
                        "user_phone": user_mentee.phone_number,
                        "user_gender": user_mentee.gender,
                        "user_ethnic_background": user_mentee.ethnic_background,
                        "user_experience": user_mentee.experience,
                        "user_link": user_mentee.link,
                        "user_about_me": user_mentee.about_me}), 200

    if user.ment_type == "mentee":
        mentee = db.session.query(Mentee).filter_by(user_id=user_id).first()
        user_mentor = db.session.query(User).join(Mentor).filter(User.ethnic_background != user.ethnic_background, Mentor.knowledge == mentee.need_help, Mentor.mentee == None).first()

        return jsonify({"success": True,
                        "match": user_mentor.id,
                        "user_name": user_mentor.name,
                        "user_phone": user_mentor.phone_number,
                        "user_gender": user_mentor.gender,
                        "user_ethnic_background": user_mentor.ethnic_background,
                        "user_experience": user_mentor.experience,
                        "user_link": user_mentor.link,
                        "user_about_me": user_mentor.about_me}), 200