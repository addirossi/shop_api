from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from order.models import Order
from order.serializers import OrderSerializer, OrderListSerializer


class OrderViewSet(CreateModelMixin,
                   ListModelMixin,
                   RetrieveModelMixin,
                   GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)

    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()
        if self.action == 'list':
            serializer_class = OrderListSerializer
        return serializer_class
