from rest_framework import status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from common.decorators import custom_action, custom_response, staff_required
from common.permissions import IsStaff
from common.viewsets import ResponseViewset
from common.pagination import GenericPagination

from .models import Order
from .exceptions import InvalidUserData
from .serializers import OrderSerializer, PurchaseSerializer


class OrderViewSet(ResponseViewset):
    queryset = Order.objects.all().order_by('-created', '-slug')
    pagination_class = GenericPagination
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter,  DjangoFilterBackend]
    lookup_field = 'slug'

    @custom_response
    def create(self, request, *args, **kwargs):
        if str(request.user.slug) != request.data.get('user_id', None):
            raise InvalidUserData()
        serializer = PurchaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'data': serializer.data,
            'messages': ['Order created successfully.']
        }, status=status.HTTP_201_CREATED)
    
    @custom_response
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user.slug != request.user.slug:
            self.permission_classes += [IsStaff]

        self.check_permissions(request)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @staff_required
    @custom_response
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    