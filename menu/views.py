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

class CreateMenuItemAPI(APIView):
    def post(self, request):
        serializer = MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            # Validate category ID
            category_id = serializer.validated_data.get('category_id')
            if not MenuCategory.objects.filter(category_id=category_id).exists():
                return Response({"error": "Invalid Category ID"}, status=status.HTTP_400_BAD_REQUEST)
                
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateMenuItemAPI(APIView):
    def patch(self, request, item_id):
        try:
            menu_item = MenuItem.objects.get(item_id=item_id)
        except MenuItem.DoesNotExist:
            return Response({"error": "Menu item not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MenuItemSerializer(menu_item, data=request.data, partial=True)
        if serializer.is_valid():
            # Validate category ID if it's being updated
            category_id = request.data.get('category_id')
            if category_id is not None:
                if not MenuCategory.objects.filter(category_id=category_id).exists():
                    return Response({"error": "Invalid Category ID"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteMenuItemAPI(APIView):
    def delete(self, request, item_id):
        try:
            menu_item = MenuItem.objects.get(item_id=item_id)
            menu_item.delete()
            return Response({"message": "Menu item deleted successfully"}, status=status.HTTP_200_OK)
        except MenuItem.DoesNotExist:
            return Response({"error": "Menu item not found"}, status=status.HTTP_404_NOT_FOUND)
