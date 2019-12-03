from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_returns_valid_user(self):
        """Test creating a user with email is successfull"""
        email = "test@google.com"
        password = "testPass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_users_email_is_always_stored_all_lowercase(self):
        """Test that the user always stores email in lowercase"""
        email = "test@GOOgle.com"
        user = get_user_model().objects.create_user(email, "pw123")

        self.assertEqual(user.email, email.lower())

    def test_create_user_with_invalid_email_fails(self):
        """Test that you can't create a user with invalid email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_user_manager_can_create_superuser(self):
        """Test that user manager can create a superuser"""
        user = get_user_model().objects.create_superuser(
            'test@google.com',
            'pw123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)
