from mongoengine import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from flask import current_app as app
from flask import g
import datetime


class User(Document):
    username = StringField(max_length=200, required=True, unique=True)
    password = StringField(max_length=200, required=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    activated = BooleanField(default=False)
    activated_at = DateTimeField()
    deleted_at = DateTimeField()
    deleted = BooleanField(required=True, default=False)

    def set_username_and_password(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': str(self.id)})

    def generate_activation_code(self, expiration=6000):
        s = Serializer(app.config['ACTIVATION_SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': str(self.id)})

    def marked_as_deleted(self):
        self.deleted = True
        self.deleted_at = datetime.datetime.now()
        self.save()

    def marked_as_active(self):
        self.activated = True
        self.activated_at = datetime.datetime.now()
        self.save()

    def assertion_is_not_deleted(self):
        if not hasattr(self, 'deleted'):
            raise Exception
        if self.deleted:
            raise Exception

    def assertion_is_activated(self):
        if not hasattr(self, 'activated'):
            raise Exception
        if not self.activated:
            raise Exception

    def verify_activation( self,activation_code ):
        s = Serializer(app.config['ACTIVATION_SECRET_KEY'])
        try:
            data = s.loads(activation_code)
        except SignatureExpired:
            return False
        except BadSignature:
            return False

        if self.id == data['id']:
            self.marked_as_active()
            return True
        return False

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.objects.get(pk=data['id'])
        return user

    auth = HTTPBasicAuth()

    @staticmethod
    @auth.verify_password
    def verify_password(username_or_token, password):
        # first try to authenticate by token
        user = User.verify_auth_token(username_or_token)
        if not user:
            # try to authenticate with username/password
            user = User.objects.get(username=username_or_token)
            if not user or not user.check_password(password):
                return False
        g.user = user
        return True
