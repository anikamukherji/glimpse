from __future__ import absolute_import
from main import db


class Chat(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    # right now, a user can only be a part of one active conversation
    members = db.relationship('User', backref='active_chat', lazy=True)
    created_at = db.Column(db.DateTime)
    expired = db.Column(db.Boolean, default=False)
