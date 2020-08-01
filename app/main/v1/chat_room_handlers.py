from __future__ import absolute_import
from flask import Blueprint
from main import db
from main.utils import chat_room_utils

chat_room = Blueprint('chat_room', __name__)

@chat_room.route('/create_chat_room')
def create_chat_room():
    """ Creates unqiue chat room id
    """
    # TODO: take in owner arg
    room_id = chat_room_utils.generate_chat_room_id()
    # TODO: create DB entry for chat room
    return room_id

@chat_room.route('/join_chat_room')
def join_chat_room():
    # TODO: take in room id arg
    # TODO: verify room id exists
    # TODO: return id if success, error otherwise
    return 'Join'

@chat_room.route('/leave_chat_room')
def leave_chat_room():
    # TODO: take in room id arg
    # TODO: verify room id exists
    # TODO: throw error otherwise
    return "Leave" 
