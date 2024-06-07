from rest_framework import status
from rest_framework.exceptions import ValidationError

class PermissionDenied(ValidationError):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Permission denied"

class NotFound(ValidationError):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Resource not found"

class BadRequest(ValidationError):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Bad Request"

class NotAuthenticated(ValidationError):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "User not authenticated"
