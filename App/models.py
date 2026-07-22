from django.db import models

# Create your models here.
class MembershipPlan(models.Model):
    plan_name = models.CharField(max_length = 50)
    duration_days = models.IntegerField()
    price = models.DecimalField(max_digits = 8, decimal_places = 2)

    def __str__(self):
        return self.plan_name