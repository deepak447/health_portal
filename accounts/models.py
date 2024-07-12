from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import pytz
from datetime import datetime




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


class BlogPost(models.Model):
    category_type = (("Mental Health","Mental Health"), ("Heart Disease","Heart Disease"),
                     ("Covid19","Covid19" ),("Immunization","Immunization"))
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='blog_images/')
    category = models.CharField(max_length=255, choices=category_type)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE)
    summary = models.TextField(max_length=255)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title