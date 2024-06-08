from .constants import ErrorCode
from common.exceptions import PermissionDenied, NotFound, BadRequest, NotAuthenticated

class DuplicatedProductIDs(BadRequest):
    default_detail = ErrorCode.DUPLICATED_IDS
    
class InvalidUserData(PermissionDenied):
    default_detail = ErrorCode.INVALID_USER_DATA
    
class FiledToCreateOrder(PermissionDenied):
    default_detail = ErrorCode.FAILED_TO_CREATE_ORDER

