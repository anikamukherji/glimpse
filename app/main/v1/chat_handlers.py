from __future__ import absolute_import

import random
import json
import datetime
from flask import Blueprint
from flask import request
from main import db
from main.utils import chat_room_utils
from main.utils import chat_utils
from main.utils import user_utils
from main.models.chat_model import Chat
from main.models.chat_room_model import ChatRoom

chat = Blueprint('chat', __name__)


@chat.route('/chat/<chat_id>', methods=['GET'])
def get_chat_room(chat_id):
    """ Get information for a chat room
    """
    chat = chat_utils.get_chat_by_id(chat_id)
    if not chat:
        return "Chat with id not found."
    chat_dict = {}
    for key, value in chat.__dict__.items():
        if isinstance(value, datetime.datetime):
            chat_dict[key] = value.strftime("%m/%d/%Y, %H:%M:%S")
        elif key.startswith("_"):
            continue
        else:
            chat_dict[key] = value
    return json.dumps(chat_dict)


@chat.route('/find_chat/<chat_room_id>')
def find_chat(chat_room_id):
    """ This endpoint should be be polled by client until it return a chat id
    """
    user_id = request.args.get('user')
    current_user = user_utils.get_user_by_id(user_id)

    room = chat_room_utils.get_room_by_id(chat_room_id)
    if not room:
        return "Room not found."

    # if user has been added to conversation when another user was polling
    if current_user.chat_id:
        return current_user.chat_id

    # shuffle members so that we won't keep trying to pair the same people together
    members = room.members
    random.shuffle(members)
    for user in members:
        if user.id != user_id and not user.chat_id:
            members=[current_user, user]
            new_chat_id = chat_utils.create_new_chat(members, chat_room_id)
            return new_chat_id

    user.chatroom_id = room.id
    db.session.commit()
    return room.id


@chat.route('/leave_chat/<chat_room_id>/<chat_id>')
def leave_chat(chat_room_id, chat_id):
    user_id = request.args.get('user')
    room = chat_room_utils.get_room_by_id(chat_room_id)
    if not room:
        return "Room not found."
    
    user = user_utils.get_user_by_id(user_id)

    # increaese lifetime chats field and nullify chat_id field.
    # Other users in that active chat may
    # still be in the chat (and will manually leave themselves).
    if user.chat_id:
        user.lifetime_chats += 1
        user.chat_id = None
    db.session.commit()
    return "Success"
