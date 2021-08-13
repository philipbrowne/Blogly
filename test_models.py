from unittest import TestCase

from app import app
from models import db, User, Post
from sqlalchemy.sql import func

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """Tests for User model"""

    def setUp(self):
        """Clean up existing users in test model"""
        User.query.delete()
        Post.query.delete()

    def tearDown(self):
        """Clean up any bad transactions"""
        db.session.rollback()

    def test_new_user(self):
        """Tests Creating New User"""
        user = User(first_name='Test_First', last_name='Test_Last')
        self.assertEqual(user.first_name, 'Test_First')
        self.assertEqual(user.last_name, 'Test_Last')
        db.session.add(user)
        db.session.commit()
        self.userId = user.id
        #Tests FK Relationship with Post
        post = Post(title='Test_Title', content='Test_Content', user_id=self.userId)
        db.session.add(post)
        db.session.commit()
        self.assertEqual(post.user.first_name, 'Test_First')
        # Tests Default Image URL
        self.assertEqual(
            user.image_url, 'https://randomuser.me/api/portraits/lego/1.jpg')

    def test_get_full_name(self):
        """Tests full name property"""
        user = User(first_name='Test_First', last_name='Test_Last')
        self.assertEqual(user.full_name, 'Test_First Test_Last')
    
class PostModelTestCase(TestCase):
    """Tests for Post Model"""
    def setUp(self):
        """Clean up existing posts in test model"""
        User.query.delete()
        Post.query.delete()

    def tearDown(self):
        """Clean up any bad transactions"""
        db.session.rollback()
        
    def test_new_post(self):
        """Tests for Creating New Post"""
        DateTime = func.now()
        post = Post(title='Test_Title', content='Test_Content', created_at=DateTime)
        self.assertEqual(post.title, 'Test_Title')
        self.assertEqual(post.content, 'Test_Content')
        self.assertEqual(post.created_at, DateTime)