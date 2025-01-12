from django.contrib.auth import get_user_model

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserSetupMixin:
    """Mixin to set up users and reusable test data."""
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_superuser(
            username='admin',
            email='root@email.com',
            password='secret1234'
        )
        cls.admin_token = Token.objects.get(user=cls.admin)

        cls.user = User.objects.create_user(
            email='random@email.com',
            password='secret1234'
        )

        cls.user2 = User.objects.create_user(
            email='randomuser2@email.com',
            password='secret1234#'
        )

        cls.user2_token = Token.objects.get(user=cls.user2)
        cls.user_token = Token.objects.get(user=cls.user)

        cls.users_list_url = reverse('users-list')
        cls.login_url = reverse('rest_framework:login')
        cls.logout_url = reverse('rest_framework:logout')

    def set_credentials(self, token):
        """Helper to set authorization token."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')


class TestUserRegistration(UserSetupMixin, APITestCase):
    """Test cases for user registration."""

    def test_registration_with_valid_data(self):
        """Ensure a user can register with valid data."""
        user_data = {
            "username": "testboy",
            "email": "testboy@email.com",
            "password": "secret12#as"
        }
        response = self.client.post(self.users_list_url, data=user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_user = User.objects.get(email=user_data['email'])
        self.assertEqual(response.data['username'], user_data['username'])
        self.assertEqual(response.data['joined'], str(new_user.profile.member_since))
        self.assertEqual(response.data['status'], new_user.profile.role)
        self.assertTrue(new_user.check_password(user_data['password']))

    def test_registration_with_incomplete_data(self):
        """Ensure registration fails with incomplete data."""
        incomplete_data = {
            "username": "testboy1",
            "email": "",
            "password": "secret12#as"
        }
        response = self.client.post(self.users_list_url, data=incomplete_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestUserAuthentication(UserSetupMixin, APITestCase):
    """Test cases for user login and logout."""

    def test_user_login_logout(self):
        """Test login and logout functionality."""
        data = {"email": self.admin.email, "password": "secret1234"}

        response = self.client.post(self.login_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.set_credentials(self.admin_token.key)
        logout_response = self.client.post(self.logout_url)
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)


class TestUserEndpoints(UserSetupMixin, APITestCase):
    """Test cases for user-related endpoints."""

    def test_retrieve_users_list(self):
        """Ensure users list endpoint returns correct data."""
        response = self.client.get(self.users_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)

    def test_authenticated_user_cannot_create_account(self):
        """Ensure authenticated users cannot create new accounts."""
        self.set_credentials(self.user_token.key)
        response = self.client.post(self.users_list_url, data={
            "email": "dummyaccount@email.com",
            "password": "secret1234"
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestUserDetailActions(UserSetupMixin, APITestCase):
    """Test cases for user detail actions like update and delete."""

    def test_user_detail_update(self):
        """Ensure user can update their details."""
        data = {"bio": "Hello I am a random user"}
        self.set_credentials(self.user_token.key)
        response = self.client.patch(self.user.get_absolute_url(), data=data, format='json')
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.bio, data['bio'].lower())

    def test_authenticated_user_cannot_update_another_user(self):
        """Ensure an authenticated user cannot update another user's details."""
        self.set_credentials(self.user_token.key)
        update_data = {"bio": "Attempting unauthorized update"}
        response = self.client.patch(
            path=self.user2.get_absolute_url(),
            data=update_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_cannot_delete_another_user(self):
        """Ensure an authenticated user cannot delete another user's account."""
        self.set_credentials(self.user_token.key)
        response = self.client.delete(path=self.user2.get_absolute_url())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(User.objects.filter(email=self.user2.email).exists())

    def test_user_delete(self):
        """Ensure user can delete their account."""
        self.set_credentials(self.user_token.key)
        response = self.client.delete(self.user.get_absolute_url())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_update_deletion(self):
        """Ensure admin user can delete and update accounts."""
        self.set_credentials(self.admin_token.key)

        update_data = {"bio": "Updated by admin"}
        response = self.client.patch(
            path=self.user.get_absolute_url(),
            data=update_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.bio, update_data["bio"].lower())

        response = self.client.delete(path=self.user2.get_absolute_url())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(email=self.user2.email).exists())


class TestPasswordChange(UserSetupMixin, APITestCase):
    """Test cases for password change endpoint."""

    def test_password_change_with_valid_data(self):
        """Ensure users can change their password with valid data."""
        url = reverse('users-change-password', kwargs={'pk': self.user.pk})
        self.set_credentials(self.user_token.key)
        response = self.client.post(url, data={
            "old_password": "secret1234",
            "new_password": "secret123456",
            "confirm_password": "secret123456"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("secret123456"))

    def test_password_change_with_incorrect_old_password(self):
        """Ensure error is returned if the old password is incorrect."""
        url = reverse('users-change-password', kwargs={'pk': self.user.pk})
        self.set_credentials(self.user_token.key)
        response = self.client.post(url, data={
            "old_password": "wrongpassword",
            "new_password": "secret123456",
            "confirm_password": "secret123456"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Old password is incorrect.", response.data["detail"])

    def test_password_change_with_non_matching_new_passwords(self):
        """Ensure error is returned if new passwords do not match."""
        url = reverse('users-change-password', kwargs={'pk': self.user.pk})
        self.set_credentials(self.user_token.key)
        response = self.client.post(url, data={
            "old_password": "secret1234",
            "new_password": "secret123456",
            "confirm_password": "differentpassword"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("New passwords do not match.", response.data["detail"])


class TestTokenEndpoints(UserSetupMixin, APITestCase):
    """Test cases for token generation and validation."""

    def test_token_retrieval_with_correct_credentials(self):
        """Ensure token is retrieved with correct credentials."""
        data = {"username": self.user.email, "password": "secret1234"}
        token_url = reverse('basic_token')
        response = self.client.post(token_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_token_retrieval_with_incorrect_credentials(self):
        """Ensure token is not retrieved with incorrect credentials."""
        data = {"email": self.user.email, "password": "wrongpassword"}
        token_url = reverse('basic_token')
        response = self.client.post(token_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
