from datetime import datetime
from .extentions import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line_user_id = db.Column(db.String(255), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    # posted_at = db.Column(db.Datetime, nullable=False, default=datetime.now)
