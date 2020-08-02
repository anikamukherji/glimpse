from __future__ import absolute_import

import datetime
from flask import Blueprint
from flask import request
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from main import db
from main.models.user_model import User
from main.utils import user_utils

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    email = request.args.get('email')
    password = request.args.get('password')
    user = user_utils.get_user_by_email(email)

    if not user or not check_password_hash(user.password, password):
        return "Login credentails invalid. Did you type your username or password wrong?"
    return user.id


@auth.route('/signup', methods=["POST"])
def signup():
    email = request.args.get('email')
    name = request.args.get('name')
    password = request.args.get('password')
    user = User.query.filter_by(email=email).first()
    created_at = datetime.datetime.now()

    if user:
        return "Looks like this user already exists.k"
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), created_at=created_at, lifetime_chats=0)
    db.session.add(new_user)
    db.session.commit()
    return new_user.id


@auth.route('/logout')
def logout():
    return 'Logged Out'
