import pytest
from rest_framework.test import APIRequestFactory
from django.contrib.auth import get_user_model
from rest_framework.exceptions import Throttled
from accounts.throttles import PasswordResetThrottle, PasswordChangeThrottle

User = get_user_model()

@pytest.mark.django_db
class TestPasswordResetThrottle:
    
    @pytest.fixture
    def user(self):
        return User.objects.create_user(email="testuser@example.com", password="password123")
    
    def test_throttle_authenticated_user(self, user):
        factory = APIRequestFactory()
        request = factory.post("/password-reset/")
        request.user = user

        throttle = PasswordResetThrottle()

        # Allow first request
        assert throttle.allow_request(request, None) is True

        # Exceed rate limit
        for _ in range(10):
            throttle.allow_request(request, None)
        
        with pytest.raises(Throttled):
            throttle.allow_request(request, None)

    def test_throttle_anonymous_user(self):
        factory = APIRequestFactory()
        request = factory.post("/password-reset/")
        request.user = User()
        throttle = PasswordResetThrottle()

        # Allow first request
        assert throttle.allow_request(request, None) is True

        # Exceed rate limit
        for _ in range(10):
            throttle.allow_request(request, None)
        
        with pytest.raises(Throttled):
            throttle.allow_request(request, None)


@pytest.mark.django_db
class TestPasswordChangeThrottle:
    
    @pytest.fixture
    def user(self):
        return User.objects.create_user(email="testuser@example.com", password="password123")
    
    def test_throttle_authenticated_user(self, user):
        factory = APIRequestFactory()
        request = factory.post("/password-change/")
        request.user = user

        throttle = PasswordChangeThrottle()

        # Allow first request
        assert throttle.allow_request(request, None) is True

        # Exceed rate limit
        for _ in range(10):
            throttle.allow_request(request, None)
        
        with pytest.raises(Throttled):
            throttle.allow_request(request, None)
    
    def test_throttle_anonymous_user(self):
        factory = APIRequestFactory()
        request = factory.post("/password-change/")
        request.user = User()
        throttle = PasswordChangeThrottle()

        # Allow first request
        assert throttle.allow_request(request, None) is True

        # Exceed rate limit
        for _ in range(10):
            throttle.allow_request(request, None)
        
        with pytest.raises(Throttled):
            throttle.allow_request(request, None)