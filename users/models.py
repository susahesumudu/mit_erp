from django.db import models

# Create your models here.from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    # Link this Profile model to the User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Add a gender field to the profile
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),  # Optional for other gender choices
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

