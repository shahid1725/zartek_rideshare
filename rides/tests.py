from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Ride,Driver,Rider
from django.contrib.auth import get_user_model
from .models import Ride, Driver, Rider
User = get_user_model()


class RideTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.driver_user = User.objects.create_user(username='driver', password='testpass', is_driver=True)
        self.rider_user = User.objects.create_user(username='rider', password='testpass', is_rider=True)
        self.ride = Ride.objects.create(rider=self.rider_user, driver=self.driver_user, pickup_location='Location A', dropoff_location='Location B')

    def test_create_ride(self):
        url = reverse('ride-list')
        data = {
            'rider': self.rider_user.id,  # Provide rider ID
            'driver': self.driver_user.id,
            'pickup_location': 'Location C',
            'dropoff_location': 'Location D'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class RideModelTestCase(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create(username='test_driver', is_available=True)
        self.rider = Rider.objects.create(username='test_rider')
        self.ride = Ride.objects.create(rider=self.rider, driver=self.driver, pickup_location='Location A', dropoff_location='Location B')

    def test_ride_creation(self):
        self.assertEqual(self.ride.pickup_location, 'Location A')
        self.assertEqual(self.ride.dropoff_location, 'Location B')
        self.assertEqual(self.ride.status, 'requested')  # default status

    def test_match_ride_method(self):
        matched_driver = Ride.match_ride(self.ride)
        self.assertEqual(matched_driver, self.driver)

class DriverModelTestCase(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create(username='test_driver', is_available=True)

    def test_driver_creation(self):
        self.assertEqual(self.driver.username, 'test_driver')
        self.assertTrue(self.driver.is_available)

class RiderModelTestCase(TestCase):
    def setUp(self):
        self.rider = Rider.objects.create(username='test_rider')

    def test_rider_creation(self):
        self.assertEqual(self.rider.username, 'test_rider')

#-----------------------------------------------------------------------------------

from django.contrib.auth import get_user_model

User = get_user_model()

class RideAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.driver_user = User.objects.create_user(username='driver', password='testpass', is_driver=True)
        self.rider_user = User.objects.create_user(username='rider', password='testpass', is_rider=True)

    def test_create_ride(self):
        url = reverse('ride-list')
        data = {
            'rider': self.rider_user.id,  # Provide rider ID
            'driver': self.driver_user.id,
            'pickup_location': 'Location C',
            'dropoff_location': 'Location D'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class APITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.driver_user = User.objects.create_user(username='driver', password='testpass', is_driver=True)
        self.rider_user = User.objects.create_user(username='rider', password='testpass', is_rider=True)
        self.ride = Ride.objects.create(rider=self.rider_user, driver=self.driver_user, pickup_location='Location A', dropoff_location='Location B')

    def test_create_ride_request(self):
        url = reverse('create-ride-request')
        data = {
            'rider': self.rider_user.id,
            'pickup_location': 'Location C',
            'dropoff_location': 'Location D'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_accept_ride_request(self):
        url = reverse('accept-ride-request', kwargs={'ride_id': self.ride.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_rides(self):
        url = reverse('get-rides')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_ride_detail(self):
        url = reverse('get-ride-detail', kwargs={'ride_id': self.ride.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_ride_status(self):
        url = reverse('update-ride-status', kwargs={'ride_id': self.ride.id})
        data = {'status': 'completed'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

#------------------------------------ALGORITHM TESTS--------------------------------

from .views import match_driver_by_proximity
from .views import accept_ride_request, update_ride_status
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Ride, Driver

class RideMatchingAlgorithmTest(TestCase):
    def test_match_driver_by_proximity(self):
        # Create sample ride object
        ride = Ride.objects.create(pickup_latitude=..., pickup_longitude=...)

        # Create sample available drivers
        driver1 = Driver.objects.create(current_latitude=..., current_longitude=...)
        driver2 = Driver.objects.create(current_latitude=..., current_longitude=...)

        # Test scenario where there are available drivers
        matched_driver = match_driver_by_proximity(ride)
        self.assertIsNotNone(matched_driver)
        self.assertEqual(ride.driver, matched_driver)




class RideStatusUpdatesTest(TestCase):
    def setUp(self):
        # Create sample ride for testing
        self.ride = Ride.objects.create(pickup_latitude=..., pickup_longitude=..., status='requested')

    def test_accept_ride_request(self):
        # Test accepting a ride request
        client = APIClient()
        response = client.post(f'/api/rides/accept/{self.ride.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ride.refresh_from_db()
        self.assertEqual(self.ride.status, 'accepted')

    def test_invalid_accept_ride_request(self):
        # Test accepting a ride request with invalid status
        self.ride.status = 'matched'
        self.ride.save()
        client = APIClient()
        response = client.post(f'/api/rides/accept/{self.ride.pk}/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Ride request cannot be accepted at this time')

    def test_update_ride_status(self):
        # Test updating ride status
        client = APIClient()
        data = {'status': 'started'}
        response = client.put(f'/api/rides/{self.ride.pk}/status/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ride.refresh_from_db()
        self.assertEqual(self.ride.status, 'started')

    def test_invalid_update_ride_status(self):
        # Test updating ride status with missing status field
        client = APIClient()
        data = {}  # Missing 'status' field
        response = client.put(f'/api/rides/{self.ride.pk}/status/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Status is required', response.data['message'])

class DriverAPIEndpointsTest(TestCase):
    def setUp(self):
        # Create sample driver for testing
        self.driver_data = {
            'username': 'test_driver',
            'email': 'test_driver@example.com',
            'password': 'test_password',
            'is_available': True,
            'current_latitude': 0.0,
            'current_longitude': 0.0
        }
        self.driver = Driver.objects.create(**self.driver_data)

    def test_driver_register(self):
        # Test driver registration endpoint
        client = APIClient()
        url = reverse('driver-register')  # Assuming 'driver-register' is the name of your registration endpoint
        response = client.post(url, self.driver_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Driver.objects.filter(username='test_driver').exists())

    def test_driver_list_api(self):
        # Test driver list API endpoint
        client = APIClient()
        url = reverse('driver-list')  # Assuming 'driver-list' is the name of your driver list endpoint
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Assuming only one driver is created in setUp

    def test_driver_update_api(self):
        # Test driver update API endpoint
        client = APIClient()
        updated_data = {'username': 'updated_username'}
        url = reverse('driver-detail', kwargs={'pk': self.driver.pk})  # Assuming 'driver-detail' is the name of your driver detail endpoint
        response = client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.driver.refresh_from_db()
        self.assertEqual(self.driver.username, 'updated_username')

class RideTrackingSimulationTest(TestCase):
    def setUp(self):
        # Create sample ride and driver for testing
        self.driver = Driver.objects.create(username='test_driver', current_latitude=0.0, current_longitude=0.0)
        self.ride = Ride.objects.create(driver=self.driver, status='matched', pickup_latitude=0.0, pickup_longitude=0.0)

    def test_ride_tracking_simulation(self):
        # Test ride tracking simulation
        # Assuming there's a function to simulate ride tracking, let's call it simulate_ride_tracking
        # This function might update the driver's location and the ride status based on some logic

        # Initial ride status and driver location
        initial_ride_status = self.ride.status
        initial_driver_location = (self.driver.current_latitude, self.driver.current_longitude)

        # Simulate ride tracking
        simulate_ride_tracking(self.ride, self.driver)

        # Check if the ride status and driver location are updated
        self.assertNotEqual(initial_ride_status, self.ride.status)
        self.assertNotEqual(initial_driver_location, (self.driver.current_latitude, self.driver.current_longitude))

        # Additional assertions based on your ride tracking logic
