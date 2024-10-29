
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from fields.views import FieldDetailView
from bookings.views import BookingDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/fields/', include('fields.urls')),
    path('api/bookings/', include('bookings.urls')),
    path('fields/<int:pk>/', FieldDetailView.as_view(), name='field_detail'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='booking_detail'),
    path('api/users/', include('users.urls')),  # Optional
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]