from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

ma = Marshmallow()
db = SQLAlchemy()


class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=True)
    firstname = db.Column(db.String(150), unique=False, nullable=True)
    lastname = db.Column(db.String(150), unique=False, nullable=True)

    def __init__(self, username, firstname, lastname):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname


class Email(db.Model):
    __tablename__ = 'email'
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id', ondelete='CASCADE'), nullable=False)
    email = db.Column(db.String(300), unique=False, nullable=False)
    username = db.relationship('Contact', backref=db.backref('email', lazy='dynamic'))

    def __init__(self, contact_id, email):
        self.email = email
        self.contact_id = contact_id


class ContactSchema(ma.Schema):
    id = fields.Integer(required=False)
    username = fields.String(required=True)
    firstname = fields.String(required=False)
    lastname = fields.String(required=False)
    # email = fields.List(required=False)


class EmailSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    contact_id = fields.Integer(required=True)
    email = fields.String(required=True, validate=validate.Length(1))
