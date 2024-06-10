from rest_framework import serializers
from .models import Task
import sys
sys.path.append("..")
from accounts.models import User


class TaskSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    employee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Task
        fields = [
            "id",
            "title", 
            "description", 
            "customer", 
            "employee", 
            "status", 
            "date_of_create",
            "date_of_update",
            "data_of_close",
            "report"]

    def create(self, validated_data):
        task = Task.objects.create(**validated_data)
        return task