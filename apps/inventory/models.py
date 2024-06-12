from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    email_address = models.EmailField()
    phone_number = PhoneNumberField(blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateField(auto_now_add=True)
    suppliers = models.ManyToManyField(Supplier, related_name="items")

    def __str__(self):
        return self.name
