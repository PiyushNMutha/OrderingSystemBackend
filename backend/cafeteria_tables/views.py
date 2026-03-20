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
            return Response({"error": "Table not found"}, status=404)

        table.status = request.data.get('status', table.status)
        table.save()

        serializer = CafeteriaTableSerializer(table)
        return Response(serializer.data)
