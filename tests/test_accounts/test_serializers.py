import pytest
from datetime import timedelta
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient
from accounts.models import CustomUser, PasswordResetCode
from accounts.serializers import (
    CustomLoginSerializer,
    CustomUserSerializer,
    UserAuthMessageSerializer,
    UserAuthErrorSerializer,
    CustomPasswordChangeSerializer,
    CustomPasswordResetConfirmSerializer,
    CustomPasswordResetSerializer,
)

@pytest.mark.django_db
class TestCustomLoginSerializer:
    
    @pytest.fixture
    def valid_data(self):
        return {"email": "testuser@example.com", "password": "password123"}
    
    @pytest.fixture
    def user(self, valid_data):
        return CustomUser.objects.create_user(**valid_data)
    
    def test_valid_data(self, valid_data, user):
        serializer = CustomLoginSerializer(data=valid_data)
        assert serializer.is_valid()
        assert serializer.validated_data["email"] == "testuser@example.com"
    
    def test_missing_email(self):
        serializer = CustomLoginSerializer(data={"password": "password123"})
        assert not serializer.is_valid()
        assert "email" in serializer.errors
    
    def test_missing_password(self):
        serializer = CustomLoginSerializer(data={"email": "testuser@example.com"})
        assert not serializer.is_valid()
        assert "password" in serializer.errors


@pytest.mark.django_db
class TestCustomUserSerializer:
    
    @pytest.fixture
    def user(self):
        return CustomUser.objects.create_user(
            email="testuser@example.com",
            password="password123",
            first_name="Test",
            last_name="User"
        )
    
    def test_serializer(self, user):
        serializer = CustomUserSerializer(user)
        assert serializer.data["email"] == "testuser@example.com"
        assert serializer.data["first_name"] == "Test"
        assert serializer.data["last_name"] == "User"


@pytest.mark.django_db
class TestUserAuthMessageSerializer:
    
    def test_serializer(self):
        data = {
            "responseCode": "200",
            "message": "Success",
            "data": {"key": "value"}
        }
        serializer = UserAuthMessageSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.data == data


@pytest.mark.django_db
class TestUserAuthErrorSerializer:
    
    def test_serializer(self):
        data = {
            "responseCode": "400",
            "message": "Error",
            "data": {"key": "value"}
        }
        serializer = UserAuthErrorSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.data == data


@pytest.mark.django_db
class TestCustomPasswordChangeSerializer:
    
    @pytest.fixture
    def user(self):
        return CustomUser.objects.create_user(
            email="testuser@example.com",
            password="old_password"
        )
    
    def test_valid_data(self, user):
        serializer = CustomPasswordChangeSerializer(data={
            "old_password": "old_password",
            "new_password1": "new_password",
            "new_password2": "new_password"
        }, context={'request': Mock(user=user)})
        assert serializer.is_valid()
    
    def test_password_mismatch(self, user):
        serializer = CustomPasswordChangeSerializer(data={
            "old_password": "old_password",
            "new_password1": "new_password1",
            "new_password2": "new_password2"
        }, context={'request': Mock(user=user)})
        assert not serializer.is_valid()
        assert "new_password2" in serializer.errors


@pytest.mark.django_db
class TestCustomPasswordResetConfirmSerializer:
    
    @pytest.fixture
    def user(self):
        return CustomUser.objects.create_user(
            email="testuser@example.com",
            password="password123"
        )
    
    @pytest.fixture
    def reset_code(self, user):
        return PasswordResetCode.objects.create(
            user=user,
            code=1234,
            expires_at=timezone.now() + timedelta(minutes=5)
        )
    
    def test_valid_data(self, user, reset_code):
        serializer = CustomPasswordResetConfirmSerializer(data={
            "email": "testuser@example.com",
            "code": 1234,
            "new_password1": "new_password",
            "new_password2": "new_password"
        })
        assert serializer.is_valid()
    
    def test_invalid_code(self, user):
        serializer = CustomPasswordResetConfirmSerializer(data={
            "email": "testuser@example.com",
            "code": 9999,
            "new_password1": "new_password",
            "new_password2": "new_password"
        })
        assert not serializer.is_valid()
        assert "code" in serializer.errors
    
    def test_password_mismatch(self, user, reset_code):
        serializer = CustomPasswordResetConfirmSerializer(data={
            "email": "testuser@example.com",
            "code": 1234,
            "new_password1": "new_password1",
            "new_password2": "new_password2"
        })
        assert not serializer.is_valid()
        assert "non_field_errors" in serializer.errors
    
    def test_expired_code(self, user):
        reset_code = PasswordResetCode.objects.create(
            user=user,
            code=1234,
            expires_at=timezone.now() - timedelta(minutes=1)
        )
        serializer = CustomPasswordResetConfirmSerializer(data={
            "email": "testuser@example.com",
            "code": 1234,
            "new_password1": "new_password",
            "new_password2": "new_password"
        })
        assert not serializer.is_valid()
        assert "code" in serializer.errors


@pytest.mark.django_db
class TestCustomPasswordResetSerializer:
    
    @pytest.fixture
    def user(self):
        return CustomUser.objects.create_user(
            email="testuser@example.com",
            password="password123"
        )
    
    def test_valid_email(self, user):
        serializer = CustomPasswordResetSerializer(data={"email": "testuser@example.com"})
        assert serializer.is_valid()
    
    def test_invalid_email(self):
        serializer = CustomPasswordResetSerializer(data={"email": "nonexistent@example.com"})
        assert not serializer.is_valid()
        assert "email" in serializer.errors