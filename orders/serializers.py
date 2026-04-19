from rest_framework import serializers
from .models import Order
from customer.models import Customer
from cafeteria_tables.models import CafeteriaTable
from order_item.models import OrderItem
from menu.models import MenuItem
from cafeteria_tables.serializers import CafeteriaTableSerializer

class OrderCreateSerializer(serializers.Serializer):
    table_id = serializers.IntegerField()
    customer_name = serializers.CharField(max_length=100)
    mobile_no = serializers.CharField(max_length=15)
    payment_mode = serializers.ChoiceField(choices=['cash', 'upi'])

    items = serializers.ListField(
        child=serializers.DictField()
    )

class OrderItemDetailSerializer(serializers.ModelSerializer):
    item_details = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['order_item_id', 'item_id', 'quantity', 'item_details']

    def get_item_details(self, obj):
        try:
            item = MenuItem.objects.get(item_id=obj.item_id)
            return {
                "item_name": item.item_name,
                "price": item.price,
                "image_url": item.image_url
            }
        except MenuItem.DoesNotExist:
            return None

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class OrderListSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()
    table = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['order_id', 'total_amount', 'order_status', 'created_at', 'customer', 'table', 'items']

    def get_customer(self, obj):
        try:
            customer = Customer.objects.get(customer_id=obj.customer_id)
            return CustomerSerializer(customer).data
        except Customer.DoesNotExist:
            return None

    def get_table(self, obj):
        try:
            table = CafeteriaTable.objects.get(table_id=obj.table_id)
            return CafeteriaTableSerializer(table).data
        except CafeteriaTable.DoesNotExist:
            return None

    def get_items(self, obj):
        items = OrderItem.objects.filter(order_id=obj.order_id)
        return OrderItemDetailSerializer(items, many=True).data

class UpdateOrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_status']

    def validate_order_status(self, value):
        valid_statuses = ['Placed', 'Preparing', 'Completed']
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Invalid status. Must be one of {valid_statuses}")
        return value