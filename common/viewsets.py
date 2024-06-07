from rest_framework import viewsets
from common.decorators import custom_response


class ResponseViewset(viewsets.ModelViewSet):
    @custom_response
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @custom_response
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @custom_response
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @custom_response
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @custom_response
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @custom_response
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)