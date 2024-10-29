
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import permissions
from fields.views import FieldDetailView
from bookings.views import BookingDetailView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Fastfood API",
      default_version='v1',
      description="Документация для API фастфуд ресторана",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="support@fastfood.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/fields/', include('fields.urls')),
    path('api/bookings/', include('bookings.urls')),
    path('fields/<int:pk>/', FieldDetailView.as_view(), name='field_detail'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='booking_detail'),
    path('api/users/', include('users.urls')),  # Optional
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]