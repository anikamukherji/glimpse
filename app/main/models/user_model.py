from __future__ import absolute_import
from main import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(100), primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    lifetime_chats = db.Column(db.Integer, nullable=False, default=0)
    chatroom_id = db.Column(db.String(100), db.ForeignKey('chatroom.id'), nullable=True)
    chat_id = db.Column(db.String(100), db.ForeignKey('chat.id'), nullable=True)
