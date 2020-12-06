from flask import (Blueprint, jsonify, session, request)
from flask_cors import CORS
from .helper import *
import json

api = Blueprint("api", __name__)

CORS(api)


@api.route('/mentor/signup', methods=['POST'])
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
    
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}
        
@api.route('/mentee/signup', methods=['POST'])
def mentee_signup():
    """ Adds new user to User table and new mentee to mentor table """

    form_data = request.get_json()
    new_user = create_user(form_data, "mentee")   

    # add mentee to Mentee table
    new_need_help = request.form.get("need_help")
    new_mentee = Mentee(user_id=new_user.id, need_help=new_need_help)
    db.session.add(new_mentee)
    db.session.commit()

    return 200

@api.route("/handle-login", methods=["POST"])
def handle_login():
    """ Logs in existent User """

    form_data = request.get_json()

    email = form_data['email']
    password = form_data["password"]

    user = User.query.filter_by(email=email).first()

    if password == user.password:
        session["logged_in_user"] = user
        return 200
    else:
        return "Incorrect email or password" 

@api.route("/matching")
def matching():
    #who's in session? Mentor or Mentee?
    user_id = session.get('user_id')
    user = User.query.filter_by(user_id)
    #add ment_type collumn to User table on db

    #if mentor:
        # query mentees where mentee.id is Null and mentor.ethnic_backgound != mentee.ethnic_background and 
        # mentor.knowledge == mentee.need_help 
        # select the first metee that meets those requirements
        # add mentee_id id to db 
        # return mentee
        
    if user.ment_type == "mentor":
        mentees = session.query(Mentee).filter()


    #if mentee:
        # query mentors where mentor.id is Null and mentee.ethnic_background != mentor.ethnic_backgound and 
        # mentee.need_help == mentor.knowledge
        # select the first metee that meets those requirements
        # add mentor_id to db 
        # return mentor
