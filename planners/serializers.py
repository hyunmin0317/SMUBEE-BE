from rest_framework import serializers
from .models import Plan

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class CreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    category = serializers.ReadOnlyField()
    date = serializers.ReadOnlyField()

    class Meta:
        model = Plan
        fields = '__all__'