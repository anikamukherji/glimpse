from __future__ import absolute_import

from main import db


class ChatRoom(db.Model):
    __tablename__ = "chatroom"
    id = db.Column(db.String(100), primary_key=True)
    owner = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, nullable=False)
    ended_at = db.Column(db.DateTime, nullable=True)
    # how long (minutes) the chats should last
    duration = db.Column(db.Integer, nullable=False)

    # right now, a user can only be a part of one active chatroom
    members = db.relationship("User", backref="chatroom", lazy=True)
    chats = db.relationship("Chat", backref="chatroom", lazy=True)
