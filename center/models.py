from django.db import models

# Create your models here.
from django.db import models

class TrainingCenter(models.Model):
    center_name = models.CharField(max_length=200, help_text="Name of the training center.")
    address = models.TextField(help_text="Address of the training center.")
    contact_number = models.CharField(max_length=15, blank=True, null=True, help_text="Contact number of the training center.")
    email = models.EmailField(blank=True, null=True, help_text="Email address of the training center.")
    registration_number = models.CharField(max_length=50, unique=True, help_text="Unique registration number of the training center.")
    established_date = models.DateField(blank=True, null=True, help_text="Date when the training center was established.")
    head_of_center = models.CharField(max_length=100, blank=True, null=True, help_text="Name of the head of the training center.")
    total_capacity = models.PositiveIntegerField(blank=True, null=True, help_text="Total capacity of trainees the center can accommodate.")
    specialization = models.CharField(max_length=200, blank=True, null=True, help_text="Specialization or focus area of the training center.")

    def __str__(self):
        return self.center_name