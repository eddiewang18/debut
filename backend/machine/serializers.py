from .models import *
from rest_framework import serializers

class Machine_lineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine_line
        fields = "__all__"

class MachineSerializer(serializers.ModelSerializer):
    lines = Machine_lineSerializer(many=True, read_only=True)  # 使用 related_name
    class Meta:
        model = Machine
        fields = "__all__"

class Machine_line_record_Serializer(serializers.ModelSerializer):
    tot_work_hours = serializers.SerializerMethodField()

    class Meta:
        model = Machine_line_record
        fields = "__all__"

    def get_tot_work_hours(self, obj):

        return obj.emp_amt * obj.work_hours 