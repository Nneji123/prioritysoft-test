import pytest
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from datetime import datetime
from inventory.models import Supplier
from inventory.tasks import send_new_supplier_notification


@pytest.fixture
def mock_send_mail(mocker):
    return mocker.patch('django.core.mail.send_mail')


@pytest.mark.django_db
def test_send_new_supplier_notification(celery_worker, mock_send_mail):
    User = get_user_model()
    user = User.objects.create_user(email='testuser@example.com', password='password123', is_active=True)
    supplier = Supplier.objects.create(
        name="Test Supplier",
        email_address="test@supplier.com",
        phone_number="+1234567890"
    )

    send_new_supplier_notification.delay(supplier.id)

    mock_send_mail.assert_called_once()
    assert mock_send_mail.call_args[0][0] == "New Supplier Created"
    assert "Test Supplier" in mock_send_mail.call_args[0][1]
    assert "testuser@example.com" in mock_send_mail.call_args[0][3]
  
