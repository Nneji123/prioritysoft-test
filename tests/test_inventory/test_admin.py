import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client
from apps.inventory.models import Supplier, Item

@pytest.fixture
def admin_user(db):
    return get_user_model().objects.create_superuser(username='admin', email='admin@example.com', password='password')

@pytest.fixture
def normal_user(db):
    return get_user_model().objects.create_user(username='user', email='user@example.com', password='password')

@pytest.fixture
def client():
    return Client()

@pytest.mark.django_db
def test_supplier_admin_list_display(admin_user, client):
    client.login(username='admin', password='password')
    response = client.get(reverse('admin:inventory_supplier_changelist'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_supplier_admin_permissions(admin_user, normal_user, client):
    client.login(username='user', password='password')
    response = client.get(reverse('admin:inventory_supplier_add'))
    assert response.status_code == 403

    client.login(username='admin', password='password')
    response = client.get(reverse('admin:inventory_supplier_add'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_item_admin_list_display(admin_user, client):
    client.login(username='admin', password='password')
    response = client.get(reverse('admin:inventory_item_changelist'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_item_admin_add(admin_user, client):
    client.login(username='admin', password='password')
    response = client.get(reverse('admin:inventory_item_add'))
    assert response.status_code == 200
  
