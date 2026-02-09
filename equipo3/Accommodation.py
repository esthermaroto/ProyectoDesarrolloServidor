from .db import db
from sqlalchemy import CheckConstraint

class Accommodation(db.Model):
    __tablename__ = 'accommodation'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phoneNumber = db.Column(db.String(20))
    web = db.Column(db.String(150))
    stars_quality = db.Column(db.Integer)
    description = db.Column(db.Text)
    type = db.Column(db.String(20), nullable=False) # 'hotel' or 'house'
    
    # Foreign Key to User
    id_company = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationship with User
    owner = db.relationship('User', back_populates='accommodations')

    __table_args__ = (
        CheckConstraint('stars_quality BETWEEN 1 AND 5', name='check_stars_quality'),
    )

    def __repr__(self):
        return f'<Accommodation {self.name}>'

    