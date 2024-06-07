from .constants import ErrorCode
from common.exceptions import PermissionDenied, NotFound, BadRequest, NotAuthenticated

class InvalidCredentials(PermissionDenied):
    default_detail = ErrorCode.INVALID_CREDENTIALS
