from sqlalchemy import ARRAY
from sqlalchemy.ext.mutable import MutableList

from ...model import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    images = db.Column(MutableList.as_mutable(ARRAY(db.Text)), nullable=True, default=list)
    created_at = db.Column(db.DateTime, server_default=db.func.now())