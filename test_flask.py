from unittest import TestCase

from app import app
from models import db, User, Post
from sqlalchemy.sql import asc, desc, func

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Test for views for Users"""
    def setUp(self):
        """Aad sample user"""
        User.query.delete()
        user = User(first_name='Test_First', last_name='Test_Last')
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id
        self.user = user

    def tearDown(self):
        """Clean up any fouled transaction"""
        db.session.rollback()

    def test_user_list(self):
        """Tests user list to make sure added user from setup is there"""
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test_First Test_Last', html)

    def test_user_details(self):
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Test_First Test_Last</h1>', html)
            # Check if Default Image is In Html
            self.assertIn(
                'https://randomuser.me/api/portraits/lego/1.jpg', html)

    def test_add_user(self):
        with app.test_client() as client:
            user2 = {'first_name': 'Test_First2', 'last_name': 'Test_Last2',
                     'image_url': 'https://randomuser.me/api/portraits/lego/1.jpg'}
            resp = client.post('/users/new', data=user2, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test_First2 Test_Last2', html)

    def test_edit_user(self):
        """Tests Editing User"""
        with app.test_client() as client:
            user1 = {'first_name': 'FIRST_NEW', 'last_name': 'LAST_NEW',
                     'image_url': 'https://randomuser.me/api/portraits/lego/1.jpg'}
            resp = client.post(f'/users/{self.user_id}/edit', data=user1,
                               follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('FIRST_NEW LAST_NEW', html)
                
    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post('/users/2/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Test_First2 Test_Last2', html)

class PostViewsTestCase(TestCase):
    def setUp(self):
        """Aad sample user"""
        User.query.delete()
        Post.query.delete()
        user = User(first_name='Test_First', last_name='Test_Last')
        db.session.add(user)
        db.session.commit()
        post = Post(title='SETUP_TITLE', content='SETUP_CONTENT', user_id=user.id)
        self.user_id = user.id
        db.session.add(post)
        db.session.commit()
        self.post_id=post.id
    def tearDown(self):
        db.session.rollback()
    def test_add_post(self):
        """Tests adding new post"""
        with app.test_client() as client:
            user = User(first_name='Test_First', last_name='Test_Last')
            post1 = {'title': 'TESTPOST_TITLE', 'content': 'TESTPOST_CONTENT'}
            resp = client.post(f'/users/{self.user_id}/posts/new', data=post1, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('TESTPOST_TITLE',html)
    def test_show_post(self):
        """Tests Showing Post for Post ID"""
        with app.test_client() as client:
            resp = client.get(f'/posts/{self.post_id}')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('SETUP_CONTENT', html)
    def test_edit_post(self):
        """Tests Changing Post"""
        with app.test_client() as client:
            postchange = {'title': 'CHANGEPOST_TITLE', 'content': 'CHANGEPOST_CONTENT'}
            resp = client.post(f'/posts/{self.post_id}/edit', data=postchange, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('CHANGEPOST_TITLE', html)
            
    def test_post_delete(self):
        """Tests Deleting Post"""
        with app.test_client() as client:
            post = Post(title='DELETE_TITLE', content='DELETE_CONTENT', user_id=self.user_id)
            db.session.add(post)
            db.session.commit()
            self.post_id = post.id
            resp = client.get(f'/posts/{self.post_id}')
            html = resp.get_data(as_text=True)
            self.assertIn('DELETE_CONTENT', html)
            resp = client.post(f'/posts/{self.post_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('DELETE_TITLE', html)
            
            
            