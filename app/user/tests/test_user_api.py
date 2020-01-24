from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    """Test the user API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successfull"""
        payload = {
            'email': 'test@brabbl.com',
            'password': 'testPass123',
            'name': 'test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_user_with_existing_email_fails(self):
        """Test that duplicate user cant be created"""
        payload = {
            'email': 'test@brabbl.com',
            'password': 'testPass123',
            'name': 'test name'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_short_password_fails(self):
        """Test that users with a too short password can't be created"""
        payload = {
            'email': 'test@brabbl.com',
            'password': 'test',
            'name': 'test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_esisting_user_succeeds(self):
        """Test that a token is created for the user"""
        payload = {
            'email': 'test@brabbl.com',
            'password': 'testPass123',
            'name': 'test name'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_for_invalid_credentials_fails(self):
        """Test that no token is created for invalid credentials"""
        payload = {
            'email': 'test@brabbl.com',
            'password': 'testPass123',
            'name': 'test name'
        }
        create_user(**payload)

        incorrect_payload = {
            'email': 'test@brabbl.com',
            'password': 'testPass456WRONG',
            'name': 'test name'
        }
        res = self.client.post(TOKEN_URL, incorrect_payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_for_non_existing_user_fails(self):
        """Test that no token is created for non existing user"""
        payload = {
            'email': 'test@brabbl.com',
            'password': 'testPass123',
            'name': 'test name'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
