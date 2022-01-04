from app import app
import os
from unittest import TestCase
from sqlalchemy import exc
from models import db, User, Brewery

os.environ['DATABASE_URL'] = 'postgresql://brewery-test'


db.create_all()


class UserTestCase(TestCase):

    def setUp(self):

        db.drop_all()
        db.create_all()

        user_1 = User.sign_up('test1', 'Test1', 'User1', '1/1/1950',
                              'test1@test.com', None, 'password')
        user_1_id = 1122
        user_1.id = user_1_id

        user_2 = User.sign_up('test2', 'Test2', 'User2', '12/31/1950',
                              'test2@test.com', None, 'password')
        user_2_id = 2233
        user_2.id = user_2_id

        db.session.commit()

        user_1 = User.query.get(user_1_id)
        user_2 = User.query.get(user_2_id)

        self.user_1 = user_1
        self.user_1_id = user_1_id

        self.user_2 = user_2
        self.user_2_id = user_2_id

        self.client = app.test_client

    def tearDown(self):

        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_user_model(self):

        u = User(username='testuser', first_name='Tester', last_name='Users',
                 date_of_birth='2/2/1988', email='tester@test.com', password='password')

        db.session.add(u)
        db.session.commit()

        self.assertTrue(u.id == 1)
        self.assertTrue(u.fav_brewery == None)

    def test_signup(self):

        test_user = User.sign_up(
            'testguy', 'guy', 'testoski', '12/18/1988', 'guy@gmail.com', None, 'password')

        user_id = 9876
        test_user.id = user_id
        db.session.commit()

        test_user = User.query.get(user_id)

        self.assertEqual(test_user.username, 'testguy')
        self.assertEqual(test_user.email, 'guy@gmail.com')
        self.assertEqual(test_user.id, 9876)
        self.assertIsNotNone(test_user)
        self.assertTrue(test_user.password.startswith('$2b$'))

    def test_incorrect_usernames(self):

        invaild_username = User.sign_up(
            None, 'guy', 'testoski', '12/18/1988', 'guy@gmail.com', None, 'password')

        user_id = 444555

        invaild_username.id = user_id

        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_incorrect_email(self):

        invaild_username = User.sign_up(
            'testguy', 'guy', 'testoski', '12/18/1988', None, None, 'password')

        user_id = 12344

        invaild_username.id = user_id

        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_incorrect_password(self):

        with self.assertRaises(ValueError) as context:
            User.sign_up('testguy', 'guy', 'testoski',
                         '12/18/1988', 'guy@gmail.com', None, '')

        with self.assertRaises(ValueError) as context:
            User.sign_up('testguy', 'guy', 'testoski',
                         '12/18/1988', 'guy@gmail.com', None, None)

    def test_authentication(self):

        user = User.authenticate(self.user_1.username, "password")
        self.assertIsNotNone(user)
        self.assertEqual(user.id, self.user_1_id)

    def test_wrong_user_authentication(self):
        self.assertFalse(User.authenticate('notrightusername', 'password'))

    def test_wrong_password_authentication(self):
        self.assertFalse(User.authenticate(
            self.user_1.username, 'notrightpassword'))
