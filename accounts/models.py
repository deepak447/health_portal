from django.db import models
from django.contrib.auth.models import AbstractUser




class CustomUser(AbstractUser):
    """
    Custom user model extending AbstractUser.

    This model adds additional fields to the default Django user model, 
    including profile picture, address, city, state, pincode, and user type.
    """

    USER_TYPE_CHOICES = (('patient', 'Patient'),('doctor', 'Doctor'))

    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=20)
    pincode = models.IntegerField(blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

 # Define how the object is represented as a string
    def __str__(self) -> str:
        return self.username
