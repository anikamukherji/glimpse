from __future__ import absolute_import

import datetime
from flask import Blueprint
from main import db
from main.utils import chat_room_utils
from main.models.chat_model import Chat
from main.models.chat_room_model import ChatRoom

chat_room = Blueprint('chat_room', __name__)


@chat_room.route('/create_chat_room', methods=['POST'])
def create_chat_room():
    """ Creates unqiue chat room id
    """
    owner = request.args.get('user')
    created_at = datetime.datetime.now()
    # chat duration
    duration = request.args.get('duration')
    new_room = ChatRoom(owner=owner, created_at=created_at, duration=duration)
    db.session.add(new_room)
    db.session.commit()
    return room_id


@chat_room.route('/join_chat_room/<chat_room_id>')
def join_chat_room(chat_room_id):
    """ Endpoint for a specific user to join a chat room.
    """
    user_id = request.args.get('user')
    room = ChatRoom.query.filter_by(id=chat_room_id).first()
    if not room:
        return "Room with id not found."
    user = User.query.filter_by(id=user_id).first()
    user.active_chat_room = room.id
    db.session.commit()
    return room.id


@chat_room.route('/leave_chat_room/<chat_room_id>')
def leave_chat_room(chat_room_id):
    """ Endpoint for a specific user to leave a chat room.
    """
    user_id = request.args.get('user')
    room = ChatRoom.query.filter_by(id=chat_room_id).first()
    if not room:
        return "Room may already have been ended."
    user = User.query.filter_by(id=user_id).first()
    user.active_chat_room = None
    # if user is currently in conversation, increaese lifetime chats field
    # and nullify active_chat field. Other users in that active chat may
    # still be in the chat (and will manually leave themselves).
    if user.active_chat:
        user.lifetime_chats += 1
        user.active_chat = None
    db.session.commit()
    return "Success"


@chat_room.route('/end_chat_room/<chat_room_id>')
def end_chat_room(chat_room_id):
    """ Endpoint to close a chat room.
    Chat rooms can only be closed by the user that created it (or after X minutes
    of inactivity, determined by client).
    """
    user_id = request.args.get('user')
    room = ChatRoom.query.filter_by(id=chat_room_id).first()
    if not room:
        return "Room may already have been ended."
    if room.owner != user_id:
        return "Only person who created room may delete it."
    for user in room.members:
        user.active_chat_room = None
        # if user is currently in conversation, increaese lifetime chats field
        # and nullify active_chat field
        if user.active_chat:
            user.lifetime_chats += 1
            user.active_chat = None
    # delete chats for room
    for conversation in room.chats:
        db.session.delete(chat)
    ended_at = datetime.datetime.now()
    room.ended_at = ended_at
    db.session.commit()
    return "Success"
