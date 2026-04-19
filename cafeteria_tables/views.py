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
