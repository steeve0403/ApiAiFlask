from src import db
from datetime import datetime


class RevokedToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)  # JWT ID
    revoked_at = db.Column(db.DateTime, default=datetime.utcnow)

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_token_revoked(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)
