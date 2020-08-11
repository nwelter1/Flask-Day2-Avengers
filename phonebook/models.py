from phonebook import app, db

class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    phone_number = db.Column(db.String(15), nullable=False, unique=True)
    address = db.Column(db.String(300), nullable=True)

    def __init__(self, name, email, phone_number, address):
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.address = address

    
    def __repr__(self):
        return f'{self.name}, {self.email}, {self.phone_number} and {self.address} has been created with {self.email}'