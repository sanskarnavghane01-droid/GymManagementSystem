from django.db import models

# Create your models here.
#trainer model




class Trainer(models.Model):
    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]

    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
        ("On Leave", "On Leave"),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="Male")
    specialization = models.CharField(max_length=100)
    experience = models.IntegerField(help_text="Years of experience")
    joining_date = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="Active")
    address = models.TextField(blank=True)

    def __str__(self):
        return self.full_name
