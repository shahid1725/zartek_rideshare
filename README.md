# zartek_rideshare

Ride Share Project
Overview
The Ride Share project is a Django-based web application that facilitates ride requests and matching between drivers and riders. It provides API endpoints for user registration, ride requests, ride tracking, and status updates.

Features
User registration and login using Django Rest Framework (DRF).
Models for rides with fields including rider, driver, pickup location, dropoff location, status, created at, and updated at.
API endpoints for creating a ride request, viewing ride details, and listing all rides.
API endpoints for updating the status of a ride (e.g., started, completed, cancelled).
Algorithm for matching ride requests with available drivers, based on proximity or other factors.
API endpoint for drivers to accept ride requests.

Installation and Setup

  Clone the repository:

    git clone https://github.com/shahid1725/zartek_rideshare.git
    cd ride_share

  Install dependencies:

    pip install -r requirements.txt

  Apply migrations:

    python manage.py migrate

  Start the development server:

    python manage.py runserver

  Access the API endpoints using the provided URLs
  API Endpoints:
  
    Driver Registration: POST /api/driver/register/
    List Drivers: GET /api/drivers/
    Update Driver Profile: PUT /api/drivers/<int:pk>/
    Rider Registration: POST /api/rider/register/
    Create Ride Request: POST /api/ride/create/
    List Rides: GET /api/rides/
    Get Ride Detail: GET /api/ride/<int:ride_id>/
    Update Ride Status: PUT /api/ride/<int:ride_id>/update/status/
    Accept Ride Request: POST /api/ride/<int:ride_id>/accept/

  Testing

    Basic Django tests have been implemented for models and API endpoints.
    Additional tests are required for the ride matching algorithm, ride status updates, driver API endpoints, and ride tracking simulation.

  Future Improvements

    Implement real-time ride tracking functionality.
    Enhance the ride matching algorithm to consider more factors.
    Add authentication and authorization mechanisms for API endpoints.

  
 
