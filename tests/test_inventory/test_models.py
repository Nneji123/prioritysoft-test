import pytest
from django.db import IntegrityError
from datetime import date
from apps.inventory.models import Supplier, Item

@pytest.mark.django_db
def test_supplier_creation():
    supplier = Supplier.objects.create(
        name="Test Supplier",
        email_address="test@supplier.com",
        phone_number="+1234567890"
    )
    assert supplier.name == "Test Supplier"
    assert supplier.email_address == "test@supplier.com"
    assert str(supplier.phone_number) == "+1234567890"
    assert supplier.date_added == date.today()

@pytest.mark.django_db
def test_item_creation():
    item = Item.objects.create(
        name="Test Item",
        description="This is a test item.",
        price=9.99
    )
    assert item.name == "Test Item"
    assert item.description == "This is a test item."
    assert item.price == 9.99
    assert item.date_added == date.today()

@pytest.mark.django_db
def test_item_supplier_relationship():
    supplier = Supplier.objects.create(
        name="Test Supplier",
        email_address="test@supplier.com",
        phone_number="+1234567890"
    )
    item = Item.objects.create(
        name="Test Item",
        description="This is a test item.",
        price=9.99
    )
    item.suppliers.add(supplier)

    # Read test
    assert supplier in item.suppliers.all()
    assert item in supplier.items.all()

    # Update test (modify supplier details)
    supplier.name = "Updated Supplier"
    supplier.save()
    assert Supplier.objects.get(pk=supplier.pk).name == "Updated Supplier"

    # Delete test (remove supplier)
    supplier.delete()
    assert Supplier.objects.filter(pk=supplier.pk).count() == 0

@pytest.mark.django_db
def test_supplier_str():
    supplier = Supplier.objects.create(
        name="Test Supplier",
        email_address="test@supplier.com",
        phone_number="+1234567890"
    )
    assert str(supplier) == "Test Supplier"

@pytest.mark.django_db
def test_item_str():
    item = Item.objects.create(
        name="Test Item",
        description="This is a test item.",
        price=9.99
    )
    assert str(item) == "Test Item"
    
