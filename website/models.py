from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    unique_id = db.Column(db.String(100), unique=True)
    blob_name = db.Column(db.String(255), unique=True, nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # 1:n relationship with File: each file is associated with a single user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    size = db.Column(db.Integer)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    # SQLAlchemy looks for a relationship with the File model
    # retrieves associated File objects based on foreign key
    files = db.relationship('File')

