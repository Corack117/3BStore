import unittest
from django.test import TestCase
from applications.users.models import User
from uuid import UUID

class UserModelTest(TestCase):

    def test_user_creation(self):
        user = User.objects.create_user(
            username='testuser',
            password='pass123',
            email='testuser@gmail.com'
        )
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.email, 'testuser@gmail.com')
        self.assertIsNotNone(user.slug)
        self.assertIsInstance(user.slug, UUID)
        self.assertEqual(str(user), user.username)
    
    def test_user_retrieval(self):
        user = User.objects.create_user(
            username='testuser',
            password='pass123',
            email='testuser@gmail.com'
        )
        retrieved_user = User.objects.get(username='testuser')
        self.assertEqual(retrieved_user.email, 'testuser@gmail.com')
        self.assertEqual(retrieved_user.slug, user.slug)

    def test_unique_email_constraint(self):
        User.objects.create_user(
            username='testuser1',
            password='pass123',
            email='testuser1@gmail.com'
        )
        with self.assertRaises(Exception):
            User.objects.create_user(
                username='testuser2',
                password='pass123',
                email='testuser1@gmail.com'
            )