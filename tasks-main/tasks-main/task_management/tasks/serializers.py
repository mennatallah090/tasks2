from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class TaskSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'priority', 'status', 'user', 'created_at', 'updated_at', 'completed_at']
        read_only_fields = ['created_at', 'updated_at', 'completed_at']

    def validate_due_date(self, value):
        from django.utils import timezone
        if value < timezone.now():
            raise serializers.ValidationError("Due date must be in the future")
        return value