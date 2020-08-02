from __future__ import absolute_import

import datetime
# import simplejson as json
import json

from flask import Blueprint, request

from main import db
from main.models.chat_model import Chat
from main.models.chat_room_model import ChatRoom
from main.utils import chat_room_utils, user_utils

chat_room = Blueprint("chat_room", __name__)

DEFAULT_CHAT_LENGTH = 2  # minutes


@chat_room.route("/chat_room/<chat_room_id>", methods=["GET"])
def get_chat_room(chat_room_id):
    """ Get information for a chat room
    """
    room = chat_room_utils.get_room_by_id(chat_room_id)
    if not room:
        return "Room with id not found."
    room_dict = {}
    for key, value in room.__dict__.items():
        if isinstance(value, datetime.datetime):
            room_dict[key] = value.strftime("%m/%d/%Y, %H:%M:%S")
        elif key.startswith("_"):
            continue
        else:
            room_dict[key] = value
    return json.dumps(room_dict)


@chat_room.route("/create_chat_room", methods=["POST"])
def create_chat_room():
    """ Creates unqiue chat room id
    """
    owner_id = request.args.get("user")
    # chat duration, default is  2 min
    duration = request.args.get("duration", DEFAULT_CHAT_LENGTH)
    new_room_id = chat_room_utils.create_chat_room(owner_id, duration)
    user = user_utils.get_user_by_id(owner_id)
    user.chatroom_id = new_room_id
    db.session.commit()
    return new_room_id


@chat_room.route("/join_chat_room/<chat_room_id>")
def join_chat_room(chat_room_id):
    """ Endpoint for a specific user to join a chat room.
    """
    user_id = request.args.get("user")
    room = chat_room_utils.get_room_by_id(chat_room_id)
    if not room:
        return "Room with id not found."
    if room.ended_at:
        return "This room has already been ended."
    user = user_utils.get_user_by_id(user_id)
    user.chatroom_id = room.id
    db.session.commit()
    return room.id


@chat_room.route("/leave_chat_room/<chat_room_id>")
def leave_chat_room(chat_room_id):
    """ Endpoint for a specific user to leave a chat room.
    """
    user_id = request.args.get("user")
    room = chat_room_utils.get_room_by_id(chat_room_id)
    if not room:
        return "Room with id not found."
    user = user_utils.get_user_by_id(user_id)
    user.chatroom_id = None
    # if user is currently in conversation, increaese lifetime chats field
    # and nullify chat_id field. Other users in that active chat may
    # still be in the chat (and will manually leave themselves).
    if user.chat_id:
        user.lifetime_chats += 1
        user.chat_id = None
    user.lifetime_chats = 3
    db.session.commit()
    return "Success"


@chat_room.route("/end_chat_room/<chat_room_id>")
def end_chat_room(chat_room_id):
    """ Endpoint to close a chat room.
    Chat rooms can only be closed by the user that created it (or after X minutes
    of inactivity, determined by client).
    """
    user_id = request.args.get("user")
    room = chat_room_utils.get_room_by_id(chat_room_id)
    if room.ended_at:
        return "Room may already have been ended."
    if room.owner != user_id:
        return "Only person who created room may delete it."
    for user in room.members:
        user.chatroom_id = None
        # if user is currently in conversation, increaese lifetime chats field
        # and nullify chat_id field
        if user.chat_id:
            user.lifetime_chats += 1
            user.chat_id = None
    ended_at = datetime.datetime.now()
    room.ended_at = ended_at
    chat_room_utils.remove_all_chats_from_chatroom(room)
    db.session.commit()
    return "Success"
