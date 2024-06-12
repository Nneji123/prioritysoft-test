# inventory/schema.py

from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
    extend_schema_view,
)
from rest_framework import status

from apps.core.utils import get_code_samples

from .serializers import BaseResponseSerializer, ItemSerializer, SupplierSerializer

item_schema = extend_schema_view(
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
                                "date_added": "2024-06-10T00:00:00Z",
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

supplier_schema = extend_schema_view(
    list=extend_schema(
        summary="List Suppliers",
        description="Retrieve a list of suppliers.",
        parameters=[
            OpenApiParameter(
                name="name",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Name filter",
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
                description="Search in name, email address, and phone number",
                required=False,
                type=OpenApiTypes.STR,
            ),
        ],
        responses={200: OpenApiResponse(response=BaseResponseSerializer)},
    ),
    retrieve=extend_schema(
        summary="Retrieve Supplier",
        description="Retrieve a single supplier by ID.",
        responses={200: OpenApiResponse(response=BaseResponseSerializer)},
    ),
    create=extend_schema(
        summary="Create Supplier",
        description="Create a new supplier. Only admins can perform this action.",
        request=SupplierSerializer,
        examples=[
            OpenApiExample(
                name="CreateSupplierExample",
                value={
                    "name": "New Supplier",
                    "email_address": "supplier@example.com",
                    "phone_number": "123-456-7890",
                },
                request_only=True,
            ),
        ],
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=BaseResponseSerializer,
                examples=[
                    OpenApiExample(
                        name="SupplierCreateSuccess",
                        value={
                            "responseCode": 200,
                            "message": "Supplier created successfully",
                            "data": {
                                "id": 1,
                                "name": "New Supplier",
                                "email_address": "supplier@example.com",
                                "phone_number": "123-456-7890",
                                "date_added": "2024-06-10T00:00:00Z",
                            },
                        },
                    )
                ],
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=BaseResponseSerializer,
                examples=[
                    OpenApiExample(
                        name="SupplierCreateError",
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
        summary="Update Supplier",
        description="Update an existing supplier. Only admins can perform this action.",
        request=SupplierSerializer,
        examples=[
            OpenApiExample(
                name="UpdateSupplierExample",
                value={
                    "name": "Updated Supplier",
                    "email_address": "updatedsupplier@example.com",
                    "phone_number": "123-456-7890",
                },
                request_only=True,
            ),
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=BaseResponseSerializer,
                examples=[
                    OpenApiExample(
                        name="SupplierUpdateSuccess",
                        value={
                            "responseCode": 200,
                            "message": "Supplier information updated successfully",
                            "data": {
                                "id": 1,
                                "name": "Updated Supplier",
                                "email_address": "updatedsupplier@example.com",
                                "phone_number": "123-456-7890",
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
                        name="SupplierUpdateError",
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
        summary="Delete Supplier",
        description="Delete a supplier. Only admins can perform this action.",
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                response=BaseResponseSerializer,
                examples=[
                    OpenApiExample(
                        name="SupplierDeleteSuccess",
                        value={
                            "responseCode": 204,
                            "message": "Supplier deleted successfully",
                            "data": {},
                        },
                    )
                ],
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=BaseResponseSerializer,
                examples=[
                    OpenApiExample(
                        name="SupplierDeleteError",
                        value={
                            "responseCode": 404,
                            "message": "Supplier not found",
                            "data": {},
                        },
                    )
                ],
            ),
        },
    ),
)
