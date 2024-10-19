from django.urls import path
from .views import TaskViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', TaskViewSet, basename='task')

urlpatterns = router.urls