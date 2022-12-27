from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from model_bakery import baker
from parameterized import parameterized

from spell.models import User


# Create your tests here.
class BaseTest(TestCase):
    def setUp(self):
        """
        Setup API client with authentication
        """
        self.client = APIClient()
        self.user = baker.make(User, username="setupuser")


class RegisterViewTestCase(BaseTest):
    @parameterized.expand(["GET", "PUT", "PATCH", "DELETE"])
    def test_register_not_allowed_methods(self, method):
        response = self.client.generic(method=method, path="/api/spell/register/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_register_user(self):
        """
        Should be possible to register a user
        """
        new_user_data = {
            "username": "test",
            "password": "test",
            "email": "test@test.com",
            "first_name": "test",
            "last_name": "test",
        }
        response = self.client.post(path="/api/spell/register/", data=new_user_data)
        new_user = User.objects.last()

        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(
            new_user_data["password"], new_user.password
        )  # Assert password has been encrypted


class AuthenticationTestCase(BaseTest):
    def test_invalid_user_credentials(self):
        response = self.client.post(
            path="/api/spell/token/",
            data={"username": "invalid_username", "password": "invalid_password"},
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("access", response.json())

    def test_cant_auth_with_empty_password(self):
        response = self.client.post(
            path="/api/spell/token/", data={"username": "invalid_username"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual({"password": ["This field is required."]}, response.json())

    def test_success_get_user_access_token(self):
        self.user.set_password("pass")
        self.user.save()

        response = self.client.post(
            path="/api/spell/token/", data={"username": "setupuser", "password": "pass"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.json())


class UserViewTestCase(BaseTest):
    def test_patch_update_user(self):
        """
        Should be possible to update the authenticated user data
        """
        self.client.force_authenticate(user=self.user)
        updated_user_data = {"first_name": "update_test"}
        response = self.client.patch(
            path=f"/api/spell/users/{self.user.id}/", data=updated_user_data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_user_data["first_name"], response.json()["first_name"])

    def test_delete_user(self):
        """
        Should be possible to update the authenticated user
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(path=f"/api/spell/users/{self.user.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.exists())
