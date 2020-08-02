from __future__ import absolute_import

import hashlib
from flask import Blueprint
from flask import request
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
    user = user_utils.get_user_by_email(email)

    if user:
        return "Looks like this user already exists."
    return user_utils.create_new_user(name, email, password)


@auth.route('/logout')
def logout():
    return 'Logged Out'
