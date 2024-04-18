# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group

class Driver(AbstractUser):
    # Add any additional fields for Driver
    is_available = models.BooleanField(default=True)
    current_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    current_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this driver belongs to. A driver will get all permissions granted to each of their groups.',
        related_name='driver_set',
        related_query_name='driver',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this driver.',
        related_name='driver_set',
        related_query_name='driver',
    )

class Rider(AbstractUser):
    # Add any additional fields for Rider
    pass

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this rider belongs to. A rider will get all permissions granted to each of their groups.',
        related_name='rider_set',
        related_query_name='rider',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this rider.',
        related_name='rider_set',
        related_query_name='rider',
    )

class Ride(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('matched', 'Matched'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('started', 'Started'),
    ]

    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True)
    pickup_location = models.CharField(max_length=100)
    dropoff_location = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='requested')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pickup_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    pickup_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    @classmethod
    def match_ride(cls, ride):
        # Implement your matching algorithm here
        # Example: Find the nearest available driver
        closest_driver = Driver.objects.filter(is_available=True).first()
        if closest_driver:
            ride.driver = closest_driver
            ride.status = 'matched'
            ride.save()
            return closest_driver
        else:
            return None
