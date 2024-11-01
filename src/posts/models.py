from model import db


class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    images = db.Column(db.String(1000), nullable=True, default="")
    created_at = db.Column(db.DateTime, server_default=db.func.now())