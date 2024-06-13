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
        responses={
            200: OpenApiResponse(
                response=BaseResponseSerializer,
                examples=[
                    OpenApiExample(
                        name="ItemsListExample",
                        value={
                            "responseCode": 200,
                            "message": "Items retrieved successfully",
                            "data": [
                                {
                                    "id": 1,
                                    "name": "Item 1",
                                    "description": "Description 1",
                                    "price": "10.00",
                                    "date_added": "2024-06-10T00:00:00Z",
                                    "suppliers": [1, 2],
                                },
                                {
                                    "id": 2,
                                    "name": "Item 2",
                                    "description": "Description 2",
                                    "price": "20.00",
                                    "date_added": "2024-06-11T00:00:00Z",
                                    "suppliers": [2, 3],
                                },
                            ],
                        },
                    )
                ],
            )
        },
        extensions={
            "x-code-samples": get_code_samples(
                app_name="inventory", view_name="list_item_view"
            ),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve Item",
        description="Retrieve a single inventory item by ID.",
        responses={
            200: OpenApiResponse(
                response=BaseResponseSerializer,
                examples=[
                    OpenApiExample(
                        name="ItemRetrieveExample",
                        value={
                            "responseCode": 200,
                            "message": "Item retrieved successfully",
                            "data": {
                                "id": 1,
                                "name": "Item 1",
                                "description": "Description 1",
                                "price": "10.00",
                                "date_added": "2024-06-10T00:00:00Z",
                                "suppliers": [1, 2],
                            },
                        },
                    )
                ],
            )
        },
        extensions={
            "x-code-samples": get_code_samples(
                app_name="inventory", view_name="retrieve_item_view"
            ),
        },
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
                    "suppliers": [1, 2],
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
                                "name": "New Item",
                                "description": "A description of the new item",
                                "price": "29.99",
                                "date_added": "2024-06-13T00:00:00Z",
                                "suppliers": [1, 2],
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
        extensions={
            "x-code-samples": get_code_samples(
                app_name="inventory", view_name="create_item_view"
            ),
        },
    ),
    partial_update=extend_schema(
        summary="Partial Update Item",
        description="Update an existing inventory item.",
        request=ItemSerializer,
        examples=[
            OpenApiExample(
                name="PatchItemExample",
                value={
                    "name": "Updated Item",
                    "description": "An updated description of the item",
                    "price": "35.99",
                    "suppliers": [1, 3],
                },
                request_only=True,
            ),
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=BaseResponseSerializer,
                description="Item updated successfully",
                examples=[
                    OpenApiExample(
                        name="ItemUpdatedExample",
                        value={
                            "responseCode": 200,
                            "message": "Item updated successfully",
                            "data": {
                                "id": 1,
                                "name": "Updated Item",
                                "description": "An updated description of the item",
                                "price": "35.99",
                                "date_added": "2024-06-12T00:00:00Z",
                                "suppliers": [1, 3],
                            },
                        },
                    )
                ],
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=BaseResponseSerializer,
                examples=[
                    OpenApiExample(
                        name="ItemUpdateErrorExample",
                        value={
                            "responseCode": 400,
                            "message": "Validation error",
                            "data": {"detail": "Error details here"},
                        },
                    )
                ],
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=BaseResponseSerializer,
                examples=[
                    OpenApiExample(
                        name="ItemNotFoundExample",
                        value={
                            "responseCode": 404,
                            "message": "Item not found",
                            "data": {},
                        },
                    )
                ],
            ),
        },
        extensions={
            "x-code-samples": get_code_samples(
                app_name="inventory", view_name="update_item_view"
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
                                "suppliers": [1, 3],
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
        extensions={
            "x-code-samples": get_code_samples(
                app_name="inventory", view_name="delete_item_view"
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
                    "phone_number": "+2348056042384",
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
                                "phone_number": "+2348056042384",
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
                    "phone_number": "+2348056042384",
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
                                "phone_number": "+2348056042384",
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
