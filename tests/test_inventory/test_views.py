import pytest
from rest_framework.test import APIClient
from rest_framework import status
from .models import Item, Supplier

@pytest.fixture
def admin_user(db):
    return User.objects.create_user(username='admin', password='password', is_staff=True, is_superuser=True)

@pytest.fixture
def normal_user(db):
    return User.objects.create_user(username='user', password='password')

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def supplier(db):
    return Supplier.objects.create(
        name="Test Supplier",
        email_address="test@supplier.com",
        phone_number="+1234567890"
    )

@pytest.fixture
def item(db):
    return Item.objects.create(
        name="Test Item",
        description="This is a test item.",
        price=9.99
    )

# Test ItemViewSet
@pytest.mark.django_db
def test_list_items(api_client, item):
    response = api_client.get('/items/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['message'] == "Items retrieved successfully"

@pytest.mark.django_db
def test_create_item(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    data = {
        "name": "New Item",
        "description": "A new item",
        "price": 19.99
    }
    response = api_client.post('/items/', data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['message'] == "Item created successfully"

@pytest.mark.django_db
def test_create_item_permission_denied(api_client, normal_user):
    api_client.force_authenticate(user=normal_user)
    data = {
        "name": "New Item",
        "description": "A new item",
        "price": 19.99
    }
    response = api_client.post('/items/', data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_retrieve_item(api_client, item):
    response = api_client.get(f'/items/{item.id}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['message'] == "Item retrieved successfully"

@pytest.mark.django_db
def test_update_item(api_client, admin_user, item):
    api_client.force_authenticate(user=admin_user)
    data = {
        "name": "Updated Item",
        "description": "Updated description",
        "price": 29.99
    }
    response = api_client.put(f'/items/{item.id}/', data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['message'] == "Item updated successfully"

@pytest.mark.django_db
def test_delete_item(api_client, admin_user, item):
    api_client.force_authenticate(user=admin_user)
    response = api_client.delete(f'/items/{item.id}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT

# Test SupplierViewSet
@pytest.mark.django_db
def test_list_suppliers(api_client, supplier):
    response = api_client.get('/suppliers/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['message'] == "Suppliers retrieved successfully"

@pytest.mark.django_db
def test_create_supplier(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    data = {
        "name": "New Supplier",
        "email_address": "new@supplier.com",
        "phone_number": "+1234567890"
    }
    response = api_client.post('/suppliers/', data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['message'] == "Supplier created successfully"

@pytest.mark.django_db
def test_create_supplier_permission_denied(api_client, normal_user):
    api_client.force_authenticate(user=normal_user)
    data = {
        "name": "New Supplier",
        "email_address": "new@supplier.com",
        "phone_number": "+1234567890"
    }
    response = api_client.post('/suppliers/', data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_retrieve_supplier(api_client, supplier):
    response = api_client.get(f'/suppliers/{supplier.id}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['message'] == "Supplier retrieved successfully"

@pytest.mark.django_db
def test_update_supplier(api_client, admin_user, supplier):
    api_client.force_authenticate(user=admin_user)
    data = {
        "name": "Updated Supplier",
        "email_address": "updated@supplier.com",
        "phone_number": "+0987654321"
    }
    response = api_client.put(f'/suppliers/{supplier.id}/', data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['message'] == "Supplier information updated successfully"

@pytest.mark.django_db
def test_delete_supplier(api_client, admin_user, supplier):
    api_client.force_authenticate(user=admin_user)
    response = api_client.delete(f'/suppliers/{supplier.id}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT
  
