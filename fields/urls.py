from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FieldViewSet, FieldAvailabilityView

router = DefaultRouter()
router.register(r'', FieldViewSet, basename='field')

urlpatterns = [
    path('available-fields/', FieldAvailabilityView.as_view(), name='available-fields'),
    path('', include(router.urls)),
]