from src import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"User('{self.firstname}', '{self.lastname}', '{self.email}')"
