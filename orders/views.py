from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from cafeteria_tables.models import CafeteriaTable
from menu.models import MenuItem
from .models import Order
from .serializers import OrderListSerializer, UpdateOrderStatusSerializer
from order_item.models import OrderItem
from customer.models import Customer
from payment.models import Payment


class CreateOrderAPI(APIView):

    def post(self, request):
        data = request.data

        table_id = data.get("table_id")
        items = data.get("items", [])
        customer_name = data.get("customer_name")
        mobile_no = data.get("mobile_no")
        payment_mode = data.get("payment_mode")

        # 1️⃣ Validate Table
        try:
            table = CafeteriaTable.objects.get(table_id=table_id)
        except CafeteriaTable.DoesNotExist:
            return Response({"error": "Invalid table"}, status=400)

        # 2️⃣ Create Customer
        customer = Customer.objects.create(
            name=customer_name,
            contact_number=mobile_no
        )

        total_amount = 0

        # 3️⃣ Create Order (initially 0 total)
        order = Order.objects.create(
            customer_id=customer.customer_id,
            table_id=table_id,
            total_amount=0,
            order_status="Placed"
        )

        # 4️⃣ Create Order Items
        for item in items:
            try:
                menu_item = MenuItem.objects.get(item_id=item["item_id"], availability=True)
            except MenuItem.DoesNotExist:
                return Response({"error": f"Item {item['item_id']} not available"}, status=400)

            quantity = item.get("quantity", 1)

            OrderItem.objects.create(
                order_id=order.order_id,
                item_id=menu_item.item_id,
                quantity=quantity
            )

            total_amount += menu_item.price * quantity

        # 5️⃣ Update Total Amount
        order.total_amount = total_amount
        order.save()

        # 6️⃣ Create Payment
        Payment.objects.create(
            order_id=order.order_id,
            payment_mode=payment_mode,
            payment_status="Completed"
        )

        # 7️⃣ Update Table Status
        table.status = "Occupied"
        table.save()

        return Response({
            "message": "Order placed successfully",
            "order_id": order.order_id,
            "total_amount": total_amount
        }, status=status.HTTP_201_CREATED)

class OrderListAPI(APIView):
    def get(self, request):
        orders = Order.objects.all().order_by('-created_at')
        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateOrderStatusAPI(APIView):
    def patch(self, request, order_id):
        try:
            order = Order.objects.get(order_id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateOrderStatusSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Order status updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)