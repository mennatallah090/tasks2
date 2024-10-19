from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Task
from .serializers import TaskSerializer, UserSerializer
from django.contrib.auth.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def toggle_complete(self, request, pk=None):
        task = self.get_object()
        if task.status == 'PENDING':
            task.status = 'COMPLETED'
            task.completed_at = timezone.now()
        else:
            task.status = 'PENDING'
            task.completed_at = None
        task.save()
        return Response(TaskSerializer(task).data)

    def list(self, request):
        queryset = self.get_queryset()
        status = request.query_params.get('status')
        priority = request.query_params.get('priority')
        due_date = request.query_params.get('due_date')
        sort_by = request.query_params.get('sort_by')

        if status:
            queryset = queryset.filter(status=status.upper())
        if priority:
            queryset = queryset.filter(priority=priority.upper())
        if due_date:
            queryset = queryset.filter(due_date__date=due_date)
        if sort_by:
            if sort_by == 'due_date':
                queryset = queryset.order_by('due_date')
            elif sort_by == 'priority':
                queryset = queryset.order_by('priority')

        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)
    

