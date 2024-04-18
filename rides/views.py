# views.py
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *

@api_view(['POST'])
def driver_register(request):
    if request.method == 'POST':
        serializer = DriverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DriverListAPIView(generics.ListAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

class DriverUpdateAPIView(generics.UpdateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

@api_view(['POST'])
def rider_register(request):
    if request.method == 'POST':
        serializer = RiderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#--------------------------------------------------------------------------------------

# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Ride
from .serializers import RideSerializer

from django.db.models import F

@api_view(['POST'])
def create_ride_request(request):
    if request.method == 'POST':
        serializer = RideSerializer(data=request.data)
        if serializer.is_valid():
            ride = serializer.save()
            matched_driver = match_driver_by_proximity(ride)
            if matched_driver:
                return Response({'message': 'Ride created and matched with driver'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'No available drivers at the moment'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def match_driver_by_proximity(ride):
    # Get the pickup location of the ride
    pickup_latitude = ride.pickup_latitude
    pickup_longitude = ride.pickup_longitude

    # Get all available drivers
    available_drivers = Driver.objects.filter(is_available=True)

    closest_driver = None
    closest_distance = float('inf')

    # Iterate through each available driver to find the closest one
    for driver in available_drivers:
        # Calculate the distance between the driver's location and the pickup location
        distance = calculate_distance(driver.current_latitude, driver.current_longitude, pickup_latitude, pickup_longitude)
        if distance < closest_distance:
            closest_distance = distance
            closest_driver = driver

    # Assign the closest driver to the ride if one is found
    if closest_driver:
        ride.driver = closest_driver
        ride.status = 'matched'
        ride.save(update_fields=['driver', 'status'])  # Use update_fields to avoid unnecessary field updates
        return closest_driver
    else:
        return None

def calculate_distance(lat1, lon1, lat2, lon2):
    # Placeholder function to calculate distance between two locations
    # You can use libraries like geopy or implement your own distance calculation logic here
    # For simplicity, this function returns a constant distance of 0 for demonstration purposes
    return 0

@api_view(['POST'])
def accept_ride_request(request, ride_id):
    try:
        ride = Ride.objects.get(pk=ride_id)
    except Ride.DoesNotExist:
        return Response({"message": "Ride does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        if ride.status == 'matched':
            ride.status = 'accepted'
            ride.save()
            return Response({"message": "Ride request accepted"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Ride request cannot be accepted at this time"}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def get_rides(request):
    if request.method == 'GET':
        rides = Ride.objects.all()
        serializer = RideSerializer(rides, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def get_ride_detail(request, ride_id):
    try:
        ride = Ride.objects.get(pk=ride_id)
    except Ride.DoesNotExist:
        return Response({"message": "Ride does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RideSerializer(ride)
        return Response(serializer.data)


@api_view(['PUT'])
def update_ride_status(request, ride_id):
    try:
        ride = Ride.objects.get(pk=ride_id)
    except Ride.DoesNotExist:
        return Response({"message": "Ride does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        data = request.data
        if 'status' in data:
            ride.status = data['status']
            ride.save()
            serializer = RideStatusUpdateSerializer(ride)
            return Response(serializer.data)
        else:
            return Response({"message": "Status is required"}, status=status.HTTP_400_BAD_REQUEST)