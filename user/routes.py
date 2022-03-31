import json
import logging

from flask import request, jsonify

from app import app
from user import db
from user.models import User

logging.basicConfig(filename='routes.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


@app.route("/signup", methods=["POST"])
def signup():
    print("Reach signup")
    try:
        if request.method == "POST":
            userdata = json.loads(request.data)
            user_id = userdata.get('user_id')
            username = userdata.get('username')
            email = userdata.get('email')
            password = userdata.get("password")
            if User.query.filter_by(username=username).first() or User.query.filter_by(
                    user_id=user_id).first() or User.query.filter_by(email=email).first():
                return jsonify({
                    "message": "duplicate found in username or userid or email "
                })
            else:
                user = User(user_id, username, email, password)
                db.session.add(user)
                db.session.commit()
                return jsonify({"message": "user is created "})
    except Exception as e:
        app.logger.error(e)


@app.route("/signin", methods=["POST"])
def signin():
    try:
        if request.method == "POST":
            userdata = json.loads(request.data)
            username = userdata.get("username")
            password = userdata.get("password")
            print(username, password)
            is_signin = User.query.filter_by(username=username, password=password).first()
            print(is_signin)
            if is_signin:
                return jsonify({"message": "user signin successfully"})
            else:
                return jsonify({"message": "user signin unsuccessful"})
    except Exception as e:
        app.logger.error(e)
