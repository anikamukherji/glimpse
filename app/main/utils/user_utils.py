from __future__ import absolute_import

import datetime
from main import db
from main.models.user_model import User
from werkzeug.security import generate_password_hash


def get_user_by_id(user_id):
    """ Queries DB for user by id 
    """
    return User.query.filter_by(id=user_id).first()


def get_user_by_email(email):
    """ Queries DB for user by email
    """
    return User.query.filter_by(email=email).first()


def create_new_user(name, email, password):
    """ Creates new entry in DB for a new user
    """
    # create simple user id  by hashing email
    user_id = str(hash(email))[1:13]
    created_at = datetime.datetime.now()
    new_user = User(id=user_id, email=email, name=name, password=generate_password_hash(password, method='sha256'), created_at=created_at, lifetime_chats=0)
    db.session.add(new_user)
    db.session.commit()
    return new_user.id
