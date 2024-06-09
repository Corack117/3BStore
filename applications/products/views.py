from rest_framework import status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from common.decorators import custom_action, custom_response, staff_required
from common.permissions import IsStaff
from common.viewsets import ResponseViewset
from common.pagination import GenericPagination

from .models import Product
from .serializers import AddStockSerializer, ProductSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny



class ProductViewSet(ResponseViewset):
    queryset = Product.objects.all().order_by('-created', 'sku')
    pagination_class = GenericPagination
    permission_classes = []
    serializer_class = ProductSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter,  DjangoFilterBackend]
    lookup_field = 'sku'

    @staff_required
    def create(self, request, *args, **kwargs):
        response =  super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            response.data['messages'] = ['Product created successfully.']
        return response

    @staff_required    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            response.data['messages'] = ['Product updated successfully.']
        return response
    
    def list(self, request, *args, **kwargs):
        self.permission_classes = []
        self.check_permissions(request)
        return super().list(request, *args, **kwargs)

    @staff_required
    @custom_response   
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({ 
            'deleted': True ,
            'response_message': ['Product deleted successfully.']
        }, status=status.HTTP_204_NO_CONTENT)
    
    @staff_required
    @custom_action(methods=['PATCH'], detail=False, url_path='add-to-inventory')
    def add_to_inventory(self, request, sku = None):
        product = self.get_object()
        serializer = AddStockSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            **serializer.data,
            'response_message': ['Stock added successfully.']
        }, status=status.HTTP_200_OK)
        