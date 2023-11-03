from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    # Relationship to reference the events that the user has created
    events = db.relationship('Event', backref='user', lazy='dynamic')
    # Relationship to reference the comments that the user has created
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    def __repr__(self):
        return f"<User {self.name}>"

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    artist_or_band = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(500))
    tickets_available = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(2000))
    # Foreign key to associate an event with a user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='event', lazy='dynamic')

    def __repr__(self):
        return f"<Event {self.title}>"

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now)
    # Foreign keys to associate a comment with a user and an event
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return f"<Comment by User {self.user_id} on Event {self.event_id}: {self.text}>"
