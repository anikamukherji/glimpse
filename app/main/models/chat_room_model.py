from __future__ import absolute_import
from main import db

class ChatRoom(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    created_at = db.Column(db.DateTime)
    duration = db.Column(db.Integer)
    members = db.relationship('User', backref='chatroom', lazy=True)
    chats = db.relationship('Chat', backref='chatroom', lazy=True)
