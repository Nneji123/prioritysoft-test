# inventory/utils.py

from rest_framework.response import Response


def format_response(responseCode: int, message: str, data=None):
    if data is None:
        data = {}
    return Response({"responseCode": responseCode, "message": message, "data": data})
