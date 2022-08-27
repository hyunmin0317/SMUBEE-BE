from rest_framework import serializers

from planners.models import Plan
from courses.models import Subject

class SubjectSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = '__all__'

    def get_status(self, obj):
        all = Plan.objects.filter(code=obj.code, category='course').count()
        done = Plan.objects.filter(code=obj.code, category='course', checked=True).count()

        if all == 0:
            return -1
        return round(done / all * 100)
