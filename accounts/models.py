from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.
class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to='profile_pics', default='profile_pics/default.jpg')
    phone_number = models.CharField(max_length=10)
    is_delivery_person = models.BooleanField(default=False)
    is_farmer = models.BooleanField(default=False)
    address = models.CharField(max_length=100)

    # Use Django's built-in UserManager, which supports authentication
    objects = UserManager()  

    def __str__(self):
        return self.username