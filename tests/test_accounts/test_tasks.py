import pytest
from django.core.mail import send_mail
from unittest.mock import patch
from accounts.tasks import send_password_reset_email

@pytest.mark.django_db
def test_send_password_reset_email(settings, celery_worker):
    settings.EMAIL_HOST_USER = "from@example.com"
    
    to_email = "to@example.com"
    code = 1234

    with patch("django.core.mail.send_mail") as mock_send_mail:
        send_password_reset_email.delay(to_email, code)
        celery_worker.ensure_task_accepted()
        celery_worker.ensure_task_accepted()  # Ensure task was sent to worker
        
        mock_send_mail.assert_called_once_with(
            "Password Reset Requested",
            f"Your password reset code is: {code}",
            "from@example.com",
            [to_email],
            html_message=mock_send_mail.call_args[1]["html_message"]
        )