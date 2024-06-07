from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout

from rest_framework import viewsets
from rest_framework.decorators import action


from .models import * 
from .serializers import *
from .exceptions import InvalidCredentials
from common.permissions import IsStaff


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('email')
    permission_classes = []
    serializer_class = UserSerializer
    lookup_field = 'slug'
    def create(self, request, *args, **kwargs):
        print("Hola")
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.permission_classes = [IsStaff]
        self.check_permissions(request)
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        self.permission_classes = [IsStaff]
        self.check_permissions(request)
        return super().retrieve(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        slug = kwargs.get('slug', None)
        if not hasattr(request.user, 'slug') or str(request.user.slug) != slug:
            self.permission_classes = [IsStaff]
            self.check_permissions(request)
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        slug = kwargs.get('slug', None)
        if not hasattr(request.user, 'slug') or str(request.user.slug) != slug:
            self.permission_classes = [IsStaff]
            self.check_permissions(request)
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({ 'deleted': True }, status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['POST'], detail=False, authentication_classes=[])
    def login(self, request, slug = None):
        serializer: UserAuthenticateSerializer = UserAuthenticateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(request, **serializer.validated_data)
        
        if not user:
            raise InvalidCredentials()

        login(request, user)
        serializer_response = self.get_serializer(user)
        return Response({'login': True, 'user': serializer_response.data}, status=status.HTTP_200_OK) 

    @action(methods=['POST'], detail=False, url_path='logout')
    def logout_user(self, request, slug = None):
        logout(request)
        return Response({'logout': True}, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False, url_path='is-logged') 
    def is_logged(self, request, *args, **kwargs):
        data = True

        if request.user.id == None:
            data = False
        return Response({ 'isLogged': data }, status=status.HTTP_200_OK)
    
    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated]) 
    def me(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
