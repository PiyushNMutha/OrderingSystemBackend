from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db.models import Sum, Count, Avg
from django.db.models.functions import ExtractHour
from datetime import timedelta

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

class TrackOrderAPI(APIView):
    def get(self, request, order_id):
        try:
            order = Order.objects.get(order_id=order_id)
            return Response({
                "order_id": order.order_id,
                "status": order.order_status,
                "created_at": order.created_at,
                "total_amount": order.total_amount
            }, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)


class AdminDashboardAPI(APIView):
    def get(self, request):
        today = timezone.now().date()
        current_month = today.month
        current_year = today.year

        # Basic Metrics
        daily_revenue = Order.objects.filter(created_at__date=today).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        monthly_revenue = Order.objects.filter(created_at__month=current_month, created_at__year=current_year).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        average_order_value = Order.objects.aggregate(Avg('total_amount'))['total_amount__avg'] or 0
        total_orders_today = Order.objects.filter(created_at__date=today).count()

        # ── Total Items Sold (filterable) ──────────────────────────────────────
        from_date = request.query_params.get('from_date')  # e.g. 2026-06-01
        to_date   = request.query_params.get('to_date')    # e.g. 2026-06-15
        period    = request.query_params.get('period')     # today | weekly | monthly

        if from_date and to_date:
            # Custom date range takes priority over period
            filtered_orders = Order.objects.filter(
                created_at__date__gte=from_date,
                created_at__date__lte=to_date
            )
        elif period == 'today':
            filtered_orders = Order.objects.filter(created_at__date=today)
        elif period == 'weekly':
            week_ago = today - timedelta(days=7)
            filtered_orders = Order.objects.filter(created_at__date__gte=week_ago)
        elif period == 'monthly':
            filtered_orders = Order.objects.filter(
                created_at__month=current_month,
                created_at__year=current_year
            )
        else:
            # No filter — all-time total
            filtered_orders = Order.objects.all()

        filtered_order_ids = filtered_orders.values_list('order_id', flat=True)
        total_items_sold = OrderItem.objects.filter(
            order_id__in=filtered_order_ids
        ).aggregate(total=Sum('quantity'))['total'] or 0
        # ──────────────────────────────────────────────────────────────────────

        # Order Status Breakdown
        status_breakdown_qs = Order.objects.values('order_status').annotate(count=Count('order_id'))
        status_breakdown = {item['order_status']: item['count'] for item in status_breakdown_qs}

        # Predictive & Item Analytics
        order_items_qs = OrderItem.objects.values('item_id').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity')
        item_ids = [item['item_id'] for item in order_items_qs]
        items = MenuItem.objects.filter(item_id__in=item_ids)
        item_map = {item.item_id: item.item_name for item in items}

        items_sales = []
        for item in order_items_qs:
            items_sales.append({
                "item_name": item_map.get(item['item_id'], f"Unknown Item {item['item_id']}"),
                "total_quantity": item['total_quantity']
            })

        top_selling_items = items_sales[:5]
        low_performing_items = items_sales[-5:] if len(items_sales) >= 5 else list(reversed(items_sales))

        # Peak ordering time
        peak_hours_qs = Order.objects.annotate(hour=ExtractHour('created_at')).values('hour').annotate(order_count=Count('order_id')).order_by('-order_count')[:5]
        peak_ordering_time = [{"hour": f"{item['hour']:02d}:00" if item['hour'] is not None else "Unknown", "order_count": item['order_count']} for item in peak_hours_qs]

        # Table Analytics
        table_sales_qs = Order.objects.values('table_id').annotate(total_sales=Sum('total_amount')).order_by('-total_sales')
        table_ids = [item['table_id'] for item in table_sales_qs]
        tables = CafeteriaTable.objects.filter(table_id__in=table_ids)
        table_map = {table.table_id: table.table_number for table in tables}

        table_wise_sales = []
        for item in table_sales_qs:
            table_wise_sales.append({
                "table_number": table_map.get(item['table_id'], f"Unknown Table {item['table_id']}"),
                "total_sales": item['total_sales']
            })

        # Recent Activity Feed
        recent_orders_qs = Order.objects.order_by('-created_at')[:5]
        recent_orders = []
        for order in recent_orders_qs:
            recent_orders.append({
                "order_id": order.order_id,
                "table_number": table_map.get(order.table_id, f"Unknown Table {order.table_id}"),
                "total_amount": order.total_amount,
                "status": order.order_status,
                "time": order.created_at
            })

        return Response({
            "basic_metrics": {
                "daily_revenue": daily_revenue,
                "monthly_revenue": monthly_revenue,
                "average_order_value": round(average_order_value, 2) if average_order_value else 0,
                "total_orders_today": total_orders_today,
                "total_items_sold": total_items_sold,
            },
            "applied_filter": {
                "period": period or ("custom" if from_date and to_date else "all-time"),
                "from_date": from_date,
                "to_date": to_date,
            },
            "order_status_breakdown": status_breakdown,
            "predictive_analytics": {
                "peak_ordering_time": peak_ordering_time,
                "top_selling_items": top_selling_items,
                "low_performing_items": low_performing_items
            },
            "table_analytics": {
                "table_wise_sales": table_wise_sales
            },
            "recent_activity": recent_orders
        }, status=status.HTTP_200_OK)