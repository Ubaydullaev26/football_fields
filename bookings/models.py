from django.db import models
from django.conf import settings

class Booking(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='bookings',
        on_delete=models.CASCADE
    )
    field = models.ForeignKey(
        'fields.Field',
        related_name='bookings',
        on_delete=models.CASCADE
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f'{self.field.name} booking by {self.user.username}'