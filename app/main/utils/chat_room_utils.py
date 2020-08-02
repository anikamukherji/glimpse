from __future__ import absolute_import

from main import db
from main.models.chat_room_model import ChatRoom

import datetime
import random
import string

DEFAULT_CHAT_ROOM_ID_LENGTH = 6

def get_room_by_id(room_id):
    return ChatRoom.query.filter_by(id=room_id).first()


def generate_chat_room_id(id_length=DEFAULT_CHAT_ROOM_ID_LENGTH):
    """ Generate chat room id of random alphanumeric characters.
    Check to make sure the room id doesn't exist already, only return id if unique.
    """
    valid_chars = string.ascii_letters + string.digits
    room_id = ''.join((random.choice(valid_chars) for _ in range(id_length)))
    already_exists = get_room_by_id(room_id) is not None
    if already_exists:
        room_id = ''.join((random.choice(valid_chars) for _ in range(id_length)))
    return room_id


def create_chat_room(owner_id, duration):
    """ Creates new chat room id and updates DB. Adds owner of chatroom
    to chatroom members.

    Returns id of the new room
    """
    room_id = generate_chat_room_id()
    created_at = datetime.datetime.now()
    new_room = ChatRoom(id=room_id, owner=owner_id, created_at=created_at, duration=duration)
    db.session.add(new_room)
    db.session.commit()
    return room_id


def remove_all_chats_from_chatroom(room):
    """ Clean up function to delete chat room entries from DB

    Room arg should be room object, not id
    """
    for chat in room.chats:
        db.session.delete(chat)
    db.session.commit()
