from __future__ import absolute_import

import random
import datetime
from flask import Blueprint
from main import db
from main.utils import chat_room_utils
from main.models.chat_model import Chat
from main.models.chat_room_model import ChatRoom

chat = Blueprint('chat', __name__)


@chat.route('/find_chat/<chat_room_id>')
def find_chat(chat_room_id):
    """ This endpoint should be be polled by client until it return a chat id
    """
    user_id = request.args.get('user')
    current_user = User.query.filter_by(id=user_id).first()

    room = ChatRoom.query.filter_by(id=chat_room_id).first()
    if not room:
        return "Room not found."

    # if user has been added to conversation when another user was polling
    if current_user.active_chat:
        return current_user.active_chat.id

    # shuffle members so that we won't keep trying to pair the same people together
    for user in random.shuffle(room.members):
        if user.id != user_id and not user.active_chat:
            created_at = datetime.datetime.now()
            new_conversation = Chat(created_at=created_at, members=[current_user, user], chatroom=room)
            return new_conversation.id

    user.active_chat_room = room.id
    db.session.commit()
    return room.id


@chat.route('/leave_chat/<chat_room_id>')
def leave_chat():
    user_id = request.args.get('user')
    room = ChatRoom.query.filter_by(id=chat_room_id).first()
    if not room:
        return "Room not found."
    
    user = User.query.filter_by(id=user_id).first()

    # increaese lifetime chats field and nullify active_chat field.
    # Other users in that active chat may
    # still be in the chat (and will manually leave themselves).
    if user.active_chat:
        user.lifetime_chats += 1
        user.active_chat = None
    db.session.commit()
    return "Success"
