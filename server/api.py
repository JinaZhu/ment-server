from flask import (Blueprint, jsonify, session, request)
from flask_cors import CORS
from .helper import *
import json

api = Blueprint("api", __name__)
CORS(api)

api.secret_key = "ABC"


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
  
    return jsonify({"success":True, "user_id" : new_user.id}), 200, 
        
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

    return jsonify({"success":True, "user_id" : new_user.id}), 200

@api.route("/login", methods=["POST"])
def handle_login():
    """ Logs in existent User """

    form_data = request.get_json()

    email = form_data["email"]
    password = form_data["password"]

    user = User.query.filter_by(email=email).first()

    if password == user.password:

        return jsonify({"success":True, "user_id" : user.id},), 200
    else:
        return "Incorrect email or password" 

@api.route("/matching", methods=["POST"])
def matching():
    
    form_data = request.get_json()
    user_id = form_data["user_id"]

    if user_id != None:
        user = User.query.filter_by(id=user_id).first()
    else:
        return jsonify({"message":"failed"}), 401
        
    if user.ment_type == "mentor":
        mentor = db.session.query(Mentor).filter_by(user_id=user_id).first()
        user_mentee = db.session.query(User).join(Mentee).filter(User.ethnic_background != user.ethnic_background, Mentee.need_help == mentor.knowledge, Mentee.mentor == None).first()

        return jsonify({"success":True, "match":user_mentee.id}), 200 

    if user.ment_type == "mentee":
        mentee = db.session.query(Mentee).filter_by(user_id=user_id).first()
        user_mentor = db.session.query(User).join(Mentor).filter(User.ethnic_background != user.ethnic_background, Mentor.knowledge == mentee.need_help, Mentor.mentee == None).first()

        return jsonify({"success":True, "match":user_mentor.id}), 200

