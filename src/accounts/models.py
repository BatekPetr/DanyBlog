from datetime import datetime

import sqlalchemy
from flask_login import UserMixin

from ...model import bcrypt, db


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, server_default=sqlalchemy.sql.expression.literal("NoName"))
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False,
                             server_default=sqlalchemy.sql.expression.literal(False))
    confirmed_on = db.Column(db.DateTime, nullable=True)
    is_approved = db.Column(db.Boolean, nullable=False, default=False,
                             server_default=sqlalchemy.sql.expression.literal(False))

    def __init__(self, email, name, password, is_admin=False, is_confirmed=False, confirmed_on=None, is_approved=False):
        self.email = email
        self.name = name
        self.password = bcrypt.generate_password_hash(password).decode('utf8')
        self.created_on = datetime.now()
        self.is_admin = is_admin
        self.is_confirmed = is_confirmed
        self.confirmed_on = confirmed_on
        self.is_approved = is_approved

    def __repr__(self):
        return f"<email {self.email}>"
