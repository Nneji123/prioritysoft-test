import sys

from loguru import logger

# Remove all handlers associated with the root logger object.
for handler in logger._core.handlers.values():
    logger.remove(handler)

logger.add(
    sys.stdout, format="{time} {level} {message}", filter="my_module", level="INFO"
)


def loguru_logging_middleware(get_response):
    def middleware(request):
        logger.info(f"Request: {request.method} {request.get_full_path()}")
        response = get_response(request)
        logger.info(f"Response: {response.status_code} {response.content}")
        return response

    return middleware
