from __future__ import absolute_import
from main import db

class ChatRoom(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    members = db.relationship('User', backref='chat', lazy=True)
    created_at = db.Column(db.DateTime)
    expired = db.Column(db.Boolean)
