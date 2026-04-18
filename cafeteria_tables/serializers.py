import qrcode
import base64
from io import BytesIO
from rest_framework import serializers
from .models import CafeteriaTable

class CafeteriaTableSerializer(serializers.ModelSerializer):
    qr_code = serializers.SerializerMethodField()

    class Meta:
        model = CafeteriaTable
        fields = '__all__'

    def get_qr_code(self, obj):
        # Base URL (change this)
        base_url = "https://coffee-ordering-systemqr.vercel.app/"

        url = f"{base_url}{obj.table_number}"

        # Generate QR
        qr = qrcode.make(url)

        # Convert to base64
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        qr_str = base64.b64encode(buffer.getvalue()).decode()

        return f"data:image/png;base64,{qr_str}"
