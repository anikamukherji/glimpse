from __future__ import absolute_import

from main import db
from main.models.user_model import User


def get_user_by_email(email):
    """ Queries DB for user by email
    """
    return User.query.filter_by(email=email).first()
