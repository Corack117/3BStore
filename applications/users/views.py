from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout

from rest_framework import viewsets

from .models import * 
from .serializers import *
from .exceptions import InvalidCredentials
from common.permissions import IsStaff
from common.decorators import custom_action, custom_response, staff_required


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('email')
    permission_classes = []
    serializer_class = UserSerializer
    lookup_field = 'slug'

    @custom_response
    @staff_required
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @custom_response
    @staff_required
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @custom_response    
    def update(self, request, *args, **kwargs):
        slug = kwargs.get('slug', None)
        self.permission_classes = [IsAuthenticated]
        if not hasattr(request.user, 'slug') or str(request.user.slug) != slug:
            self.permission_classes += [IsStaff]

        self.check_permissions(request)
        response = super().update(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            response.data['messages'] = ['User updated successfully.']
        return response
    
    @custom_response
    @staff_required
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({ 
            'deleted': True ,
            'messages': ['User deleted successfully.']
        }, status=status.HTTP_204_NO_CONTENT)
    
    @custom_action(methods=['POST'], detail=False, authentication_classes=[])
    def login(self, request, slug = None):
        serializer: UserAuthenticateSerializer = UserAuthenticateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(request, **serializer.validated_data)
        
        if not user:
            raise InvalidCredentials()

        login(request, user)
        serializer_response = self.get_serializer(user)
        return Response({
            'login': True, 
            'user': serializer_response.data,
            'messages': ['User logged in successfully.']
        }, status=status.HTTP_200_OK) 

    @custom_action(methods=['POST'], detail=False, url_path='logout')
    def logout_user(self, request, slug = None):
        logout(request)
        return Response({
            'logout': True,
            'messages': ['User logged out successfully.']
        }, status=status.HTTP_200_OK)

    @custom_action(methods=['GET'], detail=False, url_path='is-logged') 
    def is_logged(self, request, slug = None):
        data = True

        if request.user.id == None:
            data = False
        return Response({ 'isLogged': data }, status=status.HTTP_200_OK)
    
    @custom_action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated]) 
    def me(self, request, slug = None):
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
