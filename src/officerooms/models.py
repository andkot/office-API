from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Room(models.Model):
    name = models.CharField(unique=True, max_length=255)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class BookingDetails(models.Model):
    from_date_time = models.DateTimeField(auto_now_add=False, blank=True)
    to_date_time = models.DateTimeField(auto_now_add=False, blank=True)
    room_id = models.ForeignKey(Room, default=None, on_delete=models.DO_NOTHING)
    room_place_id = models.PositiveIntegerField()
    owner = models.ForeignKey(User, related_name='booking', default=None, on_delete=models.CASCADE)
