from __future__ import absolute_import
from main import db

class User(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime)
    lifetime_chats = db.Column(db.Integer)
    active_chat_room = db.Column(db.String(100))       # id for active chatroom
    active_conversation = db.Column(db.String(100))    # id for active conversation
