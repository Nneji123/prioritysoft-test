import pytest
from django.utils import timezone
from django.core.exceptions import ValidationError
from accounts.models import CustomUser, PasswordResetCode

@pytest.mark.django_db
class TestCustomUser:
    
    @pytest.fixture
    def user(self):
        return CustomUser.objects.create_user(
            email="testuser@example.com",
            password="password123",
            first_name="Test",
            last_name="User"
        )
    
    def test_create_user(self, user):
        assert CustomUser.objects.count() == 1
        assert user.email == "testuser@example.com"
    
    def test_read_user(self, user):
        retrieved_user = CustomUser.objects.get(email="testuser@example.com")
        assert retrieved_user.first_name == "Test"
        assert retrieved_user.last_name == "User"
    
    def test_update_user(self, user):
        user.first_name = "Updated"
        user.save()
        updated_user = CustomUser.objects.get(email="testuser@example.com")
        assert updated_user.first_name == "Updated"
    
    def test_delete_user(self, user):
        user.delete()
        assert CustomUser.objects.count() == 0
    
    def test_create_employee(self):
        employee = CustomUser.objects.create_employee(
            email="employee@example.com",
            password="password123"
        )
        assert employee.is_employee is True
        assert employee.is_admin is False
    
    def test_create_admin(self):
        admin = CustomUser.objects.create_admin(
            email="admin@example.com",
            password="password123"
        )
        assert admin.is_admin is True
        assert admin.is_staff is True

@pytest.mark.django_db
class TestPasswordResetCode:
    
    @pytest.fixture
    def user(self):
        return CustomUser.objects.create_user(
            email="testuser2@example.com",
            password="password123"
        )
    
    @pytest.fixture
    def password_reset_code(self, user):
        return PasswordResetCode.objects.create(
            user=user,
            code=1234,
            expires_at=timezone.now() + timezone.timedelta(hours=1)
        )
    
    def test_create_password_reset_code(self, password_reset_code):
        assert PasswordResetCode.objects.count() == 1
        assert password_reset_code.code == 1234
    
    def test_read_password_reset_code(self, password_reset_code):
        retrieved_code = PasswordResetCode.objects.get(id=password_reset_code.id)
        assert retrieved_code.code == 1234
    
    def test_update_password_reset_code(self, password_reset_code):
        password_reset_code.code = 4321
        password_reset_code.save()
        updated_code = PasswordResetCode.objects.get(id=password_reset_code.id)
        assert updated_code.code == 4321
    
    def test_delete_password_reset_code(self, password_reset_code):
        password_reset_code.delete()
        assert PasswordResetCode.objects.count() == 0
    
    def test_is_expired(self, password_reset_code):
        assert password_reset_code.is_expired() is False
        password_reset_code.expires_at = timezone.now() - timezone.timedelta(hours=1)
        password_reset_code.save()
        assert password_reset_code.is_expired() is True