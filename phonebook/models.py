from phonebook import app, db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    phone_number = db.Column(db.String(15), nullable=False, unique=True)
    address = db.Column(db.String(300), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, email, phone_number, address, user_id):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.user_id = user_id
    
    def __repr__(self):
        return f'{self.name}, {self.email}, {self.phone_number} and {self.address} has been created with {self.email}'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    post = db.relationship('Info', backref='author', lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def __repr__(self):
        return f'{self.username} has been created with {self.email}'
