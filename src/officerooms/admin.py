from django.contrib import admin

from .models import (Room,
                     BookingDetails, )

admin.site.register([Room, BookingDetails])
