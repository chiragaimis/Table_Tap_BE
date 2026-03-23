from rest_framework import serializers
from api.Cart.model import Cart
from api.Product.serializer import ProductSerializer


class CartSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'product_detail', 'quantity', 'subtotal', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        return value

    def validate(self, data):
        product = data.get('product')
        quantity = data.get('quantity', 1)
        
        if product and quantity > product.stock_quantity:
            raise serializers.ValidationError(f"Only {product.stock_quantity} items available in stock")
        
        return data
