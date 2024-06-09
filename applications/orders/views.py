import json
from rest_framework import status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from applications.orders.utils import convert_bson_dates
from common.decorators import custom_action, custom_response, staff_required
from common.permissions import IsStaff
from common.viewsets import ResponseViewset
from common.pagination import GenericPagination

from .models import Order
from .mongo_models import PurchaseMongo
from .exceptions import InvalidUserData
from .serializers import OrderSerializer, PurchaseSerializer, TicketSerializer


class OrderViewSet(ResponseViewset):
    queryset = Order.objects.all().select_related('user').order_by('-created', '-slug')
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
            **serializer.data,
            'response_message': ['Order created successfully.']
        }, status=status.HTTP_201_CREATED)
    
    @custom_response
    def retrieve(self, request, *args, **kwargs):
        instance: Order = self.get_object()
        if instance.user.slug != request.user.slug:
            self.permission_classes += [IsStaff]

        self.check_permissions(request)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @staff_required
    @custom_response
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @custom_action(methods=['GET'], detail=True)
    def ticket(self, request, slug=None):
        instance: Order = self.get_object()
        if instance.user.slug != request.user.slug:
            self.permission_classes += [IsStaff]

        self.check_permissions(request)
        purchase = PurchaseMongo.objects.get(purchase_id=str(instance.slug), user_id=str(instance.user.slug))
        purchase_data = purchase.to_mongo().to_dict()
        purchase_data = convert_bson_dates(purchase_data)
        serializer = TicketSerializer(data=purchase_data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @staff_required
    @custom_action(methods=['GET'], detail=False, url_path='tickets')
    def get_all_tickets(self, request):
        query = PurchaseMongo.objects.all()
        page = self.paginate_queryset(query)
        if page is not None:
            purchases_data = [convert_bson_dates(purchase.to_mongo().to_dict()) for purchase in query]
            serializer = TicketSerializer(data=purchases_data, many=True)
            serializer.is_valid(raise_exception=True)
            return self.get_paginated_response(serializer.data)
        
        purchases_data = [convert_bson_dates(purchase.to_mongo().to_dict()) for purchase in query]
        serializer = TicketSerializer(data=purchases_data, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)