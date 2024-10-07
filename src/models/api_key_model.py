import uuid
from src import db

class ApiKeyModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, user_id):
        self.key = str(uuid.uuid4()) # Generate a unique api key
        self.user_id = user_id

    def save(self):
        db.session.add(self)
        db.session.commit()