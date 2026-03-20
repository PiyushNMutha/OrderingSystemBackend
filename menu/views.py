from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import MenuCategory, MenuItem
from .serializers import MenuCategorySerializer, MenuItemSerializer
from cafeteria_tables.models import CafeteriaTable


class MenuCategoryByTableAPI(APIView):
    def get(self, request, table_number):
        try:
            table = CafeteriaTable.objects.get(table_number=table_number)
        except CafeteriaTable.DoesNotExist:
            return Response(
                {"error": "Invalid table number"},
                status=status.HTTP_404_NOT_FOUND
            )

        # OPTIONAL: block if table is already occupied
        # if table.status == 'Occupied':
        #     return Response(
        #         {"error": "Table is currently occupied"},
        #         status=status.HTTP_403_FORBIDDEN
        #     )

        categories = MenuCategory.objects.all()
        serializer = MenuCategorySerializer(categories, many=True)

        return Response({
            "table_number": table.table_number,
            "table_status": table.status,
            "categories": serializer.data
        }, status=status.HTTP_200_OK)


class MenuItemByTableAPI(APIView):
    def get(self, request, table_number):
        # 1. Validate table number
        try:
            table = CafeteriaTable.objects.get(table_number=table_number)
        except CafeteriaTable.DoesNotExist:
            return Response(
                {"error": "Invalid table number"},
                status=status.HTTP_404_NOT_FOUND
            )

        # 2. Fetch available menu items
        items = MenuItem.objects.filter(availability=True)

        serializer = MenuItemSerializer(items, many=True)

        return Response({
            "table_number": table.table_number,
            "table_status": table.status,
            "menu_items": serializer.data
        }, status=status.HTTP_200_OK)
