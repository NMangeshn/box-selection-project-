from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Box, Order, Product
from .serializers import (
    BoxRecommendationSerializer,
    BoxSerializer,
    OrderSerializer,
    ProductSerializer,
)
from .services import recommend_box_for_order


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer


class BoxViewSet(viewsets.ModelViewSet):
    queryset = Box.objects.all().order_by('id')
    serializer_class = BoxSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = (
        Order.objects.prefetch_related('items__product')
        .all()
        .order_by('id')
    )
    serializer_class = OrderSerializer

    @action(detail=True, methods=['get'], url_path='recommend-box')
    def recommend_box(self, request, pk=None):
        order = self.get_object()
        recommendation = recommend_box_for_order(order)

        if recommendation is None:
            return Response(
                {'detail': 'No suitable box found for this order.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = BoxRecommendationSerializer(recommendation)
        return Response(serializer.data)
