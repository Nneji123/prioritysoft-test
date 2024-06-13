# accounts/mixins.py

from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.response import Response


class CustomResponseMixin:
    def get_response(self, data, response_code=status.HTTP_200_OK, message="Success"):
        return Response(
            {
                "responseCode": response_code,
                "message": message,
                "data": data,
            },
            status=response_code,
        )

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        return self.get_error_response(
            response.data, response_code=response.status_code, message=str(exc)
        )

    def get_custom_error_message(self, errors):
        error_messages = []

        def extract_error_messages(errors):
            if isinstance(errors, list):
                for error in errors:
                    if isinstance(error, dict):
                        extract_error_messages(error)
                    else:
                        error_messages.append(str(error))
            elif isinstance(errors, dict):
                for field, error_detail in errors.items():
                    if isinstance(error_detail, list):
                        for detail in error_detail:
                            if isinstance(detail, ErrorDetail):
                                error_messages.append(f"{str(detail)}")
                            else:
                                error_messages.append(f"{str(detail)}")
                    else:
                        error_messages.append(f"{str(error_detail)}")
            else:
                error_messages.append(str(errors))

        extract_error_messages(errors)

        return "; ".join(error_messages)

    def get_error_response(self, errors, response_code=400, message=None):
        error_messages = []

        def extract_error_messages(errors):
            if isinstance(errors, list):
                for error in errors:
                    if isinstance(error, dict):
                        extract_error_messages(error)
                    else:
                        error_messages.append(str(error))
            elif isinstance(errors, dict):
                for field, error_detail in errors.items():
                    if isinstance(error_detail, list):
                        for detail in error_detail:
                            if isinstance(detail, ErrorDetail):
                                error_messages.append(detail)
                            else:
                                error_messages.append(detail)
                    else:
                        error_messages.append(error_detail)
            else:
                error_messages.append(str(errors))

        extract_error_messages(errors)

        # Use custom message if provided, otherwise join extracted messages
        final_message = message if message else "; ".join(error_messages)

        return Response(
            {"responseCode": response_code, "message": final_message, "data": {}},
            status=response_code,
        )
