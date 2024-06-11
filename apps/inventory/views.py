from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
    extend_schema_view,
)

# inventory/views.py
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Item, Supplier
from .pagination import CustomPagination
from .permissions import IsAdminUser, IsEmployeeUser
from .serializers import BaseResponseSerializer, ItemSerializer, SupplierSerializer


def format_response(responseCode, message, data=None):
    if data is None:
        data = {}
    return Response({"responseCode": responseCode, "message": message, "data": data})


@extend_schema_view(
    list=extend_schema(
        summary="List Items",
        description="Retrieve a list of inventory items.",
        parameters=[
            OpenApiParameter(
                name="name",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Name filter",
            ),
            OpenApiParameter(
                name="price",
                type=OpenApiTypes.DECIMAL,
                location=OpenApiParameter.QUERY,
                description="Price filter",
            ),
            OpenApiParameter(
                name="limit",
                description="Number of results to return per page.",
                required=False,
                type=OpenApiTypes.INT,
            ),
            OpenApiParameter(
                name="offset",
                description="The initial index from which to return the results.",
                required=False,
                type=OpenApiTypes.INT,
            ),
            OpenApiParameter(
                name="ordering",
                description="Ordering fields",
                required=False,
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="search",
                description="Search in name and description",
                required=False,
                type=OpenApiTypes.STR,
            ),
        ],
        responses={200: OpenApiResponse(response=BaseResponseSerializer)},
    ),
    retrieve=extend_schema(
        summary="Retrieve Item",
        description="Retrieve a single inventory item by ID.",
        responses={200: OpenApiResponse(response=BaseResponseSerializer)},
    ),
    create=extend_schema(
        summary="Create Item",
        description="Create a new inventory item.",
        request=ItemSerializer,
        examples=[
            OpenApiExample(
                name="CreateItemExample",
                value={
                    "name": "New Item",
                    "description": "A description of the new item",
                    "price": "29.99",
                    "date_added": "2023-06-10T00:00:00Z",
                },
                request_only=True,
            ),
        ],
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=BaseResponseSerializer,
                examples=[
                    OpenApiExample(
                        name="ItemCreateSuccess",
                        value={
                            "responseCode": 201,
                            "message": "Item created successfully",
                            "data": {
                                "id": 1,
                                "name": "Example Item",
                                "description": "This is an example item.",
                                "price": "10.00",
                                "date_added": "2023-06-10T00:00:00Z",
                            },
                        },
                    )
                ],
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=BaseResponseSerializer,
                examples=[
                    OpenApiExample(
                        name="ItemCreateError",
                        value={
                            "responseCode": 400,
                            "message": "Validation error",
                            "data": {},
                        },
                    )
                ],
            ),
        },
    ),
    update=extend_schema(
        summary="Update Item",
        description="Update an existing inventory item.",
        request=ItemSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=BaseResponseSerializer,
                examples=[
                    OpenApiExample(
                        name="ItemUpdateSuccess",
                        value={
                            "responseCode": 200,
                            "message": "Item updated successfully",
                            "data": {
                                "id": 1,
                                "name": "Updated Item",
                                "description": "This is an updated item.",
                                "price": "20.00",
                                "date_added": "2023-06-10T00:00:00Z",
                            },
                        },
                    )
                ],
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=BaseResponseSerializer,
                examples=[
                    OpenApiExample(
                        name="ItemUpdateError",
                        value={
                            "responseCode": 400,
                            "message": "Validation error",
                            "data": {},
                        },
                    )
                ],
            ),
        },
    ),
    destroy=extend_schema(
        summary="Delete Item",
        description="Delete an inventory item.",
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                response=BaseResponseSerializer,
                examples=[
                    OpenApiExample(
                        name="ItemDeleteSuccess",
                        value={
                            "responseCode": 204,
                            "message": "Item deleted successfully",
                            "data": {},
                        },
                    )
                ],
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=BaseResponseSerializer,
                examples=[
                    OpenApiExample(
                        name="ItemDeleteError",
                        value={
                            "responseCode": 404,
                            "message": "Item not found",
                            "data": {},
                        },
                    )
                ],
            ),
        },
    ),
)
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
        return format_response(100, "Items retrieved successfully", response.data)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return format_response(100, "Item retrieved successfully", response.data)

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return format_response(100, "Item created successfully", response.data)
        except ValidationError as e:
            return format_response(400, "Validation error", e.detail)

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            return format_response(100, "Item updated successfully", response.data)
        except ValidationError as e:
            return format_response(400, "Validation error", e.detail)

    def destroy(self, request, *args, **kwargs):
        try:
            super().destroy(request, *args, **kwargs)
            return format_response(204, "Item deleted successfully")
        except Item.DoesNotExist:
            return format_response(404, "Item not found")


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
