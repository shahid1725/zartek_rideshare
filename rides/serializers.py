# serializers.py
from rest_framework import serializers
from .models import *



class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['username', 'email', 'password','is_available','current_latitude','current_longitude']



class RiderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rider
        fields = ['username', 'email', 'password']


class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id','rider', 'driver', 'pickup_location', 'dropoff_location', 'status', 'created_at', 'updated_at','pickup_latitude','pickup_longitude']

class RideStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['status','updated_at']
