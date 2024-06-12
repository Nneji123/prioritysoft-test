import pytest
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()

@pytest.mark.django_db
class TestCustomLoginView:

    @pytest.fixture
    def create_user(self):
        def make_user(**kwargs):
            return User.objects.create_user(**kwargs)
        return make_user

    def test_login_success(self, create_user):
        user = create_user(email="testuser@example.com", password="password123")
        client = APIClient()
        url = reverse('login')  # Make sure this URL name matches your URLconf
        response = client.post(url, {"email": user.email, "password": "password123"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["responseCode"] == status.HTTP_200_OK
        assert response.data["message"] == "Login Successful"

    def test_login_failure(self, create_user):
        user = create_user(email="testuser@example.com", password="password123")
        client = APIClient()
        url = reverse('login')  # Make sure this URL name matches your URLconf
        response = client.post(url, {"email": user.email, "password": "wrongpassword"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["responseCode"] == status.HTTP_400_BAD_REQUEST
        assert response.data["message"] == "Unable to log in with provided credentials."

@pytest.mark.django_db
class TestCustomPasswordChangeView:

    @pytest.fixture
    def create_user(self):
        def make_user(**kwargs):
            return User.objects.create_user(**kwargs)
        return make_user

    def test_password_change_success(self, create_user):
        user = create_user(email="testuser@example.com", password="password123")
        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse('password_change')  # Make sure this URL name matches your URLconf
        response = client.post(url, {
            "old_password": "password123",
            "new_password1": "newpassword123",
            "new_password2": "newpassword123"
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.data["responseCode"] == status.HTTP_200_OK
        assert response.data["message"] == "Password changed successfully"

    def test_password_change_failure(self, create_user):
        user = create_user(email="testuser@example.com", password="password123")
        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse('password_change')  # Make sure this URL name matches your URLconf
        response = client.post(url, {
            "old_password": "wrongpassword",
            "new_password1": "newpassword123",
            "new_password2": "newpassword123"
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["responseCode"] == status.HTTP_400_BAD_REQUEST
        assert "Unable to log in with provided credentials." in response.data["message"]


@pytest.mark.django_db
class TestCustomPasswordResetConfirmView:

    @pytest.fixture
    def create_user(self):
        def make_user(**kwargs):
            return User.objects.create_user(**kwargs)
        return make_user

    @pytest.fixture
    def create_reset_code(self, create_user):
        user = create_user(email="testuser@example.com", password="password123")
        from accounts.models import PasswordResetCode
        code = PasswordResetCode.objects.create(
            user=user,
            code=1234,
            expires_at=timezone.now() + timedelta(minutes=5)
        )
        return user, code

    def test_password_reset_confirm_success(self, create_reset_code):
        user, code = create_reset_code
        client = APIClient()
        url = reverse('password_reset_confirm')  # Make sure this URL name matches your URLconf
        response = client.post(url, {
            "email": user.email,
            "code": code.code,
            "new_password1": "newpassword123",
            "new_password2": "newpassword123"
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.data["responseCode"] == status.HTTP_200_OK
        assert response.data["message"] == "Password reset confirmation successful"

    def test_password_reset_confirm_failure(self, create_reset_code):
        user, code = create_reset_code
        client = APIClient()
        url = reverse('password_reset_confirm')  # Make sure this URL name matches your URLconf
        response = client.post(url, {
            "email": user.email,
            "code": 9999,  # Incorrect code
            "new_password1": "newpassword123",
            "new_password2": "newpassword123"
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["responseCode"] == status.HTTP_400_BAD_REQUEST
        assert "Invalid code." in response.data["message"]

@pytest.mark.django_db
class TestCustomPasswordResetView:

    @pytest.fixture
    def create_user(self):
        def make_user(**kwargs):
            return User.objects.create_user(**kwargs)
        return make_user

    def test_password_reset_success(self, create_user, settings):
        user = create_user(email="testuser@example.com", password="password123")
        client = APIClient()
        url = reverse('password_reset')  # Make sure this URL name matches your URLconf
        with patch('accounts.tasks.send_password_reset_email.delay') as mock_send_mail:
            response = client.post(url, {"email": user.email})
            assert response.status_code == status.HTTP_200_OK
            assert response.data["responseCode"] == status.HTTP_200_OK
            assert response.data["message"] == "Password reset email sent successfully"
            mock_send_mail.assert_called_once_with(user.email, ANY)  # Check if task was called

    def test_password_reset_failure(self, create_user):
        client = APIClient()
        url = reverse('password_reset')  # Make sure this URL name matches your URLconf
        response = client.post(url, {"email": "nonexistent@example.com"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["responseCode"] == status.HTTP_400_BAD_REQUEST
        assert "The provided email address does not belong to any account." in response.data["message"]