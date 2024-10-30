from datetime import date,time
from rest_framework import viewsets, filters, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Field, FieldFilter
from .serializers import FieldSerializer
from users.permissions import IsFieldOwner
from django.db.models import Q, F
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos.point import Point
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import ListAPIView




class FieldViewSet(viewsets.ModelViewSet):
    serializer_class = FieldSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['name', 'address']
    ordering_fields = ['hourly_rate']

    def get_queryset(self):
        base_queryset = Field.objects.all()
        if self.request.user.is_authenticated and getattr(self.request.user, 'role', None) == 'owner':
            base_queryset = base_queryset.filter(owner=self.request.user)
        return base_queryset

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsFieldOwner()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FieldAvailabilityView(ListAPIView):
    serializer_class = FieldSerializer
    queryset = Field.objects.all()
    filterset_class = FieldFilter
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):
        selected_location = self.request.query_params.get('location')
        selected_date = self.request.query_params.get('date')
        start_time = self.request.query_params.get('start_time')
        end_time = self.request.query_params.get('end_time')

        if selected_date and start_time and end_time:
            self.queryset = self.queryset.exclude(
                Q(bookings__date=selected_date) &
                Q(bookings__start_time__lt=end_time) &
                Q(bookings__end_time__gt=start_time)
            )

        if selected_location:
            longitude, latitude = map(float, selected_location.split(','))
            user_position = Point(longitude, latitude, srid=4326)

            self.queryset = Field.objects.annotate(
                proximity=Distance('location', user_position)
            ).order_by('proximity')

        return self.queryset.prefetch_related("images")

    @extend_schema(
        parameters=[
            OpenApiParameter(name='location', location='query', required=False, type=str, description="User's current location in 'lon,lat' format"),
            OpenApiParameter(name='date', location='query', required=False, type=str, description="Date for field availability check"),
            OpenApiParameter(name='start_time', location='query', required=False, type=str, description="Desired start time for booking"),
            OpenApiParameter(name='end_time', location='query', required=False, type=str, description="Desired end time for booking"),
        ],
        responses={200: FieldSerializer(many=True)},
        tags=['Field Availability'],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
# class AvailableFieldsView(generics.ListAPIView):
#     serializer_class = FieldSerializer
#     filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
#     ordering_fields = ['distance', 'hourly_rate']

#     def get_queryset(self):
#         from bookings.models import Booking  # Import here to avoid circular import
#         latitude = self.request.query_params.get('latitude')
#         longitude = self.request.query_params.get('longitude')
#         start_time = self.request.query_params.get('start_time')
#         end_time = self.request.query_params.get('end_time')

#         queryset = Field.objects.all()

#         # Filter by availability
#         if start_time and end_time:
#             bookings = Booking.objects.filter(
#                 Q(start_time__lt=end_time) & Q(end_time__gt=start_time)
#             ).values_list('field_id', flat=True)
#             queryset = queryset.exclude(id__in=bookings)

#         # Annotate distance
#         if latitude and longitude:
#             latitude = float(latitude)
#             longitude = float(longitude)
#             queryset = queryset.annotate(
#                 distance=ACos(
#                     Cos(Radians(latitude)) * Cos(Radians(F('latitude'))) *
#                     Cos(Radians(F('longitude')) - Radians(longitude)) +
#                     Sin(Radians(latitude)) * Sin(Radians(F('latitude')))
#                 ) * 6371  # Earth's radius in km
#             )
#             queryset = queryset.order_by('distance')

#         return queryset
    
    
class FieldDetailView(generics.RetrieveAPIView):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer