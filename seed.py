# """Seed file to make sample data for db."""

from models import db, connect_db, User, Post
from app import app

# Create all tables
db.drop_all()
db.create_all()

u1 = User(first_name='Phil', last_name='Browne')
u2 = User(first_name='Sonny', last_name='Rollins')
u3 = User(first_name='Charles', last_name='Johnson')
u4 = User(first_name='Kenny', last_name='Jackson')

p1 = Post(title='First Post', content='Hello World!!!!1', user_id=1)
p2 = Post(title='Jazz Time', content='Time to practice my saxophone!', user_id=2)
p3 = Post(title='Philosophy', content='What is the meaning of life? What is life?', user_id=3)
p4 = Post(title='I dunno', content='What is the point of these seeds lol', user_id=1)
p5 = Post(title='Seeding', content='I need to think of better content for these', user_id=4)
p6 = Post(title='Python is Cool', content='I enjoy SQLAlchemy!', user_id=1)
p7 = Post(title='Good Practice', content='So many different posts', user_id=2)

db.session.add_all([u1, u2, u3, u4])
db.session.commit()

db.session.add_all([p1,p2,p3,p4,p5,p6,p7])
db.session.commit()