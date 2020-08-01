from __future__ import absolute_import
import random
import string

DEFAULT_CHAT_ROOM_ID_LENGTH = 6


def generate_chat_room_id(id_length=DEFAULT_CHAT_ROOM_ID_LENGTH):
    """ Generate chat room id of random alphanumeric characters.
    Check to make sure the room id doesn't exist already, only return id if unique.
    """
    valid_chars = string.ascii_letters + string.digits
    room_id = ''.join((random.choice(valid_chars) for _ in range(id_length)))
    # call db to verify doesn't exist
    return room_id
