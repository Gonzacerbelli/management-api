from flask import current_app as app
from flask import request, Response
from sqlalchemy import or_, and_
import jwt
import json
import time

from database import db_session, Users
from config import get_env_vars


@app.route("/signup", methods=["POST"])
def signup():
    try:
        response = None

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = Users.query.filter(
            or_(Users.username == username, Users.email == email)).first()

        if (existing_user):
            response = Response('User with username {} or email {} already exists'.format(
                username, email), status=409, mimetype='application/json')
        else:
            user = Users(email=email, password=password, username=username)

            db_session.add(user)
            db_session.commit()

            user_registered = Users.query.filter(
                or_(Users.username == username, Users.email == email)).first()

            response = Response('User with username {} and email {} created successfully'.format(
                user_registered.username, user_registered.email), status=201, mimetype='application/json')

        return response

    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')


@app.route("/signin", methods=["POST"])
def signin():
    try:
        response = None

        username = request.form.get("username")
        password = request.form.get("password")

        existing_user = Users.query.filter(
            and_(Users.username == username, Users.password == password)).first()

        if (existing_user):
            access_token = jwt.encode({
                "exp": int(time.time()+3600),
                "email": existing_user.email,
                "username": existing_user.username
            }, get_env_vars("JWT_PRIVATE_KEY"), algorithm='RS256')

            response = Response(json.dumps(
                {"access_token": access_token, "type": "Bearer"}), status=200, mimetype='application/json')
        else:
            response = Response('Invalid credentials or non-existent user',
                                status=401, mimetype='application/json')

        return response

    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')