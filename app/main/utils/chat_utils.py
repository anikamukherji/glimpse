from __future__ import absolute_import

import datetime
import random
import string

from main import db
from main.models.chat_model import Chat
from main.models.chat_room_model import ChatRoom

DEFAULT_CHAT_ID_LENGTH = 6


def get_chat_by_id(room_id):
    return Chat.query.filter_by(id=room_id).first()


def generate_chat_id(id_length=DEFAULT_CHAT_ID_LENGTH):
    """ Generate chat id of random alphanumeric characters.
    Check to make sure the room id doesn't exist already, only return id if unique.
    """
    valid_chars = string.ascii_letters + string.digits
    room_id = "".join((random.choice(valid_chars) for _ in range(id_length)))
    already_exists = get_chat_by_id(room_id) is not None
    if already_exists:
        room_id = "".join((random.choice(valid_chars) for _ in range(id_length)))
    return room_id


def create_new_chat(members, chat_room_id):
    """ Creates new chat entry with members (list of User objects)
    """
    created_at = datetime.datetime.now()
    chat_id = generate_chat_id()
    new_chat = Chat(id=chat_id, created_at=created_at, chatroom_id=chat_room_id)
    for user in members:
        user.chat_id = new_chat.id
    db.session.add(new_chat)
    db.session.commit()
    return new_chat.id
