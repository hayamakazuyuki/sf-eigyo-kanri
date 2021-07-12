from .extentions import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    line_message_id = db.Column(db.String(255), nullable=False)
    line_user_id = db.Column(db.String(255), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.Datetime, nullable=False)
