from rest_framework import serializers
from ..models import (Room,
                      BookingDetails, )

from django.contrib.auth.models import User


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ['url', 'name', 'capacity']


class RoomBookingDetailsSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    room_id = serializers.ReadOnlyField(source='Room')

    class Meta:
        model = BookingDetails
        fields = ['room_id', 'room_place_id', 'from_date_time', 'to_date_time', 'owner']


class BookRoomPlaceSerializer(serializers.HyperlinkedModelSerializer):
    from_date_time = serializers.DateTimeField()
    to_date_time = serializers.DateTimeField()
    room_id = serializers.SerializerMethodField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    def get_room_id(self, obj):
        return self.context['room_id'].id

    class Meta:
        model = BookingDetails
        fields = ['id', 'room_id', 'room_place_id', 'from_date_time', 'to_date_time', 'owner']

    def validate(self, attrs):
        attrs['room_id'] = self.context.get('room_id')
        attrs['owner'] = self.context.get('owner')
        return attrs


class BookRoomPlaceSerializerUser(serializers.HyperlinkedModelSerializer):
    from_date_time = serializers.DateTimeField()
    to_date_time = serializers.DateTimeField()
    # room_id = serializers.SerializerMethodField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')


    class Meta:
        model = BookingDetails
        fields = ['id', 'room_id', 'room_place_id', 'from_date_time', 'to_date_time', 'owner']

    # def validate(self, attrs):
    #     attrs['room_id'] = self.context.get('room_id')
    #     attrs['owner'] = self.context.get('owner')
    #     return attrs


class BookingDetailsPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingDetails
        fields = '__all__'


class BookingDetailsInOnePlaceSerializer(serializers.Serializer):
    room_place_id = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        return validated_data


class UserSerializer(serializers.ModelSerializer):
    booking = serializers.PrimaryKeyRelatedField(many=True, queryset=BookingDetails.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'booking']


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

