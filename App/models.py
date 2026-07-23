from django.db import models





#membership plan model
class MembershipPlan(models.Model):
    plan_name = models.CharField(max_length=50)
    duration_days = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.plan_name




#member model
class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)

    membership_plan = models.ForeignKey(
        MembershipPlan,
        on_delete=models.CASCADE
    )

    joining_date = models.DateField()
    expiry_date = models.DateField()

    STATUS = [
        ("Active", "Active"),
        ("Expired", "Expired"),
    ]

    membership_status = models.CharField(
        max_length=10,
        choices=STATUS,
        default="Active"
    )

    def __str__(self):
        return self.name



    
#payment model
class Payment(models.Model):
    PAYMENT_METHODS = [
        ("Cash", "Cash"),
        ("UPI", "UPI"),
        ("Card", "Card"),
        ("Net Banking", "Net Banking"),
    ]

    PAYMENT_STATUSES = [
        ("Paid", "Paid"),
        ("Pending", "Pending"),
        ("Failed", "Failed"),
    ]

    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE
    )

    membership_plan = models.ForeignKey(
        MembershipPlan,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    payment_date = models.DateField()

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS
    )

    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUSES,
        default='Paid'
    )

    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.member.name} - {self.amount}"





