from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CafeteriaTable
from .serializers import CafeteriaTableSerializer

# GET all tables
class TableListAPI(APIView):
    def get(self, request):
        tables = CafeteriaTable.objects.all()
        serializer = CafeteriaTableSerializer(tables, many=True)
        return Response(serializer.data)


# UPDATE table status (Free / Occupied)
class UpdateTableStatusAPI(APIView):
    def patch(self, request, table_id):
        try:
            table = CafeteriaTable.objects.get(table_id=table_id)
        except CafeteriaTable.DoesNotExist:
            return Response({"error": "Table not found"}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('status')
        if new_status:
            if new_status not in ['Free', 'Occupied']:
                return Response({"error": "Invalid status. Must be 'Free' or 'Occupied'"}, status=status.HTTP_400_BAD_REQUEST)
            table.status = new_status
        table.save()

        serializer = CafeteriaTableSerializer(table)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateTableAPI(APIView):
    def post(self, request):
        table_number = request.data.get('table_number')
        if not table_number:
            return Response({"error": "table_number is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if table already exists
        if CafeteriaTable.objects.filter(table_number=table_number).exists():
            return Response({"error": "Table with this number already exists"}, status=status.HTTP_400_BAD_REQUEST)
            
        capacity = request.data.get('capacity', 4)
        
        table = CafeteriaTable(
            table_number=table_number,
            capacity=capacity,
            status='Free'
        )
        table.save()
        
        serializer = CafeteriaTableSerializer(table)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DeleteTableAPI(APIView):
    def delete(self, request, table_id):
        try:
            table = CafeteriaTable.objects.get(table_id=table_id)
            table.delete()
            return Response({"message": "Table deleted successfully"}, status=status.HTTP_200_OK)
        except CafeteriaTable.DoesNotExist:
            return Response({"error": "Table not found"}, status=status.HTTP_404_NOT_FOUND)
