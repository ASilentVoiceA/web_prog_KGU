from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class Roles(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), index=True, primary_key=True)
    name = db.Column(db.String(), nullable=False)


class Profile_status(db.Model):
    __tablename__ = 'profile_status'
    id = db.Column(db.Integer(), index=True, primary_key=True)
    name = db.Column(db.String(), nullable=False)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), index=True, primary_key=True)
    role = db.Column(db.Integer, db.ForeignKey(Roles.id), nullable=False)
    profile_status = db.Column(db.Integer, db.ForeignKey(Profile_status.id), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<{self.id}:{self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class History_search(db.Model):
    __tablename__ = 'history_search'
    id = db.Column(db.Integer(), index=True, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey(User.id), index=True, nullable=False)
    str_search = db.Column(db.String(), nullable=False)
    data = db.Column(db.DateTime())


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
