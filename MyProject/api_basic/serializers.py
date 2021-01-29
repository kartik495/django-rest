from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model=Task
        fields=['first','last','email','password','favourite']
    
    
        def create(self, validated_data):
            return Task.objects.create(validated_data)

    