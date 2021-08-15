from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func, asc, desc
import datetime
from sqlalchemy import asc, desc

"""Models for Blogly."""

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User"""
    __tablename__ = 'users'

    def __repr__(self):
        """Show information about user"""
        return f'<User ID={self.id} first_name={self.first_name} last_name={self.last_name} image_url={self.image_url}>'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String, nullable=False,
                          default='https://randomuser.me/api/portraits/lego/1.jpg')

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Post(db.Model):
    """Post"""
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(5000), nullable=False, default=None)
    created_at = db.Column(db.DateTime(timezone=True),
                           default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', onupdate='CASCADE', ondelete='CASCADE'))

    user = db.relationship('User', backref='posts')
    tags = db.relationship('Tag', secondary='posts_tags', backref='posts')

    def __repr__(self):
        """Show information about Post"""
        return f'<Post ID {self.id} {self.title}>'

    @ property
    def date(self):
        return self.created_at.strftime("%a %b %-d %Y, %-I:%M %p")


class Tag(db.Model):
    """Tag"""
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)


class PostTag(db.Model):
    """Tags on Posts"""
    __tablename__ = 'posts_tags'
    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
