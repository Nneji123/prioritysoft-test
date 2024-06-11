from subprocess import run

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification

User = get_user_model()


@shared_task
def backup_database():
    run(["python", "manage.py", "dbbackup"])


@shared_task
def send_notification():
    try:
        users = User.objects.all()
        for user in users:
            print(user)
            devices = FCMDevice.objects.filter(user=user)
            for device in devices:
                print(device)
                device.send_message(
                    Message(
                        notification=Notification(
                            title="This is a title",
                            body="This is the body",
                            image="data:image/png;base64,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",
                        ),
                    )
                )
    except User.DoesNotExist:
        print("User does not exist!")
