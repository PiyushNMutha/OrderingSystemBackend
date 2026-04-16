from rest_framework import serializers

class OrderCreateSerializer(serializers.Serializer):
    table_id = serializers.IntegerField()
    customer_name = serializers.CharField(max_length=100)
    mobile_no = serializers.CharField(max_length=15)
    payment_mode = serializers.ChoiceField(choices=['cash', 'upi'])

    items = serializers.ListField(
        child=serializers.DictField()
    )