from django.db import models

# Create your models here.
class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)

    membership_plan = models.CharField(max_length=50)

    joining_date = models.DateField()

    expiry_date = models.DateField()

    STATUS = [
        ('Active', 'Active'),
        ('Expired', 'Expired'),
    ]

    membership_status = models.CharField(
        max_length=10,
        choices=STATUS,
        default='Active'
    )

    def __str__(self):
        return self.name