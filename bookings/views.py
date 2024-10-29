from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Booking
from .serializers import BookingSerializer
from .permissions import IsBookingOwnerOrFieldOwner

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['field', 'user']

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAuthenticated(), IsBookingOwnerOrFieldOwner()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        else:
            return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role == 'owner':
            queryset = queryset.filter(field__owner=self.request.user)
        elif self.request.user.role == 'user':
            queryset = queryset.filter(user=self.request.user)
        return queryset
    
class BookingDetailView(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer