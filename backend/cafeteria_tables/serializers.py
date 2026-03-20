from rest_framework import serializers
from .models import CafeteriaTable

class CafeteriaTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = CafeteriaTable
        fields = '__all__'
