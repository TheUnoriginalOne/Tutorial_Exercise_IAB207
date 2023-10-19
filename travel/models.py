from . import db
from datetime import datetime
from flask_login import UserMixin

# User model for storing user information
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  # Store hashed password
    comments = db.relationship('Comment', backref='user')  # Relationship with comments

    def __repr__(self):
        return f"Name: {self.name}"

# Destination model for storing travel destination information
class Destination(db.Model):
    __tablename__ = 'destinations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    image = db.Column(db.String(400))
    currency = db.Column(db.String(3))
    comments = db.relationship('Comment', backref='destination')  # Relationship with comments

    def __repr__(self):
        return f"Name: {self.name}"

# Comment model for storing user comments
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # User foreign key
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'))  # Destination foreign key

    def __repr__(self):
        return f"Comment: {self.text}"

# Hotel model for storing hotel information
class Hotel(db.Model):
    __tablename__ = 'hotels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, nullable=False)
    description = db.Column(db.String(500))
    room_avail = db.Column(db.Boolean, default=True)
    rooms = db.relationship('Room', backref='hotel', lazy='dynamic')  # One-to-many relationship with Room model
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'))  # Destination foreign key

    def to_dict(self):
        h_dict = {
            b.name: str(getattr(self, b.name)) for b in self.__table__.columns
        }
        h_rooms = []
        for room in self.rooms:
            room_data = {
                'id': room.id,
                'room_type': room.type,
                'num_rooms': room.num_rooms,
                'room_description': room.description,
                'room_rate': room.rate,
                'hotel_id': room.hotel_id
            }
            h_rooms.append(room_data)
        h_dict['rooms'] = h_rooms
        return h_dict

# Room model for storing room information
class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), index=True, nullable=False)
    num_rooms = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500))
    rate = db.Column(db.Float(7))
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotels.id'))  # Hotel foreign key