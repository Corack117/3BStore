from functools import wraps
import json
from django.http import FileResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from common.permissions import IsStaff
from common.response_model import CustomResponse

def custom_action(methods=None, detail=None, url_path=None, url_name=None, **kwargs):
    """
    Mark a ViewSet method as a routable action.

    `@action`-decorated functions will be endowed with a `mapping` property,
    a `MethodMapper` that can be used to add additional method-based behaviors
    on the routed action.

    :param methods: A list of HTTP method names this action responds to.
                    Defaults to GET only.
    :param detail: Required. Determines whether this action applies to
                   instance/detail requests or collection/list requests.
    :param url_path: Define the URL segment for this action. Defaults to the
                     name of the method decorated.
    :param url_name: Define the internal (`reverse`) URL name for this action.
                     Defaults to the name of the method decorated with underscores
                     replaced with dashes.
    :param kwargs: Additional properties to set on the view.  This can be used
                   to override viewset-level *_classes settings, equivalent to
                   how the `@renderer_classes` etc. decorators work for function-
                   based API views.
    """


    def decorator(func):
        @action(methods=methods, detail=detail, url_path=url_path, url_name=url_name, **kwargs)
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            return wrapper_function(self, request, func, *args, **kwargs)
        
        return wrapper
    return decorator


def custom_response(func):
    """
    Decorador personalizado para personalizar las respuestas de las acciones en un ViewSet.
    """
    def wrapper(self, request, *args, **kwargs):
        return wrapper_function(self, request, func, *args, **kwargs)
    
    return wrapper

def wrapper_function(self, request, func, *args, **kwargs):
    try:
        data = {
            "code": 200,
            "response": True
        }
        # Lógica de la acción personalizada
        result: Response | FileResponse= func(self, request, *args, **kwargs)
        if isinstance(result, FileResponse):
            return result

        data_result = result.data
        if isinstance(data_result, list):
            data_result = {'results': data_result}

        messages = None
        status_code = result.status_code
        if isinstance(data_result, dict):
            messages = data_result.pop('response_message', None)
        data.update({'data': data_result, 'messages': messages, 'code': status_code})
        response = CustomResponse(data=data)
        response.is_valid(raise_exception=True)

        return Response(response.data, status=result.status_code)
    except ValidationError as e:
        messages = e.detail if isinstance(e.detail, list) else [e.detail]
        data = {
            'code': e.status_code,
            'messages': messages
        }
        print(data)
        response = CustomResponse(data=data)
        response.is_valid(raise_exception=True)
        return Response(response.data, status=e.status_code)
    except Exception as e:
        data = {
            'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'messages': [str(e)]
        }
        response = CustomResponse(data=data)
        response.is_valid(raise_exception=True)
        return Response(response.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

def staff_required(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated, IsStaff]
        self.check_permissions(request)
        return func(self, request, *args, **kwargs)
    return wrapper