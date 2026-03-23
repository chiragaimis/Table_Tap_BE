from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from api.Order.model import Order, OrderItem
from api.Order.serializer import OrderSerializer, OrderCreateSerializer, OrderStatusUpdateSerializer
from api.Cart.model import Cart
from api.permissions import IsAdmin


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.groups.filter(name='Admin').exists():
            return Order.objects.all().select_related('user').prefetch_related('items__product')
        return Order.objects.filter(user=self.request.user).select_related('user').prefetch_related('items__product')

    @action(detail=False, methods=['post'])
    def place_order(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        cart_items = Cart.objects.filter(user=request.user).select_related('product')
        
        if not cart_items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate stock
        for item in cart_items:
            if item.quantity > item.product.stock_quantity:
                return Response({
                    'error': f'Insufficient stock for {item.product.name}. Only {item.product.stock_quantity} available'
                }, status=status.HTTP_400_BAD_REQUEST)

        # Create order
        with transaction.atomic():
            total = sum(item.subtotal for item in cart_items)
            
            order = Order.objects.create(
                user=request.user,
                total_amount=total,
                delivery_address=serializer.validated_data['delivery_address'],
                contact_number=serializer.validated_data['contact_number'],
                notes=serializer.validated_data.get('notes', ''),
                payment_method='COD'
            )

            # Create order items and update stock
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
                
                # Deduct stock
                cart_item.product.stock_quantity -= cart_item.quantity
                cart_item.product.save()

            # Clear cart
            cart_items.delete()

        order_serializer = OrderSerializer(order)
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'], permission_classes=[IsAdmin])
    def update_status(self, request, pk=None):
        order = self.get_object()
        serializer = OrderStatusUpdateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        order.status = serializer.validated_data['status']
        order.save()

        order_serializer = OrderSerializer(order)
        return Response(order_serializer.data)
