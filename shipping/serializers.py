from rest_framework import serializers

from .models import Box, Order, OrderItem, Product


def validate_positive(value):
    if value <= 0:
        raise serializers.ValidationError('This value must be greater than 0.')
    return value


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'length', 'width', 'height', 'weight']

    def validate_length(self, value):
        return validate_positive(value)

    def validate_width(self, value):
        return validate_positive(value)

    def validate_height(self, value):
        return validate_positive(value)

    def validate_weight(self, value):
        return validate_positive(value)


class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = [
            'id',
            'name',
            'inner_length',
            'inner_width',
            'inner_height',
            'max_weight',
            'cost',
            'is_active',
        ]

    def validate_inner_length(self, value):
        return validate_positive(value)

    def validate_inner_width(self, value):
        return validate_positive(value)

    def validate_inner_height(self, value):
        return validate_positive(value)

    def validate_max_weight(self, value):
        return validate_positive(value)

    def validate_cost(self, value):
        if value < 0:
            raise serializers.ValidationError('Cost cannot be negative.')
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'Quantity must be greater than 0.',
            )
        return value


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'created_at', 'items']
        read_only_fields = ['created_at']

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError(
                'Order must contain at least one item.',
            )
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        instance.customer_name = validated_data.get(
            'customer_name',
            instance.customer_name,
        )
        instance.save()

        if items_data is not None:
            instance.items.all().delete()
            for item_data in items_data:
                OrderItem.objects.create(order=instance, **item_data)

        return instance


class BoxRecommendationSerializer(serializers.Serializer):
    box = BoxSerializer()
    total_weight = serializers.DecimalField(max_digits=8, decimal_places=2)
    total_product_volume = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
