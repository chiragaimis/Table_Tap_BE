from rest_framework import serializers
from api.Order.model import Order, OrderItem
from api.Product.serializer import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_detail', 'quantity', 'price', 'subtotal']
        read_only_fields = ['id']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_detail = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'user_detail', 'total_amount', 'status', 'payment_method', 
                  'delivery_address', 'contact_number', 'notes', 'items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def get_user_detail(self, obj):
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'email': obj.user.email
        }


class OrderCreateSerializer(serializers.Serializer):
    delivery_address = serializers.CharField(max_length=500)
    contact_number = serializers.CharField(max_length=20)
    notes = serializers.CharField(required=False, allow_blank=True)


class OrderStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)
