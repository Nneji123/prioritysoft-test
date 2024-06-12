# inventory/views.py
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from .models import Item, Supplier
from .pagination import CustomPagination
from .permissions import IsAdminOrReadOnly
from .schema import item_schema, supplier_schema
from .serializers import ItemSerializer, SupplierSerializer
from .utils import format_response


@item_schema
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    ordering_fields = ["date_added", "name", "price"]
    ordering = ["date_added"]
    filterset_fields = ["name", "price"]
    search_fields = ["name", "description"]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return format_response(200, "Items retrieved successfully", response.data)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return format_response(200, "Item retrieved successfully", response.data)

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return format_response(200, "Item created successfully", response.data)
        except ValidationError as e:
            return format_response(400, "Validation error", e.detail)

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            return format_response(200, "Item updated successfully", response.data)
        except ValidationError as e:
            return format_response(400, "Validation error", e.detail)

    def destroy(self, request, *args, **kwargs):
        try:
            super().destroy(request, *args, **kwargs)
            return format_response(204, "Item deleted successfully")
        except Item.DoesNotExist:
            return format_response(404, "Item not found")


@supplier_schema
class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    ordering_fields = ["date_added", "name", "phone_number"]
    ordering = ["date_added"]
    filterset_fields = ["name"]
    search_fields = ["name", "email_address", "phone_number"]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return format_response(200, "Suppliers retrieved successfully", response.data)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return format_response(200, "Supplier retrieved successfully", response.data)

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return format_response(200, "Supplier created successfully", response.data)
        except ValidationError as e:
            return format_response(400, "Validation error", e.detail)

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            return format_response(
                200, "Supplier information updated successfully", response.data
            )
        except ValidationError as e:
            return format_response(400, "Validation error", e.detail)

    def destroy(self, request, *args, **kwargs):
        try:
            super().destroy(request, *args, **kwargs)
            return format_response(204, "Supplier deleted successfully")
        except Supplier.DoesNotExist:
            return format_response(404, "Supplier not found")
