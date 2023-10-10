from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from passlib.hash import pbkdf2_sha256


db = SQLAlchemy()

class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    def get_id(self):
        return self.id
    

class Items(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=True)
    type = db.Column(db.String(255), nullable=True)
    condition = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=False)

class ExchangeRequests(db.Model):
    __tablename__ = 'exchange_requests'

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    requester_item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    status = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=db.func.current_timestamp())
    address = db.Column(db.String(255))
    shipping_type = db.Column(db.String(255))

class Comments(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=db.func.current_timestamp())
    exchange_request_id = db.Column(db.Integer, db.ForeignKey('exchange_requests.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))