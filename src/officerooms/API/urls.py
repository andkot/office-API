from .views import (RoomView,
                    UpdateDeleteBookingView,
                    CreateUserView,
                    UserDetailsView)
from rest_framework import routers

from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'rooms', RoomView)
router.register(r'users', UserDetailsView)

urlpatterns = router.urls
urlpatterns.append(path('api-auth/', include('rest_framework.urls', namespace='rest_framework')))
urlpatterns.append(path('users/register', CreateUserView.as_view()))
urlpatterns.append(path('bookingdetails/<int:pk>/', UpdateDeleteBookingView.as_view()))
