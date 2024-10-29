from rest_framework import viewsets, filters, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Field
from .serializers import FieldSerializer
from users.permissions import IsFieldOwner
from django.db.models import Q, F
from django.db.models.functions import ACos, Cos, Radians, Sin

class FieldViewSet(viewsets.ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['name', 'address']
    ordering_fields = ['hourly_rate']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsFieldOwner()]
        else:
            return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated and self.request.user.role == 'owner':
            queryset = queryset.filter(owner=self.request.user)
        return queryset

class AvailableFieldsView(generics.ListAPIView):
    serializer_class = FieldSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['distance', 'hourly_rate']

    def get_queryset(self):
        from bookings.models import Booking  # Import here to avoid circular import
        latitude = self.request.query_params.get('latitude')
        longitude = self.request.query_params.get('longitude')
        start_time = self.request.query_params.get('start_time')
        end_time = self.request.query_params.get('end_time')

        queryset = Field.objects.all()

        # Filter by availability
        if start_time and end_time:
            bookings = Booking.objects.filter(
                Q(start_time__lt=end_time) & Q(end_time__gt=start_time)
            ).values_list('field_id', flat=True)
            queryset = queryset.exclude(id__in=bookings)

        # Annotate distance
        if latitude and longitude:
            latitude = float(latitude)
            longitude = float(longitude)
            queryset = queryset.annotate(
                distance=ACos(
                    Cos(Radians(latitude)) * Cos(Radians(F('latitude'))) *
                    Cos(Radians(F('longitude')) - Radians(longitude)) +
                    Sin(Radians(latitude)) * Sin(Radians(F('latitude')))
                ) * 6371  # Earth's radius in km
            )
            queryset = queryset.order_by('distance')

        return queryset
    
    
class FieldDetailView(generics.RetrieveAPIView):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer