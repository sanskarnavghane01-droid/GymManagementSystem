from django.contrib import admin
from .models import MembershipPlan, Member, Payment
# Register your models here.
admin.site.register(MembershipPlan)
admin.site.register(Member)
admin.site.register(Payment)