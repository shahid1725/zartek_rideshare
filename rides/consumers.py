# consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
from .models import Ride

class RideTrackerConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        # Get ride_id from URL or query params
        ride_id = self.scope['url_route']['kwargs']['ride_id']

        # Track the ride in real-time
        self.track_ride(ride_id)

    def track_ride(self, ride_id):
        # Infinite loop to periodically update ride's current location
        while True:
            ride = Ride.objects.get(pk=ride_id)
            current_location = ride.update_current_location()  # Your method to update current location
            self.send(json.dumps({'current_location': current_location}))

            # Sleep for a certain period (e.g., every 10 seconds)
            import time
            time.sleep(10)

    def disconnect(self, close_code):
        # Clean up resources when WebSocket connection is closed
        pass
