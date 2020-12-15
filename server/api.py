from flask import (Blueprint, jsonify, session, request)
from flask_cors import CORS
from .helper import *
import json

api = Blueprint("api", __name__)
CORS(api)



@api.route("/mentor/signup", methods=["POST"])
def mentor_signup():
    """ Adds new user to User table and new mentor to mentor table """
    
    form_data = request.get_json()
    new_user = create_user(form_data, "mentor")

    new_company = form_data["company"]
    new_knowledge = form_data["knowledge"]
    new_mentor = Mentor(user_id=new_user.id, company=new_company, knowledge=new_knowledge)
    
    db.session.add(new_mentor)
    db.session.commit()

  
    return jsonify({"success":True, "user_id" : new_user.id}), 200
        
@api.route("/mentee/signup", methods=["POST"])
def mentee_signup():
    """ Adds new user to User table and new mentee to mentor table """

    form_data = request.get_json()
    new_user = create_user(form_data, "mentee")  

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
    
    if email == user.email:
        if password == user.password:

            return jsonify({"success":True, "user_id" : user.id},), 200
        else:
            return jsonify({"message": "Incorrect password", "user_id": ""}), 401
    else:
        return jsonify({"message": "Incorrect email"}), 401

@api.route("/matching", methods=["POST"])
def matching():
    """Finds a match mentor/mentee based on experience/interests and different ethnicity"""
    form_data = request.get_json()
    user_id = form_data["user_id"]

    if user_id != None:
        user = User.query.filter_by(id=user_id).first()
    else:
        return jsonify({"message":"failed"}), 401
        
    if user.ment_type == "mentor":
        mentor = db.session.query(Mentor).filter_by(user_id=user_id).first()
        user_mentee = db.session.query(User).join(Mentee).filter(User.ethnic_background != user.ethnic_background, Mentee.need_help == mentor.knowledge, Mentee.mentor == None).first()

        return jsonify({"success":True,  
                        "user_id":user_mentee.id,
                        "user_name":user_mentee.name,}), 200 

    if user.ment_type == "mentee":
        mentee = db.session.query(Mentee).filter_by(user_id=user_id).first()
        user_mentor = db.session.query(User).join(Mentor).filter(User.ethnic_background != user.ethnic_background, Mentor.knowledge == mentee.need_help, Mentor.mentee == None).first()

        return jsonify({"success":True, 
                        "user_id":user_mentor.id,
                        "user_name":user_mentor.name,}), 200

@api.route("/display-user-info", methods=["POST"])
def display_user_info():
    "Returns user information to display user profile"
    form_data = request.get_json()
    user_id = form_data["user_id"]
    user = User.query.filter_by(id=user_id).first()

    if user.ment_type == "mentor":

        mentor = Mentor.query.filter_by(user_id=user_id)
        return jsonify({"success":True,
                        "user_id":user.id,
                        "name":user.name,
                        "phone":user.phone_number,
                        "gender":user.gender,
                        "ethnic_background": user.ethnic_background,
                        "experience": user.experience,
                        "link": user.link,
                        "about_me": user.about_me,
                        "ment_type": user.ment_type,
                        "company": mentor.company,
                        "knowledge": mentor.knowledge}), 200

    else:
        mentee = Mentee.query.filter_by(user_id=user_id).first()

        return jsonify({"success":True,
                        "user_id":user.id,
                        "name":user.name,
                        "phone":user.phone_number,
                        "gender":user.gender,
                        "ethnic_background": user.ethnic_background,
                        "experience": user.experience,
                        "link": user.link,
                        "about_me": user.about_me,
                        "ment_type": user.ment_type,
                        "need_help": mentee.need_help}), 200
