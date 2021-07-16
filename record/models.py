from datetime import datetime
from .extentions import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(80), nullable=False)
    group_id = db.Column(db.String(255), nullable=True)
    message_id = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text(), nullable=False)
    posted_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    checked = db.Column(db.Integer, nullable=True)
