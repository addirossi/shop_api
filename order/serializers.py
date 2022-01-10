from rest_framework import serializers

from order.models import OrderItem, Order


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemsSerializer(many=True)
    total_sum = serializers.DecimalField(max_digits=10,
                                         decimal_places=2,
                                         read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'total_sum', 'address',
                  'notes', 'created_at', 'items']

    def create(self, validated_data):
        items = validated_data.pop('items', [])
        user = self.context.get('request').user
        order = Order(address=validated_data.get('address'),
                      notes=validated_data.get('notes', ''),
                      user=user)
        total = 0
        for item in items:
            total += item['product'].price * item['quantity']
            OrderItem.objects.create(order=order,
                                     product=item['product'],
                                     quantity=item['quantity'])
        order.total_sum = total
        order.save()
        return order


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'address', 'notes', 'created_at']
