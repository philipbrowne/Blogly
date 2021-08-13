from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import datetime

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
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now)
    created_date = db.Column(db.Date, default=datetime.date.today())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'))

    user = db.relationship('User', backref='posts')

    def __repr__(self):
        """Show information about Post"""
        return f'<Post ID {self.id} {self.title}>'
    
    @property
    def date(self):
        return self.created_at.strftime("%a %b %-d %Y, %-I:%M %p")

    
    
    
