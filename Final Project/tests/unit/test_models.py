from app import *

# test user model
def test_user_model():
    test_user = User(email='testuser@yahoo.com', password='testpass', username='testuser')
    assert test_user.username == 'testuser'
    assert test_user.password == 'testpass'
    assert test_user.email == 'testuser@yahoo.com'

# test session model
def test_session_model():
    test_session = Session(session_key=generate_session_key())

    assert print(test_session) == print(test_session)

# test forum model
def test_forum_model():
    test_forum = Forum(name='testforum')

    assert test_forum.name == 'testforum'

# test post model
def test_post_model():
    test_post = Post(content='testcontent', date_created=datetime.utcnow, username='testuser', thread_id=1)

    assert test_post.content == 'testcontent'
    assert test_post.date_created == datetime.utcnow
    assert test_post.username == 'testuser'
    assert test_post.thread_id == 1

# test thread model
def test_thread_model():
    test_thread = Thread(title='testtitle', content='testcontent', created_at=datetime.utcnow, forum_id=2)

    assert test_thread.title == 'testtitle'
    assert test_thread.content == 'testcontent'
    assert test_thread.created_at == datetime.utcnow
    assert test_thread.forum_id == 2