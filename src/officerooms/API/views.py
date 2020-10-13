from ..models import (Room,
                      BookingDetails, )
from .serializers import (RoomSerializer,
                          RoomBookingDetailsSerializer,
                          BookRoomPlaceSerializer,
                          BookingDetailsPlaceSerializer,
                          BookingDetailsInOnePlaceSerializer,
                          CreateUserSerializer,
                          UserDetailsSerializer,
                          BookRoomPlaceSerializerUser, )

from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import permissions

from django.contrib.auth.models import User

from .permissions import IsOwnerOrReadOnly, IsOwnerOrReadOnlyUser

from datetime import datetime
import pytz

utc = pytz.UTC


def overlaps(interval1, interval2):
    results = []
    for timestamp in interval1:
        results.append(interval2[0] < timestamp < interval2[1])
    for timestamp in interval2:
        results.append(interval1[0] < timestamp < interval1[1])
    return True in results


class RoomView(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_serializer_class(self):
        if self.action == 'book':
            return BookRoomPlaceSerializer
        elif self.action == 'booking_details':
            return BookingDetailsPlaceSerializer
        elif self.action == 'show_details_in_one_place':
            return BookingDetailsInOnePlaceSerializer
        return super().get_serializer_class()

    @action(detail=True, methods=['GET', 'POST'])
    def book(self, request, pk=None):
        if request.method == 'GET':
            return self.booking_details(request, pk)
        else:
            obj = Room.objects.get(pk=pk)

            position = request.data['room_place_id']
            request_data = dict(request.data)

            try:
                position = int(position)
            except:
                raise ValidationError('Error: data must be a integer')
            try:
                dt1 = utc.localize(datetime.strptime(request_data['from_date_time'][0], '%Y-%m-%dT%H:%M'))
                dt2 = utc.localize(datetime.strptime(request_data['to_date_time'][0], '%Y-%m-%dT%H:%M'))
            except:
                raise ValidationError('Error datetime format (should be "%Y-%m-%dT%H:%M")')
            request_interval = (dt1, dt2)

            if request_interval[0] >= request_interval[1]:
                raise ValidationError('error datatime interval')
            if int(position) > int(obj.capacity):
                raise ValidationError('error place number')

            boked_list = BookingDetails.objects.filter(room_id=pk, room_place_id=position)
            boked_list_time_from = [item.from_date_time for item in boked_list]
            boked_list_time_to = [item.to_date_time for item in boked_list]

            existed_intervals = zip(boked_list_time_from, boked_list_time_to)

            for interval in existed_intervals:
                if overlaps(request_interval, interval) is True:
                    raise ValidationError('This datetime interval has already booked')

            user = User.objects.get(id=self.request.user.pk)

            serializer = BookRoomPlaceSerializer(data=request.data,
                                                 context={'request': request, 'room_id': obj, 'owner': user})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def booking_details(self, request, pk=None):
        obj = BookingDetails.objects.filter(room_id=pk)
        print(obj)
        obj_room = Room.objects.get(pk=pk)
        serializer = BookRoomPlaceSerializer(instance=obj, many=True, context={'request': request, 'room_id': obj_room})
        for item in serializer.data:
            del item["room_id"]
        return Response(serializer.data)

    @action(detail=True, methods=['GET', 'POST'])
    def show_details_in_one_place(self, request, pk=None, room_place_id=1):
        if request.method == 'GET':
            obj_room = Room.objects.get(pk=pk)
            obj = BookingDetails.objects.filter(room_id=pk, room_place_id=room_place_id)
            serializer = BookRoomPlaceSerializer(instance=obj, many=True,
                                                 context={'request': request, 'room_id': obj_room})
            for item in serializer.data:
                del item["room_id"]
            return Response(serializer.data)
        else:
            data = dict(request.data)
            try:
                id = int(data['room_place_id'][0])
            except:
                raise ValidationError('Input error')
            serializer = BookingDetailsInOnePlaceSerializer(data={'room_place_id': id})
            serializer.is_valid(raise_exception=True)
            serializer = serializer.save()
            request.method = 'GET'
            return self.show_details_in_one_place(request, pk, serializer['room_place_id'])

    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        input_number = data['capacity']
        try:
            input_number = int(input_number[0])
        except:
            raise ValidationError('Error: data must be a integer')
        if input_number <= 0:
            raise ValidationError('Error: capasity should be more then zero')
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        result = dict(serializer.data)
        result['book'] = f'{serializer.data["url"]}book'
        result['booking_details'] = f'{serializer.data["url"]}booking_details'
        result['show_details_in_one_place'] = f'{serializer.data["url"]}show_details_in_one_place'
        del result['url']
        return Response(result)


class UpdateDeleteBookingView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookingDetails.objects.all()
    serializer_class = RoomBookingDetailsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def update(self, request, *args, **kwargs):
        pk = kwargs['pk']
        obj = Room.objects.get(pk=pk)

        position = request.data['room_place_id']
        request_data = dict(request.data)

        try:
            position = int(position)
        except:
            raise ValidationError('Error: data must be a integer')
        try:
            dt1 = utc.localize(datetime.strptime(request_data['from_date_time'][0], '%Y-%m-%dT%H:%M'))
            dt2 = utc.localize(datetime.strptime(request_data['to_date_time'][0], '%Y-%m-%dT%H:%M'))
        except:
            raise ValidationError('Error datetime format (should be "%Y-%m-%dT%H:%M")')
        request_interval = (dt1, dt2)

        if request_interval[0] >= request_interval[1]:
            raise ValidationError('error datatime interval')
        if position > int(obj.capacity):
            raise ValidationError('error place number')

        boked_list = BookingDetails.objects.filter(room_id=pk, room_place_id=position)
        boked_list_time_from = [item.from_date_time for item in boked_list]
        boked_list_time_to = [item.to_date_time for item in boked_list]

        existed_intervals = zip(boked_list_time_from, boked_list_time_to)

        for interval in existed_intervals:
            if overlaps(request_interval, interval) is True:
                raise ValidationError('This datetime interval has already booked')

        user = User.objects.get(id=self.request.user.pk)

        serializer = BookRoomPlaceSerializer(data=request.data,
                                             context={'request': request, 'room_id': obj, 'owner': user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (permissions.AllowAny,)


class UserDetailsView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailsSerializer
    permission_classes = (permissions.AllowAny, IsOwnerOrReadOnlyUser)

    @action(detail=True, methods=['GET'])
    def booking_list(self, request, pk=None):
        try:
            obj = BookingDetails.objects.filter(owner=self.request.user)
        except:
            raise ValidationError('You are exited')
        print(obj)
        serializer = BookRoomPlaceSerializerUser(instance=obj, many=True, context={'request': request})
        for item in serializer.data:
            del item["room_id"]
        return Response(serializer.data)
