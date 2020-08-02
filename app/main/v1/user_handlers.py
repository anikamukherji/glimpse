from __future__ import absolute_import

import json
import datetime
from flask import Blueprint
from flask import request
from main import db
from main.utils import user_utils

user = Blueprint('user', __name__)


@user.route('/user/<user_id>', methods=['GET'])
def get_user_room(user_id):
    """ Get information for a user room
    """
    user = user_utils.get_user_by_id(user_id)
    if not user:
        return "User with id not found."
    user_dict = {}
    for key, value in user.__dict__.items():
        if isinstance(value, datetime.datetime):
            user_dict[key] = value.strftime("%m/%d/%Y, %H:%M:%S")
        elif key.startswith("_") or key == "password":
            continue
        else:
            user_dict[key] = value
    return json.dumps(user_dict)
