from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FieldViewSet, AvailableFieldsView

router = DefaultRouter()
router.register(r'', FieldViewSet)

urlpatterns = [
    path('available-fields/', AvailableFieldsView.as_view(), name='available-fields'),
    path('', include(router.urls)),
]