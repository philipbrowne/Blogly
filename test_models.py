from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Tests for User model"""

    def setUp(self):
        """Clean up existing users in test model"""
        User.query.delete()

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
        # Tests Default Image URL
        self.assertEqual(
            user.image_url, 'https://randomuser.me/api/portraits/lego/1.jpg')

    def test_get_full_name(self):
        user = User(first_name='Test_First', last_name='Test_Last')
        self.assertEqual(user.full_name, 'Test_First Test_Last')
