# urls.py
from django.urls import path
from . import views

urlpatterns = [

    #-------------------------- DRIVER ------------------------------------
    path('driver/register/', views.driver_register, name='driver_register'),
    path('drivers/', views.DriverListAPIView.as_view(), name='driver-list'),
    path('drivers/<int:pk>/', views.DriverUpdateAPIView.as_view(), name='driver-update'),

    # -------------------------- RIDER ------------------------------------
    path('rider/register/', views.rider_register, name='rider_register'),
    path('riders/', views.RiderListAPIView.as_view(), name='rider-list'),

    # -------------------------- RIDE ------------------------------------

    path('ride/create/', views.create_ride_request, name='create_ride'),
    path('rides/', views.get_rides, name='get_rides'),
    path('ride/<int:ride_id>/', views.get_ride_detail, name='get_ride_detail'),
    path('ride/<int:ride_id>/update/status/', views.update_ride_status, name='update_ride_status'),
    path('ride/<int:ride_id>/accept/', views.accept_ride_request, name='accept_ride_request'),
]
