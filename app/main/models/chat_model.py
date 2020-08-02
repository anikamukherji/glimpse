from __future__ import absolute_import

from main import db


class Chat(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.String(100), primary_key=True)
    # right now, a user can only be a part of one active conversation
    created_at = db.Column(db.DateTime, nullable=False)
    expired = db.Column(db.Boolean, default=False, nullable=True)
    chatroom = db.Column(db.String(100), db.ForeignKey('chatroom.id'), nullable=False)

    members = db.relationship('User', backref='chat', lazy=True)
